from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.cache import cache
from datetime import datetime, timedelta
from authentication.decorators import customer_required
from .models import GamingStation, Booking, Notification, Game
from .notifications import NotificationService, InAppNotification
from authentication.models import Customer
import json
import logging

logger = logging.getLogger(__name__)


@customer_required
def booking_selection(request):
    """Booking selection interface with calendar/grid view"""
    # Get all active gaming stations
    stations = GamingStation.objects.filter(
        is_active=True,
        is_maintenance=False
    ).order_by('station_type', 'name')
    
    # Get selected date (default to today)
    selected_date = request.GET.get('date', timezone.now().date().isoformat())
    try:
        selected_date = datetime.fromisoformat(selected_date).date()
    except ValueError:
        selected_date = timezone.now().date()
    
    # Generate time slots for the selected date (9 AM to 11 PM)
    time_slots = []
    start_hour = 9
    end_hour = 23
    
    for hour in range(start_hour, end_hour):
        time_slots.append({
            'time': f"{hour:02d}:00",
            'display': f"{hour % 12 or 12}:00 {'AM' if hour < 12 else 'PM'}",
            'datetime': timezone.make_aware(
                datetime.combine(selected_date, datetime.min.time().replace(hour=hour)),
                timezone=timezone.get_current_timezone()
            )
        })
    
    # Get existing bookings for the selected date
    existing_bookings = Booking.objects.filter(
        start_time__date=selected_date,
        status__in=['CONFIRMED', 'IN_PROGRESS', 'PENDING']
    ).select_related('gaming_station')
    
    # Create availability matrix
    availability = {}
    for station in stations:
        availability[station.id] = {}
        for slot in time_slots:
            # Check if this time slot is available for this station
            slot_end = slot['datetime'] + timedelta(hours=1)
            is_available = not existing_bookings.filter(
                gaming_station=station,
                start_time__lt=slot_end,
                end_time__gt=slot['datetime']
            ).exists()
            
            availability[station.id][slot['time']] = {
                'available': is_available,
                'datetime': slot['datetime'],
                'end_datetime': slot_end
            }
    
    context = {
        'stations': stations,
        'time_slots': time_slots,
        'selected_date': selected_date,
        'availability': availability,
        'today': timezone.now().date(),
    }
    
    return render(request, 'booking/selection.html', context)


@customer_required
def booking_create(request):
    """Create a new booking"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            station_id = data.get('station_id')
            start_time = data.get('start_time')
            duration = int(data.get('duration', 1))  # Default 1 hour
            
            # Validate inputs
            if not all([station_id, start_time]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Get station
            station = get_object_or_404(GamingStation, id=station_id, is_active=True)
            
            # Parse start time
            start_datetime = timezone.make_aware(datetime.fromisoformat(start_time))
            end_datetime = start_datetime + timedelta(hours=duration)
            
            # Validate booking time is in the future
            if start_datetime <= timezone.now():
                return JsonResponse({'error': 'Booking time must be in the future'}, status=400)
            
            # Check availability
            if not station.is_available_at_time(start_datetime, end_datetime):
                return JsonResponse({'error': 'Time slot is not available'}, status=400)
            
            # Get customer
            customer = request.user.customer_profile
            
            # Create booking
            booking = Booking.objects.create(
                customer=customer,
                gaming_station=station,
                start_time=start_datetime,
                end_time=end_datetime,
                hourly_rate=station.hourly_rate,
                status='PENDING'
            )
            
            return JsonResponse({
                'success': True,
                'booking_id': str(booking.id),
                'total_amount': str(booking.total_amount),
                'redirect_url': f'/booking/confirm/{booking.id}/'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@customer_required
def booking_confirm(request, booking_id):
    """Booking confirmation page"""
    booking = get_object_or_404(
        Booking, 
        id=booking_id, 
        customer=request.user.customer_profile,
        status='PENDING'
    )
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'booking/confirm.html', context)


@customer_required
def get_availability(request):
    """AJAX endpoint to get real-time availability"""
    date_str = request.GET.get('date')
    station_id = request.GET.get('station_id')
    
    try:
        selected_date = datetime.fromisoformat(date_str).date()
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    # Generate time slots
    time_slots = []
    for hour in range(9, 23):  # 9 AM to 11 PM
        time_slots.append({
            'time': f"{hour:02d}:00",
            'datetime': timezone.make_aware(
                datetime.combine(selected_date, datetime.min.time().replace(hour=hour)),
                timezone=timezone.get_current_timezone()
            )
        })
    
    if station_id:
        # Get availability for specific station
        try:
            station = GamingStation.objects.get(id=station_id, is_active=True)
        except GamingStation.DoesNotExist:
            return JsonResponse({'error': 'Station not found'}, status=404)
        
        availability = {}
        for slot in time_slots:
            slot_end = slot['datetime'] + timedelta(hours=1)
            is_available = station.is_available_at_time(slot['datetime'], slot_end)
            availability[slot['time']] = is_available
        
        return JsonResponse({'availability': availability})
    else:
        # Get availability for all stations
        stations = GamingStation.objects.filter(is_active=True, is_maintenance=False)
        availability = {}
        
        for station in stations:
            availability[str(station.id)] = {}
            for slot in time_slots:
                slot_end = slot['datetime'] + timedelta(hours=1)
                is_available = station.is_available_at_time(slot['datetime'], slot_end)
                availability[str(station.id)][slot['time']] = is_available
        
        return JsonResponse({'availability': availability})


@customer_required
def my_bookings(request):
    """Customer's booking history and management"""
    customer = request.user.customer_profile
    
    # Get bookings with filters
    status_filter = request.GET.get('status', 'all')
    
    bookings = customer.bookings.all().order_by('-created_at')
    
    if status_filter != 'all':
        bookings = bookings.filter(status=status_filter.upper())
    
    # Categorize bookings
    now = timezone.now()
    
    # Separate old and new bookings for filtering
    upcoming = []
    past = []
    current = None
    
    for booking in bookings:
        start_dt = booking.start_datetime
        end_dt = booking.end_datetime
        
        if not start_dt or not end_dt:
            continue  # Skip bookings without valid times
        
        # Check for current booking
        if start_dt <= now <= end_dt and booking.status == 'IN_PROGRESS':
            if not current:  # Take the first one
                current = booking
        # Check for upcoming (any status, as long as it's in the future)
        elif start_dt > now:
            upcoming.append(booking)
        # Past bookings (end time has passed)
        elif end_dt < now:
            past.append(booking)
    
    # Sort lists
    upcoming.sort(key=lambda b: b.start_datetime)
    past.sort(key=lambda b: b.start_datetime, reverse=True)
    
    # Get all bookings for "All" tab
    all_bookings = list(bookings)
    
    context = {
        'bookings': all_bookings,  # For "All Bookings" tab
        'upcoming_bookings': upcoming,
        'current_booking': current,
        'past_bookings': past,
        'status_filter': status_filter,
        'now': now,  # For template comparisons
    }
    
    return render(request, 'booking/my_bookings.html', context)


@customer_required
def booking_details(request, booking_id):
    """View booking details for any confirmed/completed booking"""
    booking = get_object_or_404(
        Booking, 
        id=booking_id, 
        customer=request.user.customer_profile
    )
    
    # Redirect to confirmation page if still pending
    if booking.status == 'PENDING':
        return redirect('booking:hybrid_booking_confirm', booking_id=booking_id)
    
    context = {
        'booking': booking,
        'is_hybrid': booking.game.booking_type == 'HYBRID',
        'is_private': booking.booking_type == 'PRIVATE',
        'is_shared': booking.booking_type == 'SHARED',
    }
    
    return render(request, 'booking/booking_details.html', context)


@customer_required
def booking_success(request, booking_id):
    """
    Booking success page with animations and notifications
    SECURITY: Only accessible for CONFIRMED bookings with verified payment
    """
    booking = get_object_or_404(
        Booking, 
        id=booking_id, 
        customer=request.user.customer_profile
    )
    
    # SECURITY CHECK: Prevent access to success page without payment verification
    if booking.status != 'CONFIRMED':
        messages.error(request, 'This booking is not confirmed. Please complete the payment first.')
        return redirect('booking:hybrid_booking_confirm', booking_id=booking_id)
    
    # SECURITY CHECK: Verify payment exists (either razorpay_payment_id or old payment_id)
    if not booking.razorpay_payment_id and not booking.payment_id:
        messages.error(request, 'Payment verification required.')
        return redirect('booking:hybrid_booking_confirm', booking_id=booking_id)
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'booking/success.html', context)


@customer_required
def simulate_payment(request, booking_id):
    """Simulate payment processing for demo purposes"""
    if request.method == 'POST':
        booking = get_object_or_404(
            Booking, 
            id=booking_id, 
            customer=request.user.customer_profile,
            status='PENDING'
        )
        
        try:
            # Simulate payment processing
            booking.status = 'CONFIRMED'
            booking.payment_id = f'pay_{timezone.now().strftime("%Y%m%d%H%M%S")}'
            booking.payment_status = 'completed'
            booking.save()
            
            # Send confirmation email
            NotificationService.send_booking_confirmation_email(booking)
            
            # Create in-app notification
            InAppNotification.notify_booking_confirmed(booking)
            
            # Add success message
            messages.success(request, 'Payment successful! Your booking has been confirmed.')
            
            return JsonResponse({
                'success': True,
                'redirect_url': f'/booking/success/{booking.id}/'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@customer_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    if request.method == 'POST':
        booking = get_object_or_404(
            Booking, 
            id=booking_id, 
            customer=request.user.customer_profile,
            status__in=['PENDING', 'CONFIRMED']
        )
        
        try:
            # Update booking status
            booking.status = 'CANCELLED'
            booking.save()
            
            # Send cancellation email
            NotificationService.send_booking_cancellation_email(booking)
            
            # Create in-app notification
            InAppNotification.notify_booking_cancelled(booking)
            
            # Add success message
            messages.success(request, 'Booking cancelled successfully.')
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@customer_required
def get_notifications(request):
    """Get user's notifications with caching for performance"""
    user_id = request.user.id
    cache_key = f'notifications_user_{user_id}'
    
    # Try to get from cache first (10 second cache)
    cached_data = cache.get(cache_key)
    if cached_data:
        return JsonResponse(cached_data)
    
    # Optimized query - get unread notifications with single database hit
    notifications = request.user.notifications.filter(
        is_read=False
    ).select_related('booking').order_by('-created_at')[:10]
    
    # Convert to list to get count without extra query
    notifications_list = list(notifications)
    
    notification_data = []
    for notification in notifications_list:
        notification_data.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'type': notification.notification_type,
            'created_at': notification.created_at.isoformat(),
            'booking_id': str(notification.booking.id) if notification.booking else None
        })
    
    response_data = {
        'notifications': notification_data,
        'unread_count': len(notifications_list)
    }
    
    # Cache for 10 seconds to reduce database load
    cache.set(cache_key, response_data, 10)
    
    return JsonResponse(response_data)


@customer_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    if request.method == 'POST':
        try:
            notification = get_object_or_404(
                Notification,
                id=notification_id,
                user=request.user
            )
            notification.mark_as_read()
            
            # Invalidate cache when notification is marked as read
            cache_key = f'notifications_user_{request.user.id}'
            cache.delete(cache_key)
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# NEW HYBRID BOOKING VIEWS

@customer_required
def game_selection(request):
    """Game selection interface with hybrid booking options - PUBLIC ACCESS"""
    from .models import Game
    from .booking_service import BookingService
    from .auto_slot_generator import auto_generate_slots_all_games
    from datetime import date, timedelta
    
    # Ensure slots are available (runs in background, doesn't block)
    auto_generate_slots_all_games(async_mode=True)
    
    # Get all active games
    games = Game.objects.filter(is_active=True).order_by('name')
    
    # Get selected date (default to today)
    selected_date = request.GET.get('date', timezone.now().date().isoformat())
    try:
        selected_date = datetime.fromisoformat(selected_date).date()
    except ValueError:
        selected_date = timezone.now().date()
    
    # Get available slots for each game
    games_with_availability = []
    for game in games:
        available_slots = BookingService.get_available_slots(
            game, 
            date_from=selected_date,
            date_to=selected_date
        )
        
        games_with_availability.append({
            'game': game,
            'available_slots': available_slots,
            'has_availability': len(available_slots) > 0
        })
    
    context = {
        'games_with_availability': games_with_availability,
        'selected_date': selected_date,
        'today': timezone.now().date(),
        'date_range': [selected_date + timedelta(days=i) for i in range(7)]  # Next 7 days
    }
    
    return render(request, 'booking/game_selection.html', context)


@customer_required
def hybrid_booking_create(request):
    """Create a hybrid booking (private or shared) with enhanced validation"""
    if request.method == 'POST':
        try:
            print(f"📥 Booking request received")
            print(f"User: {request.user}")
            print(f"Authenticated: {request.user.is_authenticated}")
            print(f"Request body: {request.body[:200]}")
            
            # Check if user is authenticated
            if not request.user.is_authenticated:
                print("❌ User not authenticated")
                return JsonResponse({
                    'success': False,
                    'error': 'Authentication required',
                    'details': 'Please log in to create a booking',
                    'redirect_url': f'/accounts/login/?next={request.path}'
                }, status=401)
            
            # Check if user has customer profile
            if not hasattr(request.user, 'customer_profile'):
                print(f"❌ User {request.user} has no customer_profile")
                return JsonResponse({
                    'success': False,
                    'error': 'Customer profile required',
                    'details': 'Only customers can create bookings',
                }, status=403)
            
            # Parse JSON body
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as e:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON',
                    'details': f'Failed to parse request body: {str(e)}'
                }, status=400)
            
            game_slot_id = data.get('game_slot_id')
            booking_type = data.get('booking_type')  # 'PRIVATE' or 'SHARED'
            spots_requested = int(data.get('spots_requested', 1))
            
            # Validate inputs
            if not all([game_slot_id, booking_type]):
                logger.warning(f"Missing required fields for booking request. Parsed data: game_slot_id={game_slot_id}, booking_type={booking_type}, spots_requested={spots_requested}")
                return JsonResponse({
                    'success': False,
                    'error': 'Missing required fields',
                    'details': 'Game slot ID and booking type are required',
                    'parsed': {
                        'game_slot_id': game_slot_id,
                        'booking_type': booking_type,
                        'spots_requested': spots_requested
                    }
                }, status=400)
            
            if booking_type not in ['PRIVATE', 'SHARED']:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid booking type',
                    'details': 'Booking type must be PRIVATE or SHARED'
                }, status=400)
            
            if spots_requested < 1:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid spots requested',
                    'details': 'Must request at least 1 spot'
                }, status=400)
            
            # Get game slot
            from .models import GameSlot
            game_slot = get_object_or_404(GameSlot, id=game_slot_id, is_active=True)
            
            # Get customer
            customer = request.user.customer_profile
            
            # Get current booking options to validate request
            from .booking_service import BookingService
            available_options = BookingService.get_booking_options(game_slot)
            
            # Find the requested booking option
            requested_option = None
            for option in available_options:
                if option['type'] == booking_type and option['available']:
                    requested_option = option
                    break
            
            if not requested_option:
                return JsonResponse({
                    'success': False,
                    'error': 'Booking option not available',
                    'details': f'{booking_type} booking is not available for this slot',
                    'available_options': available_options
                }, status=400)
            
            # Validate spots for shared booking
            if booking_type == 'SHARED':
                max_spots = requested_option.get('max_spots_per_booking', requested_option['available_spots'])
                if spots_requested > max_spots:
                    return JsonResponse({
                        'success': False,
                        'error': 'Too many spots requested',
                        'details': f'Maximum {max_spots} spots can be booked at once',
                        'max_spots_allowed': max_spots
                    }, status=400)
            
            # Create booking using BookingService
            booking = BookingService.create_booking(
                customer=customer,
                game_slot=game_slot,
                booking_type=booking_type,
                spots_requested=spots_requested
            )
            
            print(f"✅ Booking created: {booking.id}")
            
            return JsonResponse({
                'success': True,
                'booking_id': str(booking.id),
                'booking_type': booking.booking_type,
                'spots_booked': booking.spots_booked,
                'price_per_spot': str(booking.price_per_spot),
                'total_amount': str(booking.total_amount),
                'game_name': booking.game.name,
                'slot_time': f"{booking.game_slot.start_time.strftime('%H:%M')} - {booking.game_slot.end_time.strftime('%H:%M')}",
                'slot_date': booking.game_slot.date.isoformat(),
                'redirect_url': f'/booking/games/confirm/{booking.id}/',
                'message': f'Successfully booked {booking.spots_booked} spot{"s" if booking.spots_booked > 1 else ""} for {booking.game.name}'
            })
            
        except ValidationError as e:
            print(f"❌ Validation Error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Booking validation failed',
                'details': str(e),
                'error_type': 'validation'
            }, status=400)
        except Exception as e:
            print(f"❌ System Error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'error': 'Booking creation failed',
                'details': str(e),
                'error_type': 'system'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@customer_required
def hybrid_booking_confirm(request, booking_id):
    """Hybrid booking confirmation page"""
    booking = get_object_or_404(
        Booking, 
        id=booking_id, 
        customer=request.user.customer_profile,
        status='PENDING'
    )
    
    # Get booking options that were available
    from .booking_service import BookingService
    available_options = BookingService.get_booking_options(booking.game_slot)
    
    # Calculate max spots that can be booked
    max_additional_spots = 0
    if booking.booking_type == 'SHARED':
        current_availability = booking.game_slot.availability
        # Max spots = current spots + available spots (capped at 4 total per booking)
        max_additional_spots = min(
            current_availability.available_spots,
            4 - booking.spots_booked  # Cap at 4 total spots per booking
        )
    
    context = {
        'booking': booking,
        'available_options': available_options,
        'is_hybrid': booking.game.booking_type == 'HYBRID',
        'is_private': booking.booking_type == 'PRIVATE',
        'is_shared': booking.booking_type == 'SHARED',
        'max_total_spots': min(booking.spots_booked + max_additional_spots, 4) if booking.booking_type == 'SHARED' else booking.spots_booked,
        'can_modify_spots': booking.booking_type == 'SHARED' and max_additional_spots > 0,
    }
    
    return render(request, 'booking/hybrid_confirm.html', context)


@customer_required
def update_booking_spots(request, booking_id):
    """Update the number of spots for a shared booking"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    try:
        import json
        from .booking_service import BookingService
        from django.db import transaction
        
        data = json.loads(request.body)
        new_spots = int(data.get('spots', 0))
        
        # Get booking
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            customer=request.user.customer_profile,
            status='PENDING'
        )
        
        # Validate it's a shared booking
        if booking.booking_type != 'SHARED':
            return JsonResponse({
                'success': False,
                'error': 'Can only modify spots for shared bookings'
            }, status=400)
        
        # Validate new spots
        if new_spots < 1:
            return JsonResponse({
                'success': False,
                'error': 'Must book at least 1 spot'
            }, status=400)
        
        if new_spots > 4:
            return JsonResponse({
                'success': False,
                'error': 'Cannot book more than 4 spots per booking'
            }, status=400)
        
        # Check if spots are available
        with transaction.atomic():
            availability = booking.game_slot.availability
            
            # Calculate spot difference
            spot_difference = new_spots - booking.spots_booked
            
            if spot_difference > 0:
                # Increasing spots - check availability
                if spot_difference > availability.available_spots:
                    return JsonResponse({
                        'success': False,
                        'error': f'Only {availability.available_spots} additional spots available'
                    }, status=400)
            
            # Update booking
            old_spots = booking.spots_booked
            booking.spots_booked = new_spots
            booking.subtotal = booking.price_per_spot * new_spots
            booking.total_amount = booking.subtotal + booking.platform_fee
            
            # Update availability
            if spot_difference > 0:
                availability.booked_spots += spot_difference
            else:
                availability.booked_spots -= abs(spot_difference)
            
            availability.save()
            booking.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Booking updated from {old_spots} to {new_spots} spot(s)',
                'new_total': str(booking.total_amount),
                'new_subtotal': str(booking.subtotal),
                'new_spots': new_spots
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except ValueError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid spot number'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@customer_required
def get_slot_availability(request, game_slot_id):
    """AJAX endpoint to get real-time slot availability with detailed information"""
    try:
        from .models import GameSlot
        from .booking_service import BookingService
        
        game_slot = get_object_or_404(GameSlot, id=game_slot_id, is_active=True)
        
        # Get current booking options with detailed information
        booking_options = BookingService.get_booking_options(game_slot)
        
        # Get booking type restrictions
        restrictions = BookingService.get_booking_type_restrictions(game_slot)
        
        # Get existing bookings for this slot
        existing_bookings = game_slot.bookings.filter(
            status__in=['CONFIRMED', 'IN_PROGRESS', 'PENDING']
        ).select_related('customer__user')
        
        booking_details = []
        for booking in existing_bookings:
            booking_details.append({
                'booking_type': booking.booking_type,
                'spots_booked': booking.spots_booked,
                'customer_name': booking.customer.user.get_full_name() or booking.customer.user.username,
                'status': booking.status,
                'created_at': booking.created_at.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'game_slot_id': str(game_slot_id),
            'game_info': {
                'id': str(game_slot.game.id),
                'name': game_slot.game.name,
                'description': game_slot.game.description,
                'capacity': game_slot.game.capacity,
                'booking_type': game_slot.game.booking_type,
                'private_price': float(game_slot.game.private_price),
                'shared_price': float(game_slot.game.shared_price) if game_slot.game.shared_price else None
            },
            'slot_info': {
                'date': game_slot.date.isoformat(),
                'start_time': game_slot.start_time.strftime('%H:%M'),
                'end_time': game_slot.end_time.strftime('%H:%M'),
                'duration_minutes': game_slot.game.slot_duration_minutes,
                'is_custom': game_slot.is_custom
            },
            'availability': {
                'total_capacity': restrictions['total_capacity'],
                'booked_spots': restrictions['booked_spots'],
                'available_spots': restrictions['available_spots'],
                'can_book_private': restrictions['can_book_private'],
                'can_book_shared': restrictions['can_book_shared'],
                'is_private_locked': restrictions['is_private_locked'],
                'is_shared_locked': restrictions['is_shared_locked']
            },
            'booking_options': booking_options,
            'existing_bookings': booking_details,
            'restrictions': restrictions,
            'timestamp': timezone.now().isoformat(),
            'is_past_slot': game_slot.start_datetime <= timezone.now()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'error_type': 'system'
        }, status=400)


@customer_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    if request.method == 'POST':
        try:
            booking = get_object_or_404(
                Booking, 
                id=booking_id, 
                customer=request.user.customer_profile
            )
            
            if booking.status not in ['PENDING', 'CONFIRMED']:
                return JsonResponse({'error': 'Booking cannot be cancelled'}, status=400)
            
            # Cancel using BookingService
            from .booking_service import BookingService
            BookingService.cancel_booking(booking)
            
            messages.success(request, 'Booking cancelled successfully')
            
            return JsonResponse({
                'success': True,
                'message': 'Booking cancelled successfully'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def game_detail(request, game_id):
    """
    Game detail page - PUBLIC ACCESS
    Shows full game information - slots loaded via AJAX for performance
    Users can view without login, but need to login to book
    
    OPTIMIZED VERSION: Only loads game details, slots fetched via API
    """
    from datetime import timedelta
    
    # Get the game (optimized query)
    game = get_object_or_404(Game, id=game_id, is_active=True)
    
    # Get selected date (default to today)
    selected_date = request.GET.get('date', timezone.now().date().isoformat())
    try:
        selected_date = datetime.fromisoformat(selected_date).date()
    except ValueError:
        selected_date = timezone.now().date()
    
    # Generate date range for navigation (7 days)
    date_range = [selected_date + timedelta(days=i) for i in range(7)]
    
    # Lightweight context - no slot processing on initial load
    context = {
        'game': game,
        'selected_date': selected_date,
        'date_range': date_range,
        'today': timezone.now().date(),
        'is_authenticated': request.user.is_authenticated,
        'use_ajax_loading': True,  # Flag to enable AJAX loading in template
    }
    
    return render(request, 'booking/game_detail.html', context)

