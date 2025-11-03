"""
Update existing bookings with platform fee
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaming_cafe.settings')
django.setup()

from booking.models import Booking
from authentication.models import TapNexSuperuser
from decimal import Decimal

print("=" * 60)
print("🔄 UPDATING EXISTING BOOKINGS WITH PLATFORM FEE")
print("=" * 60)

# Get TapNex user for platform fee settings
tapnex_user = TapNexSuperuser.objects.first()

if not tapnex_user:
    print("❌ No TapNex superuser found!")
    exit(1)

print(f"\nPlatform Fee: {tapnex_user.platform_fee}% ({tapnex_user.get_platform_fee_type_display()})")

# Get all bookings without platform fee
bookings = Booking.objects.filter(
    platform_fee=0,
    total_amount__isnull=False
).exclude(status='CANCELLED')

print(f"\nFound {bookings.count()} bookings to update\n")

updated_count = 0
for booking in bookings:
    # Calculate what the original subtotal should be
    if booking.price_per_spot and booking.spots_booked:
        original_subtotal = Decimal(str(booking.price_per_spot)) * Decimal(str(booking.spots_booked))
    else:
        original_subtotal = booking.total_amount
    
    # Calculate platform fee
    if tapnex_user.platform_fee_type == 'PERCENT':
        platform_fee = (original_subtotal * tapnex_user.platform_fee) / 100
    else:
        platform_fee = tapnex_user.platform_fee
    
    # Update booking
    booking.subtotal = original_subtotal
    booking.platform_fee = platform_fee
    booking.total_amount = original_subtotal + platform_fee
    booking.save(update_fields=['subtotal', 'platform_fee', 'total_amount'])
    
    print(f"✓ Updated Booking {booking.id}")
    print(f"  Subtotal: ₹{original_subtotal:.2f}")
    print(f"  Platform Fee: ₹{platform_fee:.2f}")
    print(f"  New Total: ₹{booking.total_amount:.2f}\n")
    
    updated_count += 1

print("=" * 60)
print(f"✅ Updated {updated_count} bookings successfully!")
print("=" * 60)
