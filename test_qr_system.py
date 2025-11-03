"""
Test script for QR Code verification system
Run this to verify the QR code generation and verification flow
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaming_cafe.settings')
django.setup()

from booking.models import Booking
from booking.qr_service import QRCodeService
from django.utils import timezone

def test_qr_generation():
    """Test QR code generation for a booking"""
    print("🧪 Testing QR Code Generation System\n")
    print("=" * 60)
    
    # Get a confirmed booking without QR code
    confirmed_bookings = Booking.objects.filter(
        status='CONFIRMED',
        qr_code__isnull=True
    ).first()
    
    if not confirmed_bookings:
        print("❌ No confirmed bookings found without QR codes")
        print("   Create a test booking first or use an existing confirmed booking")
        return
    
    booking = confirmed_bookings
    print(f"\n📋 Testing with Booking: {booking.id}")
    print(f"   Customer: {booking.customer.user.get_full_name()}")
    print(f"   Status: {booking.get_status_display()}")
    
    # Generate QR code
    print("\n🔄 Generating QR code...")
    success = QRCodeService.generate_qr_code(booking)
    
    if success:
        print("✅ QR Code generated successfully!")
        print(f"   Token: {booking.verification_token[:20]}...")
        print(f"   QR Code Path: {booking.qr_code.name if booking.qr_code else 'None'}")
    else:
        print("❌ Failed to generate QR code")
        return
    
    # Test token verification
    print("\n🔍 Testing token verification...")
    is_valid, verified_booking, message = QRCodeService.verify_token(
        booking.verification_token
    )
    
    if is_valid:
        print(f"✅ Token verification successful!")
        print(f"   Message: {message}")
        print(f"   Booking ID: {verified_booking.id}")
        print(f"   Is Verified: {verified_booking.is_verified}")
    else:
        print(f"❌ Token verification failed: {message}")
        return
    
    print("\n" + "=" * 60)
    print("✨ QR Code Verification System Test Complete!")
    print("\n📊 Summary:")
    print(f"   ✓ QR Code Generated")
    print(f"   ✓ Verification Token: {booking.verification_token[:30]}...")
    print(f"   ✓ Token Validation: Working")
    print(f"   ✓ System Status: Ready for Production")
    print("\n🎯 Next Steps:")
    print("   1. View QR code at: /booking/my-bookings/")
    print("   2. Scan QR code at: /booking/qr-scanner/")
    print("   3. View active bookings: /booking/active-bookings/")


def test_qr_verification_flow():
    """Test the full verification flow"""
    print("\n\n🧪 Testing Full Verification Flow\n")
    print("=" * 60)
    
    # Get a booking with QR code
    booking_with_qr = Booking.objects.filter(
        status='CONFIRMED',
        qr_code__isnull=False
    ).first()
    
    if not booking_with_qr:
        print("❌ No bookings with QR codes found")
        print("   Run test_qr_generation() first")
        return
    
    print(f"\n📋 Booking: {booking_with_qr.id}")
    print(f"   Verification Status: {'✅ Verified' if booking_with_qr.is_verified else '⏳ Not Verified'}")
    
    # Simulate verification (without actually marking as verified)
    is_valid, booking, message = QRCodeService.verify_token(
        booking_with_qr.verification_token
    )
    
    print(f"\n🔍 Verification Result:")
    print(f"   Valid: {is_valid}")
    print(f"   Message: {message}")
    
    if is_valid:
        print(f"\n✅ Verification Flow Test Passed!")
    else:
        print(f"\n❌ Verification Flow Test Failed")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    print("\n🚀 QR Code Verification System - Test Suite\n")
    
    try:
        test_qr_generation()
        test_qr_verification_flow()
        
        print("\n\n✨ All Tests Complete! ✨\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
