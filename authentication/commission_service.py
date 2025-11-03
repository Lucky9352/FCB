"""
Commission calculation and revenue tracking service for TapNex superuser management.
"""
from decimal import Decimal
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import datetime, timedelta, date
from .models import TapNexSuperuser
from booking.models import Booking


class CommissionCalculator:
    """Service for calculating commissions and revenue analytics"""
    
    @staticmethod
    def calculate_commission(booking_amount, commission_rate, platform_fee, platform_fee_type='PERCENT'):
        """Calculate commission from a booking amount"""
        booking_amount = Decimal(str(booking_amount))
        commission_rate = Decimal(str(commission_rate))
        platform_fee = Decimal(str(platform_fee))
        
        commission = (booking_amount * commission_rate) / 100
        
        # Calculate platform fee based on type
        if platform_fee_type == 'PERCENT':
            platform_fee_amount = (booking_amount * platform_fee) / 100
        else:  # FIXED
            platform_fee_amount = platform_fee
        
        total_commission = commission + platform_fee_amount
        net_payout = booking_amount - total_commission
        
        return {
            'gross_revenue': booking_amount,
            'commission_amount': commission,
            'platform_fee': platform_fee_amount,
            'platform_fee_type': platform_fee_type,
            'total_commission': total_commission,
            'net_payout': net_payout
        }
    
    @staticmethod
    def get_revenue_analytics(start_date=None, end_date=None):
        """Get comprehensive revenue analytics for TapNex dashboard"""
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        # Get TapNex superuser settings
        try:
            tapnex_user = TapNexSuperuser.objects.first()
            commission_rate = tapnex_user.commission_rate if tapnex_user else Decimal('10.00')
            platform_fee = tapnex_user.platform_fee if tapnex_user else Decimal('0.00')
            platform_fee_type = tapnex_user.platform_fee_type if tapnex_user else 'PERCENT'
        except TapNexSuperuser.DoesNotExist:
            commission_rate = Decimal('10.00')
            platform_fee = Decimal('0.00')
            platform_fee_type = 'PERCENT'
        
        # Get confirmed bookings in date range
        bookings = Booking.objects.filter(
            status__in=['CONFIRMED', 'IN_PROGRESS', 'COMPLETED'],
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).exclude(total_amount__isnull=True)
        
        # Calculate totals
        total_bookings = bookings.count()
        gross_revenue = bookings.aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0.00')
        
        # Calculate commission breakdown
        commission_amount = (gross_revenue * commission_rate) / 100
        
        # Calculate platform fees based on type
        if platform_fee_type == 'PERCENT':
            total_platform_fees = (gross_revenue * platform_fee) / 100
        else:  # FIXED
            total_platform_fees = platform_fee * total_bookings
        
        total_commission = commission_amount + total_platform_fees
        net_payout = gross_revenue - total_commission
        
        # Booking type breakdown
        private_bookings = bookings.filter(booking_type='PRIVATE')
        shared_bookings = bookings.filter(booking_type='SHARED')
        
        private_revenue = private_bookings.aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0.00')
        
        shared_revenue = shared_bookings.aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0.00')
        
        # Daily revenue trend (last 7 days)
        daily_revenue = []
        for i in range(7):
            day = end_date - timedelta(days=i)
            day_bookings = bookings.filter(created_at__date=day)
            day_revenue = day_bookings.aggregate(
                total=Sum('total_amount')
            )['total'] or Decimal('0.00')
            
            daily_revenue.append({
                'date': day,
                'revenue': day_revenue,
                'bookings': day_bookings.count()
            })
        
        daily_revenue.reverse()  # Chronological order
        
        return {
            'period': {
                'start_date': start_date,
                'end_date': end_date,
                'days': (end_date - start_date).days + 1
            },
            'totals': {
                'gross_revenue': gross_revenue,
                'commission_amount': commission_amount,
                'platform_fees': total_platform_fees,
                'total_commission': total_commission,
                'net_payout': net_payout,
                'total_bookings': total_bookings
            },
            'booking_breakdown': {
                'private_bookings': private_bookings.count(),
                'shared_bookings': shared_bookings.count(),
                'private_revenue': private_revenue,
                'shared_revenue': shared_revenue
            },
            'settings': {
                'commission_rate': commission_rate,
                'platform_fee': platform_fee
            },
            'daily_trend': daily_revenue
        }
    
    @staticmethod
    def get_monthly_revenue_report(year=None, month=None):
        """Get detailed monthly revenue report"""
        if not year:
            year = date.today().year
        if not month:
            month = date.today().month
        
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        return CommissionCalculator.get_revenue_analytics(start_date, end_date)
    
    @staticmethod
    def get_game_revenue_breakdown(start_date=None, end_date=None):
        """Get revenue breakdown by game type"""
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        # Get bookings with game information
        bookings = Booking.objects.filter(
            status__in=['CONFIRMED', 'IN_PROGRESS', 'COMPLETED'],
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
            game__isnull=False
        ).select_related('game')
        
        # Group by game
        game_stats = {}
        for booking in bookings:
            game_name = booking.game.name
            if game_name not in game_stats:
                game_stats[game_name] = {
                    'bookings': 0,
                    'revenue': Decimal('0.00'),
                    'private_bookings': 0,
                    'shared_bookings': 0,
                    'private_revenue': Decimal('0.00'),
                    'shared_revenue': Decimal('0.00')
                }
            
            stats = game_stats[game_name]
            stats['bookings'] += 1
            stats['revenue'] += booking.total_amount or Decimal('0.00')
            
            if booking.booking_type == 'PRIVATE':
                stats['private_bookings'] += 1
                stats['private_revenue'] += booking.total_amount or Decimal('0.00')
            else:
                stats['shared_bookings'] += 1
                stats['shared_revenue'] += booking.total_amount or Decimal('0.00')
        
        # Sort by revenue
        sorted_games = sorted(
            game_stats.items(),
            key=lambda x: x[1]['revenue'],
            reverse=True
        )
        
        return sorted_games


class RevenueTracker:
    """Service for tracking and monitoring revenue metrics"""
    
    @staticmethod
    def get_real_time_metrics():
        """Get real-time dashboard metrics"""
        today = date.today()
        
        # Today's metrics
        today_bookings = Booking.objects.filter(
            status__in=['CONFIRMED', 'IN_PROGRESS', 'COMPLETED'],
            created_at__date=today
        )
        
        today_revenue = today_bookings.aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0.00')
        
        # This month's metrics
        month_start = today.replace(day=1)
        month_bookings = Booking.objects.filter(
            status__in=['CONFIRMED', 'IN_PROGRESS', 'COMPLETED'],
            created_at__date__gte=month_start,
            created_at__date__lte=today
        )
        
        month_revenue = month_bookings.aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0.00')
        
        # Active bookings (currently in progress)
        active_bookings = Booking.objects.filter(
            status='IN_PROGRESS'
        ).count()
        
        # Pending payments
        pending_payments = Booking.objects.filter(
            status='PENDING'
        ).count()
        
        # Get commission settings
        try:
            tapnex_user = TapNexSuperuser.objects.first()
            commission_rate = tapnex_user.commission_rate if tapnex_user else Decimal('10.00')
            platform_fee = tapnex_user.platform_fee if tapnex_user else Decimal('0.00')
        except TapNexSuperuser.DoesNotExist:
            commission_rate = Decimal('10.00')
            platform_fee = Decimal('0.00')
        
        # Calculate today's commission
        today_commission = CommissionCalculator.calculate_commission(
            today_revenue, commission_rate, platform_fee
        )
        
        return {
            'today': {
                'bookings': today_bookings.count(),
                'revenue': today_revenue,
                'commission': today_commission['total_commission']
            },
            'month': {
                'bookings': month_bookings.count(),
                'revenue': month_revenue
            },
            'active': {
                'in_progress': active_bookings,
                'pending_payments': pending_payments
            },
            'settings': {
                'commission_rate': commission_rate,
                'platform_fee': platform_fee
            }
        }
    
    @staticmethod
    def get_growth_metrics():
        """Get growth metrics comparing current vs previous periods"""
        today = date.today()
        
        # Current month vs previous month
        current_month_start = today.replace(day=1)
        if current_month_start.month == 1:
            prev_month_start = current_month_start.replace(year=current_month_start.year - 1, month=12)
            prev_month_end = current_month_start - timedelta(days=1)
        else:
            prev_month_start = current_month_start.replace(month=current_month_start.month - 1)
            prev_month_end = current_month_start - timedelta(days=1)
        
        # Current month revenue
        current_revenue = Booking.objects.filter(
            status__in=['CONFIRMED', 'IN_PROGRESS', 'COMPLETED'],
            created_at__date__gte=current_month_start,
            created_at__date__lte=today
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
        
        # Previous month revenue
        prev_revenue = Booking.objects.filter(
            status__in=['CONFIRMED', 'IN_PROGRESS', 'COMPLETED'],
            created_at__date__gte=prev_month_start,
            created_at__date__lte=prev_month_end
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
        
        # Calculate growth percentage
        if prev_revenue > 0:
            growth_rate = ((current_revenue - prev_revenue) / prev_revenue) * 100
        else:
            growth_rate = 100 if current_revenue > 0 else 0
        
        return {
            'current_month_revenue': current_revenue,
            'previous_month_revenue': prev_revenue,
            'growth_rate': growth_rate,
            'growth_amount': current_revenue - prev_revenue
        }