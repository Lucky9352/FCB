"""
Payment Views for Razorpay Integration
Handles order creation, payment verification, and webhooks
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from authentication.decorators import customer_required
from .models import Booking
from .razorpay_service import razorpay_service
from .booking_service import BookingService
import json
import logging

logger = logging.getLogger(__name__)


@customer_required
@require_http_methods(["POST"])
def create_razorpay_order(request, booking_id):
    """
    Create a Razorpay order for a booking
    
    POST /booking/payment/create-order/<booking_id>/
    """
    try:
        # Get booking
        booking = get_object_or_404(
            Booking, 
            id=booking_id, 
            customer=request.user.customer_profile
        )
        
        # Verify booking is pending
        if booking.status != 'PENDING':
            return JsonResponse({
                'success': False,
                'error': 'Booking is not in pending status'
            }, status=400)
        
        # Create Razorpay order
        order_result = razorpay_service.create_order(booking)
        
        if not order_result['success']:
            return JsonResponse({
                'success': False,
                'error': order_result.get('error', 'Failed to create order')
            }, status=500)
        
        # Save order ID to booking
        booking.razorpay_order_id = order_result['order_id']
        booking.save(update_fields=['razorpay_order_id'])
        
        # Return order details for frontend
        return JsonResponse({
            'success': True,
            'order_id': order_result['order_id'],
            'amount': order_result['amount'],
            'currency': order_result['currency'],
            'key': settings.RAZORPAY_KEY_ID,
            'booking_id': str(booking.id),
            'customer_name': request.user.get_full_name() or request.user.username,
            'customer_email': request.user.email,
            'customer_phone': request.user.customer_profile.phone if hasattr(request.user, 'customer_profile') and request.user.customer_profile.phone else '',
        })
        
    except Exception as e:
        logger.error(f"Error creating Razorpay order: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


@customer_required
@require_http_methods(["POST"])
def verify_razorpay_payment(request):
    """
    Verify Razorpay payment after successful payment
    
    POST /booking/payment/verify/
    Body: {
        "razorpay_order_id": "order_xxx",
        "razorpay_payment_id": "pay_xxx",
        "razorpay_signature": "signature_xxx",
        "booking_id": "uuid"
    }
    """
    try:
        data = json.loads(request.body)
        
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        booking_id = data.get('booking_id')
        
        # Validate inputs
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature, booking_id]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required payment details'
            }, status=400)
        
        # Get booking
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            customer=request.user.customer_profile
        )
        
        # Verify signature
        is_valid = razorpay_service.verify_payment_signature(
            razorpay_order_id,
            razorpay_payment_id,
            razorpay_signature
        )
        
        if not is_valid:
            logger.warning(f"Invalid payment signature for booking {booking_id}")
            return JsonResponse({
                'success': False,
                'error': 'Invalid payment signature'
            }, status=400)
        
        # Update booking with payment details
        booking.razorpay_payment_id = razorpay_payment_id
        booking.razorpay_signature = razorpay_signature
        booking.payment_status = 'PAID'
        booking.status = 'CONFIRMED'
        booking.save(update_fields=[
            'razorpay_payment_id',
            'razorpay_signature',
            'payment_status',
            'status'
        ])
        
        logger.info(f"Payment verified successfully for booking {booking_id}")
        
        # TODO: Send confirmation email/SMS
        # TODO: Update slot availability
        
        return JsonResponse({
            'success': True,
            'message': 'Payment verified successfully',
            'booking_id': str(booking.id),
            'status': booking.status
        })
        
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def razorpay_webhook(request):
    """
    Handle Razorpay webhooks
    
    POST /booking/payment/webhook/
    
    Events handled:
    - payment.authorized - Payment authorized by bank
    - payment.captured - Payment successfully captured
    - payment.failed - Payment attempt failed
    - order.paid - Order fully paid
    
    NOTE: Refunds are not supported - All sales are final
    """
    try:
        # Get webhook signature
        webhook_signature = request.headers.get('X-Razorpay-Signature')
        
        if not webhook_signature:
            logger.warning("Webhook received without signature")
            return HttpResponse(status=400)
        
        # Verify webhook signature (if webhook secret is configured)
        if settings.RAZORPAY_WEBHOOK_SECRET:
            is_valid = razorpay_service.verify_webhook_signature(
                request.body,
                webhook_signature
            )
            
            if not is_valid:
                logger.warning("Invalid webhook signature")
                return HttpResponse(status=400)
        else:
            logger.warning("Webhook secret not configured - skipping signature verification")
        
        # Parse webhook data
        webhook_data = json.loads(request.body)
        event = webhook_data.get('event')
        payload = webhook_data.get('payload', {})
        payment_entity = payload.get('payment', {}).get('entity', {})
        order_entity = payload.get('order', {}).get('entity', {})
        
        logger.info(f"Received Razorpay webhook: {event}")
        
        # Handle payment events only (no refunds)
        if event == 'payment.authorized':
            handle_payment_authorized(payment_entity)
        elif event == 'payment.captured':
            handle_payment_captured(payment_entity)
        elif event == 'payment.failed':
            handle_payment_failed(payment_entity)
        elif event == 'order.paid':
            handle_order_paid(order_entity)
        else:
            logger.info(f"Unhandled webhook event: {event}")
        
        return HttpResponse(status=200)
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return HttpResponse(status=500)


def handle_payment_authorized(payment_entity):
    """Handle payment.authorized event"""
    try:
        order_id = payment_entity.get('order_id')
        payment_id = payment_entity.get('id')
        amount = payment_entity.get('amount')
        
        # Find booking by order ID
        booking = Booking.objects.filter(razorpay_order_id=order_id).first()
        
        if not booking:
            logger.warning(f"Booking not found for order {order_id}")
            return
        
        # Update booking - payment authorized but not captured yet
        booking.razorpay_payment_id = payment_id
        booking.payment_status = 'AUTHORIZED'
        booking.notes = f"{booking.notes}\nPayment authorized: ₹{amount/100}"
        booking.save(update_fields=['razorpay_payment_id', 'payment_status', 'notes'])
        
        logger.info(f"Payment authorized for booking {booking.id}")
        
    except Exception as e:
        logger.error(f"Error handling payment.authorized: {str(e)}")


def handle_payment_captured(payment_entity):
    """Handle payment.captured event"""
    try:
        order_id = payment_entity.get('order_id')
        payment_id = payment_entity.get('id')
        amount = payment_entity.get('amount')
        
        # Find booking by order ID
        booking = Booking.objects.filter(razorpay_order_id=order_id).first()
        
        if not booking:
            logger.warning(f"Booking not found for order {order_id}")
            return
        
        # Update booking
        booking.razorpay_payment_id = payment_id
        booking.payment_status = 'PAID'
        booking.status = 'CONFIRMED'
        booking.save(update_fields=[
            'razorpay_payment_id',
            'payment_status',
            'status'
        ])
        
        logger.info(f"Payment captured for booking {booking.id}")
        
        # TODO: Send confirmation notifications
        
    except Exception as e:
        logger.error(f"Error handling payment.captured: {str(e)}")


def handle_payment_failed(payment_entity):
    """Handle payment.failed event"""
    try:
        order_id = payment_entity.get('order_id')
        error_code = payment_entity.get('error_code')
        error_description = payment_entity.get('error_description')
        
        # Find booking by order ID
        booking = Booking.objects.filter(razorpay_order_id=order_id).first()
        
        if not booking:
            logger.warning(f"Booking not found for order {order_id}")
            return
        
        # Update booking
        booking.payment_status = 'FAILED'
        booking.notes = f"{booking.notes}\nPayment failed: {error_description} ({error_code})"
        booking.save(update_fields=['payment_status', 'notes'])
        
        logger.info(f"Payment failed for booking {booking.id}: {error_description}")
        
        # TODO: Send failure notification to customer
        
    except Exception as e:
        logger.error(f"Error handling payment.failed: {str(e)}")


def handle_order_paid(order_entity):
    """Handle order.paid event"""
    try:
        order_id = order_entity.get('id')
        amount_paid = order_entity.get('amount_paid')
        
        # Find booking by order ID
        booking = Booking.objects.filter(razorpay_order_id=order_id).first()
        
        if not booking:
            logger.warning(f"Booking not found for order {order_id}")
            return
        
        # Update booking
        booking.payment_status = 'PAID'
        booking.status = 'CONFIRMED'
        booking.save(update_fields=['payment_status', 'status'])
        
        logger.info(f"Order paid for booking {booking.id}")
        
    except Exception as e:
        logger.error(f"Error handling order.paid: {str(e)}")


@customer_required
def payment_cancelled(request, booking_id):
    """
    Payment cancelled page - shown when user cancels payment
    Also automatically cancels the pending booking
    """
    try:
        # Get booking - must be owned by current user
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            customer=request.user.customer_profile
        )
        
        # Cancel the booking if it's still pending
        if booking.status == 'PENDING':
            booking.status = 'CANCELLED'
            booking.payment_status = 'CANCELLED'
            booking.notes = f"{booking.notes}\nPayment cancelled by user at {timezone.now()}"
            booking.save(update_fields=['status', 'payment_status', 'notes'])
            
            logger.info(f"Booking {booking_id} cancelled due to payment cancellation")
        
        context = {
            'booking': booking,
        }
        
        return render(request, 'booking/payment_cancelled.html', context)
        
    except Exception as e:
        logger.error(f"Error in payment_cancelled view: {str(e)}")
        messages.error(request, 'Unable to process cancellation')
        return redirect('booking:my_bookings')


@customer_required
def payment_success(request, booking_id):
    """
    Secure payment success page - ONLY accessible after verified payment
    Prevents direct URL access without payment verification
    """
    try:
        # Get booking - must be owned by current user
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            customer=request.user.customer_profile
        )
        
        # SECURITY CHECK: Only allow access if payment is verified
        if booking.status != 'CONFIRMED' or not booking.razorpay_payment_id:
            logger.warning(f"Unauthorized access to success page for booking {booking_id} - Status: {booking.status}, Payment ID: {booking.razorpay_payment_id}")
            messages.error(request, 'Payment verification required. Please complete the payment first.')
            return redirect('booking:hybrid_booking_confirm', booking_id=booking_id)
        
        # ADDITIONAL SECURITY: Check if payment was verified within last 10 minutes
        # This prevents old confirmed bookings from being accessed via this URL
        if booking.updated_at and (timezone.now() - booking.updated_at).total_seconds() > 600:
            # If updated more than 10 minutes ago, redirect to my bookings
            return redirect('booking:my_bookings')
        
        context = {
            'booking': booking,
        }
        
        return render(request, 'booking/success.html', context)
        
    except Exception as e:
        logger.error(f"Error in payment_success view: {str(e)}")
        messages.error(request, 'Unable to display booking confirmation')
        return redirect('booking:my_bookings')


@customer_required
@require_http_methods(["GET"])
def check_payment_status(request, booking_id):
    """
    API endpoint to check payment status - used as fallback when webhook verification fails
    
    GET /booking/payment/status/<booking_id>/
    """
    try:
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            customer=request.user.customer_profile
        )
        
        # If already confirmed, return success
        if booking.status == 'CONFIRMED' and booking.payment_status == 'PAID':
            return JsonResponse({
                'success': True,
                'payment_status': booking.payment_status,
                'booking_status': booking.status,
                'needs_action': False,
                'message': 'Payment confirmed successfully'
            })
        
        # Check with Razorpay if we have payment ID
        if booking.razorpay_payment_id and booking.payment_status != 'PAID':
            payment_details = razorpay_service.get_payment_details(booking.razorpay_payment_id)
            
            if payment_details and payment_details.get('status') == 'captured':
                booking.payment_status = 'PAID'
                booking.status = 'CONFIRMED'
                booking.save(update_fields=['payment_status', 'status'])
                
                logger.info(f"Payment status updated via API fallback for booking {booking_id}")
                
                return JsonResponse({
                    'success': True,
                    'payment_status': 'PAID',
                    'booking_status': 'CONFIRMED',
                    'needs_action': False,
                    'message': 'Payment confirmed successfully'
                })
        
        return JsonResponse({
            'success': True,
            'payment_status': booking.payment_status,
            'booking_status': booking.status,
            'needs_action': booking.status == 'PENDING',
            'message': 'Payment still processing' if booking.status == 'PENDING' else 'Payment completed'
        })
        
    except Exception as e:
        logger.error(f"Error checking payment status: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)
