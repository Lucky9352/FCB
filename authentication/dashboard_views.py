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
    """Customer dashboard view with booking history and available stations - OPTIMIZED"""
    # Ensure user has customer profile
    if not hasattr(request.user, 'customer_profile'):
        # Create customer profile if it doesn't exist (for Google OAuth users)
        Customer.objects.get_or_create(user=request.user)
    
    customer = request.user.customer_profile
    now = timezone.now()
    today = now.date()
    
    # Optimized query with select_related to avoid N+1 queries
    all_customer_bookings = customer.bookings.select_related('game', 'game_slot')
    
    # Recent bookings (last 5) - use slicing to limit query
    recent_bookings = all_customer_bookings.order_by('-created_at')[:5]
    
    # Upcoming bookings (future confirmed/pending/in_progress bookings)
    upcoming_bookings = all_customer_bookings.filter(
        game_slot__date__gte=today,
        status__in=['CONFIRMED', 'PENDING', 'IN_PROGRESS']
    ).order_by('game_slot__date', 'game_slot__start_time')[:3]
    
    # Get current active booking (if any)
    current_booking = all_customer_bookings.filter(
        game_slot__date=today,
        status='IN_PROGRESS'
    ).first()
    
    # Get available games (optimized query, NO CACHE for real-time updates)
    available_games = Game.objects.filter(is_active=True).only(
        'id', 'name', 'description', 'image', 'booking_type'
    ).order_by('name')
    
    # Use database aggregation for statistics (single query, NO CACHE)
    stats = all_customer_bookings.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        pending=Count('id', filter=Q(status='PENDING')),
        confirmed=Count('id', filter=Q(status='CONFIRMED')),
        total_spent=Sum('total_amount', filter=Q(payment_status='PAID'))
    )
    
    # Calculate total hours efficiently
    completed_with_duration = customer.bookings.filter(
        status='COMPLETED'
    ).select_related('game').only('id', 'game__id', 'game__slot_duration_minutes')
    
    total_hours = sum(
        booking.game.slot_duration_minutes / 60 
        for booking in completed_with_duration
    ) if completed_with_duration.exists() else 0
    
    context = {
        'customer': customer,
        'user': request.user,
        'recent_bookings': recent_bookings,
        'upcoming_bookings': upcoming_bookings,
        'current_booking': current_booking,
        'available_games': available_games,
        'total_bookings': stats['total'] or 0,
        'completed_bookings': stats['completed'] or 0,
        'pending_bookings': stats['pending'] or 0,
        'confirmed_bookings': stats['confirmed'] or 0,
        'total_spent': stats['total_spent'] or Decimal('0.00'),
        'total_hours': int(total_hours),
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
    """Owner overview dashboard with real-time stats and timeline - OPTIMIZED FOR REAL-TIME"""
    cafe_owner = request.user.cafe_owner_profile
    now = timezone.now()
    today = now.date()
    yesterday = today - timedelta(days=1)
    
    # Real-time stats with single aggregate query (NO CACHE)
    todays_stats = Booking.objects.filter(
        start_time__date=today
    ).aggregate(
        revenue=Sum('owner_payout', filter=Q(payment_status='PAID')),
        total_bookings=Count('id'),
        active_sessions=Count('id', filter=Q(
            start_time__lte=now,
            end_time__gte=now,
            status='IN_PROGRESS'
        )),
        pending_payments=Count('id', filter=Q(payment_status='PENDING')),
        customers_today=Count('customer', distinct=True),
        cancelled_today=Count('id', filter=Q(status='CANCELLED'))
    )
    
    todays_revenue = todays_stats['revenue'] or Decimal('0.00')
    total_bookings_today = todays_stats['total_bookings'] or 0
    active_sessions = todays_stats['active_sessions'] or 0
    pending_payments = todays_stats['pending_payments'] or 0
    customers_today = todays_stats['customers_today'] or 0
    cancelled_today = todays_stats['cancelled_today'] or 0
    
    # Available stations (real-time)
    all_games_count = Game.objects.filter(is_active=True).count()
    occupied_games_count = Booking.objects.filter(
        start_time__lte=now,
        end_time__gte=now,
        status='IN_PROGRESS'
    ).values('game_id').distinct().count()
    available_stations = all_games_count - occupied_games_count
    
    # Yesterday's revenue for comparison (single query)
    yesterdays_revenue = Booking.objects.filter(
        start_time__date=yesterday,
        payment_status='PAID'
    ).aggregate(total=Sum('owner_payout'))['total'] or Decimal('0.00')
    
    # Calculate percentage change
    if yesterdays_revenue > 0:
        revenue_change = ((todays_revenue - yesterdays_revenue) / yesterdays_revenue) * 100
    else:
        revenue_change = 100 if todays_revenue > 0 else 0
    
    # Today's Timeline (optimized - single query with grouping)
    hourly_bookings = Booking.objects.filter(
        start_time__date=today
    ).select_related('game', 'customer__user').order_by('start_time')
    
    # Group bookings by hour in Python (more efficient than 24 separate queries)
    timeline_data = []
    bookings_by_hour = {}
    for booking in hourly_bookings:
        hour = booking.start_time.hour
        if hour not in bookings_by_hour:
            bookings_by_hour[hour] = []
        bookings_by_hour[hour].append({
            'id': str(booking.id),
            'game__name': booking.game.name,
            'customer__user__first_name': booking.customer.user.first_name,
            'customer__user__last_name': booking.customer.user.last_name,
            'status': booking.status,
            'start_time': booking.start_time,
            'end_time': booking.end_time
        })
    
    for hour in range(24):
        hour_start = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        timeline_data.append({
            'hour': hour,
            'time': hour_start.strftime('%I %p'),
            'bookings': bookings_by_hour.get(hour, [])
        })
    
    # Upcoming bookings (real-time with select_related)
    upcoming_bookings = Booking.objects.filter(
        start_time__gt=now,
        status__in=['CONFIRMED', 'PENDING']
    ).select_related('game', 'customer__user').order_by('start_time')[:3]
    
    # Recent alerts (real-time)
    alerts = []
    
    if cancelled_today > 0:
        alerts.append({
            'type': 'warning',
            'icon': 'fa-exclamation-triangle',
            'message': f'{cancelled_today} booking(s) cancelled today',
            'time': 'Today'
        })
    
    # Failed payments (single query)
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
    
    # Games under maintenance (single query)
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
    """Bookings management section - OPTIMIZED FOR REAL-TIME"""
    cafe_owner = request.user.cafe_owner_profile
    now = timezone.now()
    
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    game_filter = request.GET.get('game', 'all')
    date_filter = request.GET.get('date', 'all')
    search_query = request.GET.get('search', '')
    
    # Auto-update booking statuses only for relevant bookings (performance optimization)
    from booking.booking_service import auto_update_bookings_status
    
    bookings_to_check = Booking.objects.filter(
        status__in=['PENDING', 'CONFIRMED', 'IN_PROGRESS']
    ).select_related('game_slot').only('id', 'status', 'game_slot__start_time', 'game_slot__end_time')
    
    auto_update_bookings_status(bookings_to_check)
    
    # Optimized base queryset with select_related (NO CACHE for real-time)
    bookings = Booking.objects.select_related('game', 'customer__user', 'game_slot')
    
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
    
    # Use single aggregate query for counts (real-time stats)
    stats = bookings.aggregate(
        confirmed=Count('id', filter=Q(status='CONFIRMED', start_time__gt=now)),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        completed=Count('id', filter=Q(status='COMPLETED')),
        cancelled=Count('id', filter=Q(status='CANCELLED')),
        pending_payment=Count('id', filter=Q(payment_status='PENDING')),
        no_shows=Count('id', filter=Q(status='NO_SHOW'))
    )
    
    # Get games list (real-time, optimized query)
    all_games = Game.objects.filter(is_active=True).only('id', 'name').order_by('name')
    
    # Calendar data for the month (optimized query)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = (month_start + timedelta(days=32)).replace(day=1)
    
    monthly_bookings = Booking.objects.filter(
        start_time__gte=month_start,
        start_time__lt=next_month
    ).values('start_time__date').annotate(count=Count('id'))
    
    calendar_data = [
        {
            'date': booking_day['start_time__date'].isoformat(),
            'count': booking_day['count']
        }
        for booking_day in monthly_bookings
    ]
    
    context = {
        'cafe_owner': cafe_owner,
        'bookings': bookings[:50],  # Limit to 50 for performance
        'confirmed_bookings': stats['confirmed'] or 0,
        'in_progress_bookings': stats['in_progress'] or 0,
        'completed_bookings': stats['completed'] or 0,
        'cancelled_bookings': stats['cancelled'] or 0,
        'pending_payment_bookings': stats['pending_payment'] or 0,
        'no_shows': stats['no_shows'] or 0,
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
    """Games and stations management section - OPTIMIZED"""
    cafe_owner = request.user.cafe_owner_profile
    now = timezone.now()
    today = now.date()
    
    # Get all games with optimized query
    games = Game.objects.all().order_by('name')
    
    # Get all today's bookings in one query
    todays_bookings = Booking.objects.filter(
        start_time__date=today
    ).values('game_id', 'status', 'payment_status').annotate(
        count=Count('id'),
        revenue=Sum('total_amount', filter=Q(payment_status='PAID'))
    )
    
    # Create lookup dictionaries for O(1) access
    bookings_by_game = {b['game_id']: b for b in todays_bookings}
    
    # Get currently occupied games in one query
    occupied_game_ids = set(Booking.objects.filter(
        start_time__lte=now,
        end_time__gte=now,
        status='IN_PROGRESS'
    ).values_list('game_id', flat=True))
    
    # Add stats to games efficiently (no additional queries)
    for game in games:
        game_stats = bookings_by_game.get(game.id, {})
        game.todays_bookings = game_stats.get('count', 0)
        game.todays_revenue = game_stats.get('revenue') or Decimal('0.00')
        game.is_occupied = game.id in occupied_game_ids
    
    # Station status board (use already loaded games)
    active_games_count = sum(1 for g in games if g.is_active)
    inactive_games_count = len(games) - active_games_count
    
    # Game analytics (single query)
    most_popular_game = Booking.objects.filter(
        start_time__date=today
    ).values('game__name').annotate(
        count=Count('id')
    ).order_by('-count').first()
    
    context = {
        'cafe_owner': cafe_owner,
        'games': games,
        'active_games_count': active_games_count,
        'inactive_games_count': inactive_games_count,
        'total_games': len(games),
        'most_popular_game': most_popular_game,
        'now': now,
    }
    return render(request, 'authentication/owner_games.html', context)


# ============================================
# SECTION 4: CUSTOMERS
# ============================================

@cafe_owner_required
def owner_customers(request):
    """Customers CRM section - OPTIMIZED FOR REAL-TIME"""
    cafe_owner = request.user.cafe_owner_profile
    now = timezone.now()
    
    # Get filter parameters
    filter_type = request.GET.get('filter', 'all')
    search_query = request.GET.get('search', '')
    
    # Optimized base queryset with select_related
    customers = Customer.objects.select_related('user')
    
    # Add stats to each customer - Use owner_payout for revenue (single query with annotations)
    customers = customers.annotate(
        total_bookings=Count('bookings'),
        total_spent=Sum('bookings__owner_payout', filter=Q(bookings__payment_status='PAID')),
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
    
    # Real-time customer segment counts (NO CACHE for instant updates)
    segment_counts = {
        'total': Customer.objects.count(),
        'vip': Customer.objects.annotate(
            total_spent=Sum('bookings__owner_payout', filter=Q(bookings__payment_status='PAID'))
        ).filter(total_spent__gte=1000).count(),
        'new': Customer.objects.filter(
            user__date_joined__gte=now - timedelta(days=7)
        ).count()
    }
    
    context = {
        'cafe_owner': cafe_owner,
        'customers': customers[:50],  # Limit for performance
        'total_customers': segment_counts['total'],
        'vip_customers': segment_counts['vip'],
        'new_customers': segment_counts['new'],
        'filter_type': filter_type,
        'search_query': search_query,
    }
    return render(request, 'authentication/owner_customers.html', context)


# ============================================
# SECTION 5: REVENUE & FINANCE
# ============================================

@cafe_owner_required
def owner_revenue(request):
    """Revenue and finance section - Shows owner's earnings after commission"""
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
    
    # Total revenue for owner (after commission) - Use owner_payout
    total_revenue = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        payment_status='PAID'
    ).aggregate(total=Sum('owner_payout'))['total'] or Decimal('0.00')
    
    # Gross revenue (before commission) for reference
    gross_revenue = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        payment_status='PAID'
    ).aggregate(total=Sum('subtotal'))['total'] or Decimal('0.00')
    
    # Total commission deducted
    total_commission = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        payment_status='PAID'
    ).aggregate(total=Sum('commission_amount'))['total'] or Decimal('0.00')
    
    # Revenue by payment method (using owner_payout)
    revenue_by_method = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        payment_status='PAID'
    ).values('payment_method').annotate(
        total=Sum('owner_payout'),
        count=Count('id')
    )
    
    # Revenue by game (using owner_payout)
    revenue_by_game = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        payment_status='PAID'
    ).values('game__name').annotate(
        total=Sum('owner_payout'),
        count=Count('id')
    ).order_by('-total')[:10]
    
    # Revenue trend (daily for the period) - owner_payout
    revenue_trend = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        payment_status='PAID'
    ).annotate(
        date=TruncDate('start_time')
    ).values('date').annotate(
        revenue=Sum('owner_payout')
    ).order_by('date')
    
    # Payment management
    pending_payments = Booking.objects.filter(
        payment_status='PENDING'
    ).select_related('game', 'customer').order_by('-created_at')[:20]
    
    failed_payments = Booking.objects.filter(
        payment_status='FAILED'
    ).select_related('game', 'customer').order_by('-created_at')[:20]
    
    # Commission tracking - Fixed 7% commission rate
    commission_rate = Decimal('7.00')
    
    context = {
        'cafe_owner': cafe_owner,
        'total_revenue': total_revenue,  # Owner's net revenue after commission
        'gross_revenue': gross_revenue,  # Before commission
        'platform_commission': total_commission,  # Total commission deducted
        'net_revenue': total_revenue,  # Same as total_revenue (already net)
        'commission_rate': commission_rate,
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
    
    # Average booking value - Use owner_payout
    avg_booking_value = Booking.objects.filter(
        start_time__date__gte=start_date,
        payment_status='PAID'
    ).aggregate(avg=Avg('owner_payout'))['avg'] or Decimal('0.00')
    
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
    
    # Customer lifetime value - Use owner_payout
    customer_ltv = Customer.objects.annotate(
        ltv=Sum('bookings__owner_payout', filter=Q(bookings__payment_status='PAID'))
    ).aggregate(avg_ltv=Avg('ltv'))['avg_ltv'] or Decimal('0.00')
    
    # Utilization rate
    all_games = Game.objects.filter(is_active=True).count()
    total_possible_slots = all_games * days * 12  # Assuming 12 hours per day
    total_bookings_count = Booking.objects.filter(start_time__date__gte=start_date).count()
    utilization_rate = (total_bookings_count / total_possible_slots * 100) if total_possible_slots > 0 else 0
    
    # Revenue comparison (current period vs previous period) - Use owner_payout
    previous_start_date = start_date - timedelta(days=days)
    previous_end_date = start_date - timedelta(days=1)
    
    current_revenue = Booking.objects.filter(
        start_time__date__gte=start_date,
        start_time__date__lte=today,
        payment_status='PAID'
    ).aggregate(total=Sum('owner_payout'))['total'] or Decimal('0.00')
    
    previous_revenue = Booking.objects.filter(
        start_time__date__gte=previous_start_date,
        start_time__date__lte=previous_end_date,
        payment_status='PAID'
    ).aggregate(total=Sum('owner_payout'))['total'] or Decimal('0.00')
    
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