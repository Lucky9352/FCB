"""
Test Razorpay Integration
Run this script to verify Razorpay service is working correctly
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaming_cafe.settings')
django.setup()

from booking.razorpay_service import razorpay_service
from booking.models import Booking
from decimal import Decimal


def test_razorpay_connection():
    """Test if Razorpay client is initialized correctly"""
    print("=" * 70)
    print("Testing Razorpay Connection...")
    print("=" * 70)
    
    try:
        # Check if client is initialized
        if razorpay_service.client:
            print("✅ Razorpay client initialized successfully")
            print(f"   Using Key ID: {razorpay_service.client.auth[0][:15]}...")
            return True
        else:
            print("❌ Razorpay client not initialized")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_order_creation():
    """Test creating a Razorpay order"""
    print("\n" + "=" * 70)
    print("Testing Order Creation...")
    print("=" * 70)
    
    try:
        # Get a pending booking (or create a test one)
        booking = Booking.objects.filter(status='PENDING').first()
        
        if not booking:
            print("⚠️  No pending bookings found. Skipping order creation test.")
            return False
        
        print(f"Using booking: {booking.id}")
        print(f"Amount: ₹{booking.total_amount}")
        
        # Create order
        result = razorpay_service.create_order(booking)
        
        if result['success']:
            print("✅ Order created successfully")
            print(f"   Order ID: {result['order_id']}")
            print(f"   Amount: ₹{result['amount']/100}")
            print(f"   Currency: {result['currency']}")
            return True
        else:
            print(f"❌ Order creation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_signature_verification():
    """Test payment signature verification"""
    print("\n" + "=" * 70)
    print("Testing Signature Verification...")
    print("=" * 70)
    
    try:
        # Test with sample data
        test_order_id = "order_test123"
        test_payment_id = "pay_test456"
        
        # Generate expected signature
        import hmac
        import hashlib
        from django.conf import settings
        
        message = f"{test_order_id}|{test_payment_id}"
        expected_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        print(f"Test Order ID: {test_order_id}")
        print(f"Test Payment ID: {test_payment_id}")
        print(f"Expected Signature: {expected_signature[:50]}...")
        
        # Verify signature
        is_valid = razorpay_service.verify_payment_signature(
            test_order_id,
            test_payment_id,
            expected_signature
        )
        
        if is_valid:
            print("✅ Signature verification working correctly")
            return True
        else:
            print("❌ Signature verification failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "RAZORPAY INTEGRATION TEST" + " " * 23 + "║")
    print("╚" + "=" * 68 + "╝")
    
    results = []
    
    # Test 1: Connection
    results.append(("Razorpay Connection", test_razorpay_connection()))
    
    # Test 2: Order Creation
    results.append(("Order Creation", test_order_creation()))
    
    # Test 3: Signature Verification
    results.append(("Signature Verification", test_signature_verification()))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<50} {status}")
    
    total_tests = len(results)
    passed_tests = sum(1 for _, result in results if result)
    
    print("=" * 70)
    print(f"Total Tests: {total_tests} | Passed: {passed_tests} | Failed: {total_tests - passed_tests}")
    print("=" * 70)
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Razorpay integration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("\n" + "=" * 70)
    print("Next Steps:")
    print("=" * 70)
    print("1. Create a booking in the system")
    print("2. Navigate to the booking confirmation page")
    print("3. Click 'Proceed to Payment'")
    print("4. Use test card: 4111 1111 1111 1111")
    print("5. Complete the payment flow")
    print("6. Verify booking status changes to CONFIRMED")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
