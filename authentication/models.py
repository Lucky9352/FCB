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
        help_text="Fixed platform fee per transaction"
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
        
        commission = (Decimal(str(booking_amount)) * self.commission_rate) / 100
        total_commission = commission + self.platform_fee
        net_payout = Decimal(str(booking_amount)) - total_commission
        
        return {
            'gross_revenue': booking_amount,
            'commission_amount': commission,
            'platform_fee': self.platform_fee,
            'total_commission': total_commission,
            'net_payout': net_payout
        }
