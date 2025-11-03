from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Customer(models.Model):
    """Customer model for gaming cafe customers who book gaming slots"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    google_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Customer: {self.user.get_full_name() or self.user.username}"

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class CafeOwner(models.Model):
    """Cafe owner model for managing gaming cafe operations"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cafe_owner_profile')
    cafe_name = models.CharField(max_length=100, default="Gaming Cafe")
    contact_email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cafe Owner: {self.user.get_full_name() or self.user.username} - {self.cafe_name}"

    class Meta:
        verbose_name = "Cafe Owner"
        verbose_name_plural = "Cafe Owners"


class TapNexSuperuser(models.Model):
    """TapNex Technologies superuser for SaaS management"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tapnex_superuser_profile')
    
    # Commission Settings
    commission_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=10.00,
        help_text="Commission percentage (e.g., 10.00 for 10%)"
    )
    platform_fee = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=0.00,
        help_text="Platform fee - can be fixed amount or percentage based on platform_fee_type"
    )
    platform_fee_type = models.CharField(
        max_length=10,
        choices=[
            ('FIXED', 'Fixed Amount (₹)'),
            ('PERCENT', 'Percentage (%)')
        ],
        default='PERCENT',
        help_text="Type of platform fee calculation"
    )
    
    # Contact Information
    contact_email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TapNex Superuser: {self.user.get_full_name() or self.user.username}"

    class Meta:
        verbose_name = "TapNex Superuser"
        verbose_name_plural = "TapNex Superusers"
    
    def calculate_commission(self, booking_amount):
        """Calculate commission from a booking amount"""
        from decimal import Decimal
        
        booking_amount = Decimal(str(booking_amount))
        commission = (booking_amount * self.commission_rate) / 100
        
        # Calculate platform fee based on type
        if self.platform_fee_type == 'PERCENT':
            platform_fee_amount = (booking_amount * self.platform_fee) / 100
        else:  # FIXED
            platform_fee_amount = self.platform_fee
        
        total_commission = commission + platform_fee_amount
        net_payout = booking_amount - total_commission
        
        return {
            'gross_revenue': booking_amount,
            'commission_amount': commission,
            'platform_fee': platform_fee_amount,
            'platform_fee_type': self.platform_fee_type,
            'total_commission': total_commission,
            'net_payout': net_payout
        }
