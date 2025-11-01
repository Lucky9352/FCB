# Design Document

## Overview

The Gaming Cafe Booking System is a modern Django web application designed as a SaaS solution by TapNex Technologies for a single gaming cafe. The system provides automatic slot generation, hybrid booking options (private/shared), and comprehensive management tools. Customers can book games exclusively online with flexible private or shared booking options, while cafe owners manage game catalogs with automated scheduling. The architecture leverages Supabase for real-time capacity tracking, Tailwind CSS for responsive design, and is optimized for Vercel deployment.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django App     │    │   Supabase      │
│   (Templates +  │◄──►│   (Business      │◄──►│   (PostgreSQL + │
│   Tailwind CSS) │    │   Logic)         │    │   Real-time)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Vercel        │    │   Payment        │    │   Google OAuth  │
│   (Hosting)     │    │   Gateway        │    │   (Auth)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Technology Stack

- **Backend**: Django 4.2+ with Django REST Framework
- **Database**: Supabase (PostgreSQL) with real-time subscriptions
- **Frontend**: Django Templates with Tailwind CSS
- **Authentication**: Google OAuth (customers) + Django Auth (cafe owner/superuser)
- **Deployment**: Vercel with serverless functions
- **Payment**: Stripe/PayPal integration
- **Real-time**: Supabase real-time for live booking updates

## Components and Interfaces

### 1. Authentication System

#### Google OAuth Integration
- **Purpose**: Customer authentication
- **Implementation**: `django-allauth` with Google provider
- **Flow**: 
  1. Customer clicks Google login
  2. Redirect to Google OAuth
  3. Return with user data
  4. Create/update customer profile
  5. Redirect to customer dashboard

#### Manual Authentication
- **Purpose**: Cafe owner and Django superuser login
- **Implementation**: Django's built-in authentication
- **Features**: Password complexity validation, session timeout

### 2. User Management System

#### Customer Model
```python
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=100, unique=True)
    avatar_url = models.URLField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
```

#### Cafe Owner Model
```python
class CafeOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cafe_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 3. Game Management System

#### Game Model
```python
class Game(models.Model):
    BOOKING_TYPES = [
        ('SINGLE', 'Single Booking (Private Only)'),
        ('HYBRID', 'Hybrid Booking (Private + Shared)'),
    ]
    
    name = models.CharField(max_length=100)  # e.g., "8-Ball Pool", "Table Tennis", "PS4 Console 1"
    description = models.TextField()
    capacity = models.PositiveIntegerField()  # Max players (1 for PC, 4 for pool table)
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPES)
    
    # Schedule Settings
    opening_time = models.TimeField()  # e.g., 11:00 AM
    closing_time = models.TimeField()  # e.g., 11:00 PM
    slot_duration_minutes = models.PositiveIntegerField()  # e.g., 60 minutes
    available_days = models.JSONField(default=list)  # ['monday', 'tuesday', ...]
    
    # Pricing
    private_price = models.DecimalField(max_digits=8, decimal_places=2)  # Full capacity price
    shared_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # Per spot price
    
    # Status
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='games/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Automatic Slot Generation
```python
class GameSlot(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_custom = models.BooleanField(default=False)  # True for manually added slots
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['game', 'date', 'start_time']

class SlotGenerator:
    @staticmethod
    def generate_slots_for_game(game, start_date, end_date):
        """Generate time slots based on game schedule settings"""
        slots = []
        current_date = start_date
        
        while current_date <= end_date:
            if current_date.strftime('%A').lower() in game.available_days:
                current_time = game.opening_time
                while current_time < game.closing_time:
                    end_time = (datetime.combine(current_date, current_time) + 
                               timedelta(minutes=game.slot_duration_minutes)).time()
                    if end_time <= game.closing_time:
                        slots.append(GameSlot(
                            game=game,
                            date=current_date,
                            start_time=current_time,
                            end_time=end_time
                        ))
                    current_time = end_time
            current_date += timedelta(days=1)
        
        return slots
```

### 4. Hybrid Booking System

#### Booking Model
```python
class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Payment'),
        ('CONFIRMED', 'Confirmed'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    BOOKING_TYPES = [
        ('PRIVATE', 'Private Booking (Full Capacity)'),
        ('SHARED', 'Shared Booking (Individual Spots)'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    game_slot = models.ForeignKey(GameSlot, on_delete=models.CASCADE)
    
    # Hybrid Booking Fields
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPES)
    spots_booked = models.PositiveIntegerField()  # 1-4 for shared, full capacity for private
    
    # Pricing and Status
    price_per_spot = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_id = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SlotAvailability(models.Model):
    """Track real-time availability for each slot"""
    game_slot = models.OneToOneField(GameSlot, on_delete=models.CASCADE)
    total_capacity = models.PositiveIntegerField()
    booked_spots = models.PositiveIntegerField(default=0)
    is_private_booked = models.BooleanField(default=False)
    
    @property
    def available_spots(self):
        return self.total_capacity - self.booked_spots if not self.is_private_booked else 0
    
    @property
    def can_book_private(self):
        return self.booked_spots == 0
    
    @property
    def can_book_shared(self):
        return not self.is_private_booked and self.available_spots > 0
```

#### Hybrid Booking Logic
```python
class BookingService:
    @staticmethod
    def get_booking_options(game_slot):
        """Return available booking options for a slot"""
        availability = SlotAvailability.objects.get(game_slot=game_slot)
        game = game_slot.game
        
        options = []
        
        # Private booking option
        if availability.can_book_private and game.booking_type == 'HYBRID':
            options.append({
                'type': 'PRIVATE',
                'price': game.private_price,
                'capacity': game.capacity,
                'description': f'Book entire {game.name} for your group'
            })
        
        # Shared booking option
        if availability.can_book_shared:
            options.append({
                'type': 'SHARED',
                'price': game.shared_price if game.booking_type == 'HYBRID' else game.private_price,
                'available_spots': availability.available_spots,
                'description': f'Book individual spot(s) - {availability.available_spots} remaining'
            })
        
        return options
    
    @staticmethod
    def create_booking(customer, game_slot, booking_type, spots_requested):
        """Create booking with capacity validation"""
        availability = SlotAvailability.objects.select_for_update().get(game_slot=game_slot)
        
        if booking_type == 'PRIVATE':
            if not availability.can_book_private:
                raise ValidationError("Private booking not available")
            availability.is_private_booked = True
            availability.booked_spots = availability.total_capacity
            spots_booked = availability.total_capacity
            price_per_spot = game_slot.game.private_price / availability.total_capacity
        
        elif booking_type == 'SHARED':
            if not availability.can_book_shared or spots_requested > availability.available_spots:
                raise ValidationError("Insufficient spots available")
            availability.booked_spots += spots_requested
            spots_booked = spots_requested
            price_per_spot = game_slot.game.shared_price
        
        availability.save()
        
        return Booking.objects.create(
            customer=customer,
            game=game_slot.game,
            game_slot=game_slot,
            booking_type=booking_type,
            spots_booked=spots_booked,
            price_per_spot=price_per_spot,
            total_amount=price_per_spot * spots_booked,
            status='PENDING'
        )
```

### 5. Payment Integration

#### Payment Service
```python
class PaymentService:
    def create_payment_intent(self, booking):
        # Stripe/PayPal integration
        pass
    
    def confirm_payment(self, payment_id):
        # Confirm payment and update booking
        pass
    
    def refund_payment(self, payment_id, amount):
        # Handle refunds for cancellations
        pass
```

### 5. TapNex Superuser Management

#### TapNex Superuser Model
```python
class TapNexSuperuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)  # Percentage
    platform_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # Fixed fee
    created_at = models.DateTimeField(auto_now_add=True)

class CommissionCalculator:
    @staticmethod
    def calculate_commission(booking_amount, commission_rate, platform_fee):
        """Calculate TapNex commission from booking"""
        commission = (booking_amount * commission_rate) / 100
        total_commission = commission + platform_fee
        net_payout = booking_amount - total_commission
        
        return {
            'gross_revenue': booking_amount,
            'commission_amount': commission,
            'platform_fee': platform_fee,
            'total_commission': total_commission,
            'net_payout': net_payout
        }
```

### 6. Real-time Updates and Capacity Tracking

#### Supabase Integration
- **Real-time subscriptions** for slot availability and capacity changes
- **Live updates** when bookings are made/cancelled with immediate capacity adjustments
- **Conflict resolution** for simultaneous booking attempts with database-level locking
- **Capacity broadcasting** to update all connected clients when spots are booked/released

#### Real-time Service
```python
class RealTimeService:
    @staticmethod
    def broadcast_availability_update(game_slot_id):
        """Broadcast availability changes to all connected clients"""
        availability = SlotAvailability.objects.get(game_slot_id=game_slot_id)
        
        # Send to Supabase real-time channel
        supabase.realtime.send({
            'event': 'availability_update',
            'payload': {
                'game_slot_id': game_slot_id,
                'available_spots': availability.available_spots,
                'can_book_private': availability.can_book_private,
                'can_book_shared': availability.can_book_shared,
                'is_private_booked': availability.is_private_booked
            }
        })
    
    @staticmethod
    def handle_booking_conflict(game_slot, booking_type, spots_requested):
        """Handle simultaneous booking attempts"""
        try:
            with transaction.atomic():
                availability = SlotAvailability.objects.select_for_update().get(
                    game_slot=game_slot
                )
                
                # Validate availability under lock
                if booking_type == 'PRIVATE' and not availability.can_book_private:
                    raise BookingConflictError("Slot no longer available for private booking")
                
                if booking_type == 'SHARED' and spots_requested > availability.available_spots:
                    raise BookingConflictError(f"Only {availability.available_spots} spots remaining")
                
                return True
                
        except BookingConflictError as e:
            # Broadcast updated availability to all clients
            RealTimeService.broadcast_availability_update(game_slot.id)
            raise e
```

## Data Models

### Database Schema

```sql
-- Core User Management
-- Users (Django built-in)
-- Customers (extends User)
-- CafeOwners (extends User)  
-- TapNexSuperusers (extends User)

-- Game and Slot Management
-- Games (replaces GamingStations)
-- GameSlots (auto-generated + custom slots)
-- SlotAvailability (real-time capacity tracking)

-- Booking System
-- Bookings (with hybrid booking support)
-- Payments (transaction records)

-- System Configuration
-- SystemSettings (cafe configuration)
-- CommissionSettings (TapNex revenue model)
```

### Relationships
- Customer → Bookings (One-to-Many)
- Game → GameSlots (One-to-Many)
- Game → Bookings (One-to-Many)
- GameSlot → Bookings (One-to-Many)
- GameSlot → SlotAvailability (One-to-One)
- Booking → Payment (One-to-One)
- TapNexSuperuser → CommissionSettings (One-to-One)

## User Interface Design

### Design System

#### Color Palette
- **Primary**: Gaming-themed colors (neon blue, electric purple)
- **Secondary**: Dark theme with accent colors
- **Neutral**: Grays for backgrounds and text
- **Status**: Green (available), Red (booked), Yellow (maintenance)

#### Typography
- **Headings**: Bold, modern sans-serif
- **Body**: Clean, readable font
- **UI Elements**: Consistent sizing and spacing

#### Components
- **Buttons**: Rounded corners, hover effects, loading states
- **Cards**: Gaming station cards with images and specs
- **Forms**: Clean, validated inputs with error states
- **Modals**: Booking confirmation, payment processing

### Responsive Design

#### Breakpoints (Tailwind CSS)
- **Mobile**: 320px - 768px
- **Tablet**: 768px - 1024px
- **Desktop**: 1024px+

#### Layout Strategy
- **Mobile-first** approach
- **Flexible grid** system
- **Touch-optimized** buttons and interactions
- **Collapsible navigation** for mobile

### Page Layouts

#### Customer Dashboard
```
┌─────────────────────────────────────┐
│ Header (Logo, User Menu)            │
├─────────────────────────────────────┤
│ Welcome Section (Avatar, Name)      │
├─────────────────────────────────────┤
│ Available Games                     │
│ ┌─────────────────────────────────┐ │
│ │ 8-Ball Pool    [Private ₹400]  │ │
│ │ 2 spots left   [Shared ₹100]   │ │
│ ├─────────────────────────────────┤ │
│ │ Table Tennis   [Private ₹300]  │ │
│ │ Available      [Shared ₹75]    │ │
│ ├─────────────────────────────────┤ │
│ │ PS4 Console 1  [Private ₹200]  │ │
│ │ Available      (Single only)   │ │
│ └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│ My Bookings                         │
│ ┌─────────────────────────────────┐ │
│ │ Upcoming | Past | Cancelled    │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

#### Cafe Owner Dashboard
```
┌─────────────────────────────────────┐
│ Header (Logo, Owner Menu)           │
├─────────────────────────────────────┤
│ Today's Overview                    │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐│
│ │Revenue  │ │Bookings │ │Capacity ││
│ │₹2,400   │ │12/20    │ │85% Used ││
│ └─────────┘ └─────────┘ └─────────┘│
├─────────────────────────────────────┤
│ Live Game Status                    │
│ ┌─────────────────────────────────┐ │
│ │ Game        | Capacity | Status │ │
│ │ 8-Ball Pool | 3/4 spots| Shared│ │
│ │ Table Tennis| Private  | Booked│ │
│ │ PS4 Console | Available| Free  │ │
│ └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│ Quick Actions                       │
│ [Add Game] [Custom Slots] [Analytics]│
└─────────────────────────────────────┘
```

#### TapNex Superuser Dashboard
```
┌─────────────────────────────────────┐
│ Header (TapNex Logo, Admin Menu)    │
├─────────────────────────────────────┤
│ Revenue Overview                    │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐│
│ │Gross    │ │Commission│ │Net      ││
│ │₹15,000  │ │₹1,500    │ │₹13,500  ││
│ └─────────┘ └─────────┘ └─────────┘│
├─────────────────────────────────────┤
│ Commission Settings                 │
│ ┌─────────────────────────────────┐ │
│ │ Rate: 10% | Platform Fee: ₹50  │ │
│ │ [Update Settings]               │ │
│ └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│ Cafe Owner Management               │
│ │ Owner: Harsha | Status: Active  │ │
│ │ [Reset Password] [View Details] │ │
└─────────────────────────────────────┘
```

#### Hybrid Booking Interface
```
┌─────────────────────────────────────┐
│ 8-Ball Pool - Sunday 2:00-3:00 PM  │
├─────────────────────────────────────┤
│ Choose Your Booking Option:         │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 🏆 PRIVATE BOOKING              │ │
│ │ Book entire table for your group│ │
│ │ Capacity: 4 players             │ │
│ │ Price: ₹400/hour                │ │
│ │ [Book Private] ✨               │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 👥 SHARED BOOKING               │ │
│ │ Play with other customers       │ │
│ │ Available spots: 4/4            │ │
│ │ Price: ₹100/person/hour         │ │
│ │ Spots: [1] [2] [3] [4]         │ │
│ │ [Book Shared] 🤝               │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

## Error Handling

### Client-Side Error Handling
- **Form Validation**: Real-time validation with clear error messages
- **Network Errors**: Retry mechanisms and offline indicators
- **Payment Failures**: Clear error messages with alternative options

### Server-Side Error Handling
- **Database Errors**: Graceful degradation and error logging
- **Payment Processing**: Proper error codes and user feedback
- **Authentication Errors**: Secure error messages without information leakage

### Error Logging
- **Structured Logging**: JSON format for easy parsing
- **Error Tracking**: Integration with error monitoring service
- **User Activity**: Audit trail for bookings and payments

## Slot Generation and Management

### Automatic Slot Generation Algorithm

#### Game Schedule Configuration
```python
# Example: 8-Ball Pool configuration
game_config = {
    'name': '8-Ball Pool',
    'opening_time': '11:00',  # 11 AM
    'closing_time': '23:00',  # 11 PM
    'slot_duration_minutes': 60,  # 1 hour slots
    'available_days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
    'capacity': 4,
    'booking_type': 'HYBRID',
    'private_price': 400.00,
    'shared_price': 100.00
}

# Generated slots for one day:
# 11:00-12:00, 12:00-13:00, 13:00-14:00, ..., 22:00-23:00
# Total: 12 slots per day × 7 days = 84 slots per week
```

#### Custom Slot Addition
```python
# Example: Weekend late-night slots
custom_slots = [
    {
        'game': '8-Ball Pool',
        'date': '2024-01-06',  # Saturday
        'start_time': '23:00',  # 11 PM
        'end_time': '05:00',    # 5 AM (next day)
        'is_custom': True
    }
]
```

### Slot Management Workflow

1. **Initial Setup**: Owner creates game with schedule settings
2. **Auto-Generation**: System generates slots for next 30 days
3. **Daily Regeneration**: System adds new slots for upcoming dates
4. **Custom Addition**: Owner can add temporary slots for special events
5. **Booking Preservation**: Existing bookings are preserved during regeneration

### Capacity Management

#### Real-time Availability Tracking
```javascript
// Frontend real-time updates
const slotAvailability = {
    gameSlotId: 123,
    totalCapacity: 4,
    bookedSpots: 2,
    isPrivateBooked: false,
    availableSpots: 2,
    canBookPrivate: false,  // Because shared bookings exist
    canBookShared: true
};

// Real-time subscription
supabase
    .channel('slot-availability')
    .on('postgres_changes', {
        event: 'UPDATE',
        schema: 'public',
        table: 'slot_availability'
    }, (payload) => {
        updateSlotDisplay(payload.new);
    })
    .subscribe();
```

## Testing Strategy

### Unit Testing
- **Models**: Test data validation and business logic
- **Views**: Test authentication and authorization
- **Services**: Test payment processing and booking logic

### Integration Testing
- **API Endpoints**: Test complete request/response cycles
- **Database Operations**: Test complex queries and transactions
- **Third-party Services**: Mock external services for testing

### End-to-End Testing
- **User Flows**: Test complete booking process
- **Payment Integration**: Test payment success/failure scenarios
- **Real-time Features**: Test live updates and conflict resolution

### Performance Testing
- **Load Testing**: Simulate concurrent bookings
- **Database Performance**: Optimize queries and indexing
- **Frontend Performance**: Measure page load times and interactions

## Security Considerations

### Authentication Security
- **OAuth Security**: Proper token handling and validation
- **Session Management**: Secure session configuration
- **Password Security**: Strong password requirements and hashing

### Data Protection
- **Input Validation**: Sanitize all user inputs
- **SQL Injection**: Use parameterized queries
- **XSS Protection**: Escape output and use CSP headers

### Payment Security
- **PCI Compliance**: Follow payment card industry standards
- **Secure Transmission**: HTTPS for all payment-related communications
- **Data Minimization**: Store minimal payment information

## Deployment Architecture

### Vercel Configuration
- **Build Settings**: Optimized for Django static files
- **Environment Variables**: Secure configuration management
- **Domain Configuration**: Custom domain setup
- **SSL/TLS**: Automatic HTTPS certificate management

### Database Configuration
- **Supabase Setup**: Connection pooling and security rules
- **Backup Strategy**: Automated daily backups
- **Migration Strategy**: Safe database schema updates

### Monitoring and Logging
- **Application Monitoring**: Performance and error tracking
- **Database Monitoring**: Query performance and connection health
- **User Analytics**: Booking patterns and system usage