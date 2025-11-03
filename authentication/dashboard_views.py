from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Sum, Count, Avg, F
from django.db.models.functions import TruncDate, TruncHour
from django.http import JsonResponse
from datetime import datetime, timedelta, date
from decimal import Decimal
from .models import Customer, CafeOwner
from .decorators import customer_required, cafe_owner_required
from booking.models import Game, Booking, GameSlot, SlotAvailability
import json


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
    
    # Get available games for quick booking
    available_games = Game.objects.filter(
        is_active=True
    ).order_by('name')  # Show ALL games, not just 6
    
    # Get booking statistics
    total_bookings = customer.bookings.count()
    completed_bookings = customer.bookings.filter(status='COMPLETED').count()
    
    context = {
        'customer': customer,
        'user': request.user,
        'recent_bookings': recent_bookings,
        'upcoming_bookings': upcoming_bookings,
        'current_booking': current_booking,
        'available_games': available_games,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'now': now,
    }
    return render(request, 'authentication/customer_dashboard.html', context)


@cafe_owner_required
def cafe_owner_dashboard(request):
    """Redirect to overview page"""
    return redirect('authentication:owner_overview')


# ============================================
# SECTION 1: OVERVIEW / HOME
# ============================================

@cafe_owner_required
def owner_overview(request):
    """Owner overview dashboard with real-time stats and timeline"""
    cafe_owner = request.user.cafe_owner_profile
    now = timezone.now()
    today = now.date()
    yesterday = today - timedelta(days=1)
    
    # Today's Stats
    todays_bookings = Booking.objects.filter(
        start_time__date=today
    )
    
    todays_revenue = todays_bookings.filter(
        payment_status='PAID'
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    active_sessions = Booking.objects.filter(
        start_time__lte=now,
        end_time__gte=now,
        status='IN_PROGRESS'
    ).count()
    
    total_bookings_today = todays_bookings.count()
    
    # Available stations right now
    all_games = Game.objects.filter(is_active=True)
    occupied_games = Booking.objects.filter(
        start_time__lte=now,
        end_time__gte=now,
        status='IN_PROGRESS'
    ).values_list('game_id', flat=True)
    available_stations = all_games.count() - len(set(occupied_games))
    
    # Pending payments
    pending_payments = Booking.objects.filter(
        payment_status='PENDING'
    ).count()
    
    # Total customers today
    customers_today = todays_bookings.values('customer').distinct().count()
    
    # Yesterday's revenue for comparison
    yesterdays_revenue = Booking.objects.filter(
        start_time__date=yesterday,
        payment_status='PAID'
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    # Calculate percentage change
    if yesterdays_revenue > 0:
        revenue_change = ((todays_revenue - yesterdays_revenue) / yesterdays_revenue) * 100
    else:
        revenue_change = 100 if todays_revenue > 0 else 0
    
    # Today's Timeline (hourly bookings)
    timeline_data = []
    for hour in range(24):
        hour_start = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        hour_end = hour_start + timedelta(hours=1)
        
        bookings_in_hour = Booking.objects.filter(
            start_time__gte=hour_start,
            start_time__lt=hour_end
        ).select_related('game', 'customer')
        
        timeline_data.append({
            'hour': hour,
            'time': hour_start.strftime('%I %p'),
            'bookings': list(bookings_in_hour.values(
                'id', 'game__name', 'customer__user__first_name', 
                'customer__user__last_name', 'status', 'start_time', 'end_time'
            ))
        })
    
    # Upcoming bookings (next 3)
    upcoming_bookings = Booking.objects.filter(
        start_time__gt=now,
        status__in=['CONFIRMED', 'PENDING']
    ).select_related('game', 'customer').order_by('start_time')[:3]
    
    # Recent alerts
    alerts = []
    
    # Cancelled bookings today
    cancelled_today = todays_bookings.filter(status='CANCELLED').count()
    if cancelled_today > 0:
        alerts.append({
            'type': 'warning',
            'icon': 'fa-exclamation-triangle',
            'message': f'{cancelled_today} booking(s) cancelled today',
            'time': 'Today'
        })
    
    # Failed payments
    failed_payments = Booking.objects.filter(
        payment_status='FAILED',
        created_at__date=today
    ).count()
    if failed_payments > 0:
        alerts.append({
            'type': 'danger',
            'icon': 'fa-credit-card',
            'message': f'{failed_payments} failed payment(s)',
            'time': 'Today'
        })
    
    # Games under maintenance
    maintenance_games = Game.objects.filter(is_active=False).count()
    if maintenance_games > 0:
        alerts.append({
            'type': 'info',
            'icon': 'fa-wrench',
            'message': f'{maintenance_games} game(s) under maintenance',
            'time': 'Current'
        })
    
    context = {
        'cafe_owner': cafe_owner,
        'todays_revenue': todays_revenue,
        'revenue_change': revenue_change,
        'active_sessions': active_sessions,
        'total_bookings_today': total_bookings_today,
        'available_stations': available_stations,
        'pending_payments': pending_payments,
        'customers_today': customers_today,
        'timeline_data': timeline_data,
        'upcoming_bookings': upcoming_bookings,
        'alerts': alerts,
        'now': now,
    }
    return render(request, 'authentication/owner_overview.html', context)


# ============================================
# SECTION 2: BOOKINGS
# ============================================

@cafe_owner_required
def owner_bookings(request):
    """Bookings management section"""
    cafe_owner = request.user.cafe_owner_profile
    now = timezone.now()
    
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    game_filter = request.GET.get('game', 'all')
    date_filter = request.GET.get('date', 'all')
    search_query = request.GET.get('search', '')
    
    # Base queryset
    bookings = Booking.objects.all().select_related('game', 'customer', 'customer__user')
    
    # Apply filters
    if status_filter != 'all':
        bookings = bookings.filter(status=status_filter.upper())
    
    if game_filter != 'all':
        bookings = bookings.filter(game_id=game_filter)
    
    if date_filter == 'today':
        bookings = bookings.filter(start_time__date=now.date())
    elif date_filter == 'week':
        week_start = now.date() - timedelta(days=now.weekday())
        bookings = bookings.filter(start_time__date__gte=week_start)
    elif date_filter == 'month':
        bookings = bookings.filter(start_time__year=now.year, start_time__month=now.month)
    
    if search_query:
        bookings = bookings.filter(
            Q(id__icontains=search_query) |
            Q(customer__user__first_name__icontains=search_query) |
            Q(customer__user__last_name__icontains=search_query) |
            Q(customer__user__email__icontains=search_query)
        )
    
    # Order by start time (newest first)
    bookings = bookings.order_by('-start_time')
    
    # Categorize bookings
    confirmed_bookings = bookings.filter(status='CONFIRMED', start_time__gt=now).count()
    in_progress_bookings = bookings.filter(status='IN_PROGRESS').count()
    completed_bookings = bookings.filter(status='COMPLETED').count()
    cancelled_bookings = bookings.filter(status='CANCELLED').count()
    pending_payment_bookings = bookings.filter(payment_status='PENDING').count()
    no_shows = bookings.filter(status='NO_SHOW').count()
    
    # Get all games for filter dropdown
    all_games = Game.objects.filter(is_active=True).order_by('name')
    
    # Calendar data for the month
    calendar_data = []
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = (month_start + timedelta(days=32)).replace(day=1)
    
    monthly_bookings = Booking.objects.filter(
        start_time__gte=month_start,
        start_time__lt=next_month
    ).values('start_time__date').annotate(count=Count('id'))
    
    for booking_day in monthly_bookings:
        calendar_data.append({
            'date': booking_day['start_time__date'].isoformat(),
            'count': booking_day['count']
        })
    
    context = {
        'cafe_owner': cafe_owner,
        'bookings': bookings[:50],  # Limit to 50 for performance
        'confirmed_bookings': confirmed_bookings,
        'in_progress_bookings': in_progress_bookings,
        'completed_bookings': completed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'pending_payment_bookings': pending_payment_bookings,
        'no_shows': no_shows,
        'all_games': all_games,
        'calendar_data': json.dumps(calendar_data),
        'status_filter': status_filter,
        'game_filter': game_filter,
        'date_filter': date_filter,
        'search_query': search_query,
        'now': now,
    }
    return render(request, 'authentication/owner_bookings.html', context)


# ============================================
# SECTION 3: GAMES & STATIONS
# ============================================

@cafe_owner_required
def owner_games(request):
    """Games and stations management section"""
    cafe_owner = request.user.cafe_owner_profile
    now = timezone.now()
    today = now.date()
    
    # Get all games
    games = Game.objects.all().order_by('name')
    
    # Add today's stats to each game
    for game in games:
        game.todays_bookings = Booking.objects.filter(
            game=game,
            start_time__date=today
        ).count()
        
        game.todays_revenue = Booking.objects.filter(
            game=game,
            start_time__date=today,
            payment_status='PAID'
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
        
        # Check if currently occupied
        game.is_occupied = Booking.objects.filter(
            game=game,
            start_time__lte=now,
            end_time__gte=now,
            status='IN_PROGRESS'
        ).exists()
    
    # Station status board
    active_games = games.filter(is_active=True)
    inactive_games = games.filter(is_active=False)
    
    # Game analytics
    most_popular_game = Booking.objects.filter(
        start_time__date=today
    ).values('game__name').annotate(
        count=Count('id')
    ).order_by('-count').first()
    
    context = {
        'cafe_owner': cafe_owner,
        'games': games,
        'active_games_count': active_games.count(),
        'inactive_games_count': inactive_games.count(),
        'total_games': games.count(),
        'most_popular_game': most_popular_game,
        'now': now,
    }
    return render(request, 'authentication/owner_games.html', context)


# ============================================
# SECTION 4: CUSTOMERS
# ============================================

@cafe_owner_required
def owner_customers(request):
    """Customers CRM section"""
    cafe_owner = request.user.cafe_owner_profile
    now = timezone.now()
    
    # Get filter parameters
    filter_type = request.GET.get('filter', 'all')
    search_query = request.GET.get('search', '')
    
    # Base queryset
    customers = Customer.objects.all().select_related('user')
    
    # Add stats to each customer
    customers = customers.annotate(
        total_bookings=Count('bookings'),
        total_spent=Sum('bookings__total_amount', filter=Q(bookings__payment_status='PAID')),
        last_booking_date=Count('bookings__start_time')
    )
    
    # Apply filters
    if filter_type == 'vip':
        customers = customers.filter(total_spent__gte=1000)  # VIP threshold
    elif filter_type == 'frequent':
        customers = customers.filter(total_bookings__gte=5)
    elif filter_type == 'new':
        week_ago = now - timedelta(days=7)
        customers = customers.filter(user__date_joined__gte=week_ago)
    elif filter_type == 'at_risk':
        thirty_days_ago = now - timedelta(days=30)
        customers = customers.filter(bookings__start_time__lt=thirty_days_ago).distinct()
    elif filter_type == 'inactive':
        ninety_days_ago = now - timedelta(days=90)
        customers = customers.exclude(bookings__start_time__gte=ninety_days_ago)
    
    if search_query:
        customers = customers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    # Order by total spent
    customers = customers.order_by('-total_spent')
    
    # Customer segments count
    total_customers = Customer.objects.count()
    vip_customers = Customer.objects.annotate(
        total_spent=Sum('bookings__total_amount', filter=Q(bookings__payment_status='PAID'))
    ).filter(total_spent__gte=1000).count()
    
    new_customers = Customer.objects.filter(
        user__date_joined__gte=now - timedelta(days=7)
    ).count()
    
    context = {
        'cafe_owner': cafe_owner,
        'customers': customers[:50],  # Limit for performance
        'total_customers': total_customers,
        'vip_customers': vip_customers,
        'new_customers': new_customers,
        'filter_type': filter_type,
        'search_query': search_query,
    }
    return render(request, 'authentication/owner_customers.html', context)


# ============================================
# SECTION 5: REVENUE & FINANCE
# ============================================

@cafe_owner_required
def owner_revenue(request):
    """Revenue and finance section"""
    cafe_owner = request.user.cafe_owner_profile
    now = timezone.now()
    today = now.date()
    
    # Time period filter
    period = request.GET.get('period', 'month')
    
    if period == 'today':
        start_date = today
        end_date = today
    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif period == 'month':
        start_date = today.replace(day=1)
        end_date = today
    elif period == 'year':
        start_date = today.replace(month=1, day=1)
        end_date = today
    else:
        start_date = today.replace(day=1)
        end_date = today
    
    # Total revenue
    total_revenue = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        payment_status='PAID'
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    # Revenue by payment method
    revenue_by_method = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        payment_status='PAID'
    ).values('payment_method').annotate(
        total=Sum('total_amount'),
        count=Count('id')
    )
    
    # Revenue by game
    revenue_by_game = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        payment_status='PAID'
    ).values('game__name').annotate(
        total=Sum('total_amount'),
        count=Count('id')
    ).order_by('-total')[:10]
    
    # Revenue trend (daily for the period)
    revenue_trend = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        payment_status='PAID'
    ).annotate(
        date=TruncDate('start_time')
    ).values('date').annotate(
        revenue=Sum('total_amount')
    ).order_by('date')
    
    # Payment management
    pending_payments = Booking.objects.filter(
        payment_status='PENDING'
    ).select_related('game', 'customer').order_by('-created_at')[:20]
    
    failed_payments = Booking.objects.filter(
        payment_status='FAILED'
    ).select_related('game', 'customer').order_by('-created_at')[:20]
    
    # Commission tracking (assuming 10% platform commission)
    commission_rate = Decimal('0.10')
    platform_commission = total_revenue * commission_rate
    net_revenue = total_revenue - platform_commission
    
    context = {
        'cafe_owner': cafe_owner,
        'total_revenue': total_revenue,
        'platform_commission': platform_commission,
        'net_revenue': net_revenue,
        'commission_rate': commission_rate * 100,
        'revenue_by_method': revenue_by_method,
        'revenue_by_game': revenue_by_game,
        'revenue_trend': list(revenue_trend),
        'pending_payments': pending_payments,
        'failed_payments': failed_payments,
        'period': period,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'authentication/owner_revenue.html', context)


# ============================================
# SECTION 6: REPORTS & ANALYTICS
# ============================================

@cafe_owner_required
def owner_reports(request):
    """Reports and analytics section"""
    cafe_owner = request.user.cafe_owner_profile
    now = timezone.now()
    today = now.date()
    
    # Date range filter
    days = int(request.GET.get('days', 30))
    start_date = today - timedelta(days=days)
    
    # Booking analytics
    bookings_trend = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=today
    ).annotate(
        date=TruncDate('start_time')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    # Peak hours heatmap
    peak_hours = Booking.objects.filter(
        start_time__date__gte=start_date
    ).annotate(
        hour=TruncHour('start_time')
    ).values('hour').annotate(
        count=Count('id')
    ).order_by('hour')
    
    # Average booking value
    avg_booking_value = Booking.objects.filter(
        start_time__date__gte=start_date,
        payment_status='PAID'
    ).aggregate(avg=Avg('total_amount'))['avg'] or Decimal('0.00')
    
    # Cancellation analysis
    total_bookings = Booking.objects.filter(start_time__date__gte=start_date).count()
    cancelled_bookings = Booking.objects.filter(
        start_time__date__gte=start_date,
        status='CANCELLED'
    ).count()
    cancellation_rate = (cancelled_bookings / total_bookings * 100) if total_bookings > 0 else 0
    
    # Customer analytics
    new_customers = Customer.objects.filter(
        user__date_joined__date__gte=start_date
    ).count()
    
    total_customers = Customer.objects.count()
    
    # Customer lifetime value
    customer_ltv = Customer.objects.annotate(
        ltv=Sum('bookings__total_amount', filter=Q(bookings__payment_status='PAID'))
    ).aggregate(avg_ltv=Avg('ltv'))['avg_ltv'] or Decimal('0.00')
    
    # Utilization rate
    all_games = Game.objects.filter(is_active=True).count()
    total_possible_slots = all_games * days * 12  # Assuming 12 hours per day
    total_bookings_count = Booking.objects.filter(start_time__date__gte=start_date).count()
    utilization_rate = (total_bookings_count / total_possible_slots * 100) if total_possible_slots > 0 else 0
    
    # Revenue comparison (current period vs previous period)
    previous_start_date = start_date - timedelta(days=days)
    previous_end_date = start_date - timedelta(days=1)
    
    current_revenue = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=today,
        payment_status='PAID'
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    previous_revenue = Booking.objects.filter(
        start_time__date__gte=previous_start_date,
        start_time__date__lte=previous_end_date,
        payment_status='PAID'
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    revenue_change = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0
    
    context = {
        'cafe_owner': cafe_owner,
        'bookings_trend': list(bookings_trend),
        'peak_hours': list(peak_hours),
        'avg_booking_value': avg_booking_value,
        'total_bookings': total_bookings,
        'cancelled_bookings': cancelled_bookings,
        'cancellation_rate': cancellation_rate,
        'new_customers': new_customers,
        'total_customers': total_customers,
        'customer_ltv': customer_ltv,
        'utilization_rate': utilization_rate,
        'current_revenue': current_revenue,
        'previous_revenue': previous_revenue,
        'revenue_change': revenue_change,
        'days': days,
        'start_date': start_date,
        'end_date': today,
    }
    return render(request, 'authentication/owner_reports.html', context)