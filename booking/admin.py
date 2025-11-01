from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import GamingStation, Booking, BookingHistory, Game, GameSlot, SlotAvailability


@admin.register(GamingStation)
class GamingStationAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'station_type', 
        'hourly_rate', 
        'availability_status', 
        'current_booking_info',
        'created_at'
    ]
    list_filter = ['station_type', 'is_active', 'is_maintenance', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'station_type', 'description')
        }),
        ('Pricing', {
            'fields': ('hourly_rate',)
        }),
        ('Availability', {
            'fields': ('is_active', 'is_maintenance')
        }),
        ('Technical Specifications', {
            'fields': ('specifications',),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def availability_status(self, obj):
        if obj.is_maintenance:
            return format_html('<span style="color: orange;">🔧 Maintenance</span>')
        elif obj.is_active:
            return format_html('<span style="color: green;">✅ Available</span>')
        else:
            return format_html('<span style="color: red;">❌ Inactive</span>')
    availability_status.short_description = 'Status'
    
    def current_booking_info(self, obj):
        current_booking = obj.get_current_booking()
        if current_booking:
            return format_html(
                '<span style="color: blue;">🎮 {}</span>',
                current_booking.customer.user.get_full_name() or current_booking.customer.user.username
            )
        return format_html('<span style="color: gray;">Free</span>')
    current_booking_info.short_description = 'Current Booking'


class BookingHistoryInline(admin.TabularInline):
    model = BookingHistory
    extra = 0
    readonly_fields = ['previous_status', 'new_status', 'changed_by', 'reason', 'timestamp']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'customer_info',
        'gaming_station',
        'start_time',
        'end_time',
        'duration_display',
        'total_amount',
        'status_display',
        'created_at'
    ]
    list_filter = [
        'status',
        'gaming_station__station_type',
        'is_walk_in',
        'start_time',
        'created_at'
    ]
    search_fields = [
        'customer__user__username',
        'customer__user__email',
        'customer__user__first_name',
        'customer__user__last_name',
        'gaming_station__name',
        'payment_id'
    ]
    readonly_fields = [
        'id',
        'duration_hours',
        'created_at',
        'updated_at'
    ]
    date_hierarchy = 'start_time'
    inlines = [BookingHistoryInline]
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('id', 'customer', 'gaming_station')
        }),
        ('Time Information', {
            'fields': ('start_time', 'end_time', 'duration_hours')
        }),
        ('Pricing Information', {
            'fields': ('hourly_rate', 'total_amount')
        }),
        ('Status and Payment', {
            'fields': ('status', 'payment_id', 'payment_status')
        }),
        ('Additional Information', {
            'fields': ('notes', 'is_walk_in'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def customer_info(self, obj):
        customer_name = obj.customer.user.get_full_name() or obj.customer.user.username
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:authentication_customer_change', args=[obj.customer.pk]),
            customer_name
        )
    customer_info.short_description = 'Customer'
    
    def duration_display(self, obj):
        hours = obj.duration_hours
        if hours < 1:
            minutes = int(hours * 60)
            return f"{minutes} min"
        return f"{hours:.1f} hrs"
    duration_display.short_description = 'Duration'
    
    def status_display(self, obj):
        status_colors = {
            'PENDING': 'orange',
            'CONFIRMED': 'green',
            'IN_PROGRESS': 'blue',
            'COMPLETED': 'gray',
            'CANCELLED': 'red',
            'NO_SHOW': 'darkred',
        }
        color = status_colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        # Track status changes
        if change:
            try:
                old_obj = Booking.objects.get(pk=obj.pk)
                if old_obj.status != obj.status:
                    BookingHistory.objects.create(
                        booking=obj,
                        previous_status=old_obj.status,
                        new_status=obj.status,
                        changed_by=request.user,
                        reason=f"Status changed via admin by {request.user.username}"
                    )
            except Booking.DoesNotExist:
                pass
        
        super().save_model(request, obj, form, change)


@admin.register(BookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'booking',
        'previous_status',
        'new_status',
        'changed_by',
        'timestamp'
    ]
    list_filter = ['new_status', 'previous_status', 'timestamp']
    search_fields = [
        'booking__customer__user__username',
        'booking__gaming_station__name',
        'changed_by__username'
    ]
    readonly_fields = ['booking', 'previous_status', 'new_status', 'changed_by', 'timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

# NEW HYBRID BOOKING SYSTEM ADMIN

class GameSlotInline(admin.TabularInline):
    model = GameSlot
    extra = 0
    readonly_fields = ['date', 'start_time', 'end_time', 'is_custom', 'created_at']
    fields = ['date', 'start_time', 'end_time', 'is_custom', 'is_active']
    can_delete = True
    
    def has_add_permission(self, request, obj=None):
        return False  # Slots are auto-generated


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'booking_type_display',
        'capacity',
        'schedule_display',
        'pricing_display',
        'availability_status',
        'total_slots',
        'created_at'
    ]
    list_filter = ['booking_type', 'is_active', 'capacity', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'total_slots']
    inlines = [GameSlotInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'description', 'image')
        }),
        ('Capacity and Booking Type', {
            'fields': ('capacity', 'booking_type'),
            'description': 'Set capacity (max players) and booking type (single=private only, hybrid=private+shared)'
        }),
        ('Schedule Settings', {
            'fields': ('opening_time', 'closing_time', 'slot_duration_minutes', 'available_days'),
            'description': 'Configure when this game is available and slot duration'
        }),
        ('Pricing', {
            'fields': ('private_price', 'shared_price'),
            'description': 'Private price = full capacity booking, Shared price = per person (hybrid games only)'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'total_slots'),
            'classes': ('collapse',)
        }),
    )
    
    def booking_type_display(self, obj):
        if obj.booking_type == 'SINGLE':
            return format_html('<span style="color: blue;">🔒 Private Only</span>')
        else:
            return format_html('<span style="color: green;">🤝 Private + Shared</span>')
    booking_type_display.short_description = 'Booking Type'
    
    def schedule_display(self, obj):
        days_count = len(obj.available_days)
        return format_html(
            '{} - {} ({} min slots)<br><small>{} days/week</small>',
            obj.opening_time.strftime('%H:%M'),
            obj.closing_time.strftime('%H:%M'),
            obj.slot_duration_minutes,
            days_count
        )
    schedule_display.short_description = 'Schedule'
    
    def pricing_display(self, obj):
        if obj.booking_type == 'SINGLE':
            return format_html('Private: <strong>₹{}</strong>', obj.private_price)
        else:
            return format_html(
                'Private: <strong>₹{}</strong><br>Shared: <strong>₹{}/person</strong>',
                obj.private_price,
                obj.shared_price or 0
            )
    pricing_display.short_description = 'Pricing'
    
    def availability_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✅ Active</span>')
        else:
            return format_html('<span style="color: red;">❌ Inactive</span>')
    availability_status.short_description = 'Status'
    
    def total_slots(self, obj):
        return obj.slots.count()
    total_slots.short_description = 'Total Slots'
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # New game created
            # Generate initial slots
            from .slot_generator import SlotGenerator
            from datetime import date, timedelta
            
            start_date = date.today()
            end_date = start_date + timedelta(days=30)
            slots_created = SlotGenerator.generate_slots_for_game(obj, start_date, end_date)
            
            self.message_user(
                request,
                f'Game created successfully! Generated {slots_created} initial slots for the next 30 days.'
            )


class SlotAvailabilityInline(admin.StackedInline):
    model = SlotAvailability
    extra = 0
    readonly_fields = ['total_capacity', 'booked_spots', 'available_spots', 'can_book_private', 'can_book_shared']
    fields = ['total_capacity', 'booked_spots', 'is_private_booked', 'available_spots', 'can_book_private', 'can_book_shared']
    
    def available_spots(self, obj):
        return obj.available_spots
    available_spots.short_description = 'Available Spots'
    
    def can_book_private(self, obj):
        return '✅ Yes' if obj.can_book_private else '❌ No'
    can_book_private.short_description = 'Can Book Private'
    
    def can_book_shared(self, obj):
        return '✅ Yes' if obj.can_book_shared else '❌ No'
    can_book_shared.short_description = 'Can Book Shared'


@admin.register(GameSlot)
class GameSlotAdmin(admin.ModelAdmin):
    list_display = [
        'game',
        'date',
        'time_display',
        'slot_type',
        'availability_display',
        'booking_count',
        'is_active'
    ]
    list_filter = ['game', 'date', 'is_custom', 'is_active']
    search_fields = ['game__name']
    readonly_fields = ['created_at', 'booking_count']
    date_hierarchy = 'date'
    inlines = [SlotAvailabilityInline]
    
    fieldsets = (
        ('Slot Information', {
            'fields': ('game', 'date', 'start_time', 'end_time')
        }),
        ('Type and Status', {
            'fields': ('is_custom', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'booking_count'),
            'classes': ('collapse',)
        }),
    )
    
    def time_display(self, obj):
        return f"{obj.start_time} - {obj.end_time}"
    time_display.short_description = 'Time'
    
    def slot_type(self, obj):
        if obj.is_custom:
            return format_html('<span style="color: orange;">🔧 Custom</span>')
        else:
            return format_html('<span style="color: blue;">🤖 Auto</span>')
    slot_type.short_description = 'Type'
    
    def availability_display(self, obj):
        try:
            availability = obj.availability
            if availability.is_private_booked:
                return format_html('<span style="color: red;">🔒 Private Booked</span>')
            elif availability.booked_spots > 0:
                return format_html(
                    '<span style="color: orange;">👥 {}/{} Shared</span>',
                    availability.booked_spots,
                    availability.total_capacity
                )
            else:
                return format_html('<span style="color: green;">✅ Available</span>')
        except SlotAvailability.DoesNotExist:
            return format_html('<span style="color: gray;">❓ No Tracking</span>')
    availability_display.short_description = 'Availability'
    
    def booking_count(self, obj):
        return obj.bookings.count()
    booking_count.short_description = 'Bookings'


@admin.register(SlotAvailability)
class SlotAvailabilityAdmin(admin.ModelAdmin):
    list_display = [
        'game_slot',
        'capacity_display',
        'booking_status',
        'private_available',
        'shared_available'
    ]
    list_filter = ['is_private_booked', 'game_slot__game', 'game_slot__date']
    search_fields = ['game_slot__game__name']
    readonly_fields = ['available_spots', 'can_book_private', 'can_book_shared']
    
    fieldsets = (
        ('Slot Information', {
            'fields': ('game_slot',)
        }),
        ('Capacity Tracking', {
            'fields': ('total_capacity', 'booked_spots', 'available_spots')
        }),
        ('Booking Status', {
            'fields': ('is_private_booked', 'can_book_private', 'can_book_shared')
        }),
    )
    
    def capacity_display(self, obj):
        return f"{obj.booked_spots}/{obj.total_capacity}"
    capacity_display.short_description = 'Capacity (Booked/Total)'
    
    def booking_status(self, obj):
        if obj.is_private_booked:
            return format_html('<span style="color: red;">🔒 Private</span>')
        elif obj.booked_spots > 0:
            return format_html('<span style="color: orange;">👥 Shared</span>')
        else:
            return format_html('<span style="color: green;">✅ Free</span>')
    booking_status.short_description = 'Status'
    
    def private_available(self, obj):
        return '✅' if obj.can_book_private else '❌'
    private_available.short_description = 'Private OK'
    
    def shared_available(self, obj):
        return '✅' if obj.can_book_shared else '❌'
    shared_available.short_description = 'Shared OK'