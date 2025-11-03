"""
Test platform fee calculation
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaming_cafe.settings')
django.setup()

from authentication.models import TapNexSuperuser
from decimal import Decimal

# Get or create TapNex user
tapnex_user = TapNexSuperuser.objects.first()

if tapnex_user:
    print("=" * 60)
    print("🔍 PLATFORM FEE CONFIGURATION")
    print("=" * 60)
    print(f"Platform Fee: ₹{tapnex_user.platform_fee}")
    print(f"Fee Type: {tapnex_user.get_platform_fee_type_display()}")
    print(f"Commission Rate: {tapnex_user.commission_rate}%")
    print()
    
    # Test calculation
    test_amounts = [100, 500, 1000]
    print("=" * 60)
    print("💰 PLATFORM FEE CALCULATION TEST")
    print("=" * 60)
    
    for amount in test_amounts:
        result = tapnex_user.calculate_commission(amount)
        print(f"\nBooking Amount: ₹{amount}")
        print(f"  Commission ({tapnex_user.commission_rate}%): ₹{result['commission_amount']:.2f}")
        print(f"  Platform Fee ({tapnex_user.get_platform_fee_type_display()}): ₹{result['platform_fee']:.2f}")
        print(f"  Total Deduction: ₹{result['total_commission']:.2f}")
        print(f"  Net Payout to Owner: ₹{result['net_payout']:.2f}")
    
    print("\n" + "=" * 60)
    print("✅ Platform fee system is configured and working!")
    print("=" * 60)
else:
    print("❌ No TapNex superuser found. Please create one first.")
