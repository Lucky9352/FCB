from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Customer, CafeOwner
from .decorators import customer_required, cafe_owner_required
from booking.models import GamingStation, Booking


@customer_required
def customer_dashboard(request):
    """Customer dashboard view with booking history and available stations"""
    # Ensure user has customer profile
    if not hasattr(request.user, 'customer_profile'):
        # Create customer profile if it doesn't exist (for Google OAuth users)
        Customer.objects.get_or_create(user=request.user)
    
    customer = request.user.customer_profile
    now = timezone.now()
    
    # Get customer's bookings
    recent_bookings = customer.bookings.all().order_by('-created_at')[:5]
    upcoming_bookings = customer.bookings.filter(
        start_time__gt=now,
        status__in=['CONFIRMED', 'PENDING']
    ).order_by('start_time')[:3]
    
    # Get current booking (if any)
    current_booking = customer.bookings.filter(
        start_time__lte=now,
        end_time__gte=now,
        status='IN_PROGRESS'
    ).first()
    
    # Get available gaming stations for quick booking
    available_stations = GamingStation.objects.filter(
        is_active=True,
        is_maintenance=False
    ).order_by('station_type', 'name')[:6]
    
    # Get booking statistics
    total_bookings = customer.bookings.count()
    completed_bookings = customer.bookings.filter(status='COMPLETED').count()
    
    context = {
        'customer': customer,
        'user': request.user,
        'recent_bookings': recent_bookings,
        'upcoming_bookings': upcoming_bookings,
        'current_booking': current_booking,
        'available_stations': available_stations,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'now': now,
    }
    return render(request, 'authentication/customer_dashboard.html', context)


@cafe_owner_required
def cafe_owner_dashboard(request):
    """Cafe owner dashboard view"""
    cafe_owner = request.user.cafe_owner_profile
    
    context = {
        'cafe_owner': cafe_owner,
        'user': request.user,
    }
    return render(request, 'authentication/cafe_owner_dashboard.html', context)