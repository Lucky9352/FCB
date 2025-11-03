# 💳 Razorpay Payment Integration - Complete Guide

## 🎯 Overview

This document provides a comprehensive guide to the Razorpay payment integration implemented in the TapNex Gaming Cafe booking system.

---

## 🔑 Test Credentials

### Razorpay Test Mode
```
API Key ID:     your_test_key_id
API Key Secret: your_test_key_secret
```
Get your test credentials from Razorpay Dashboard > Settings > API Keys

### Test Cards for Payment Testing
```
Card Number: 4111 1111 1111 1111
CVV: Any 3 digits
Expiry: Any future date
Name: Any name

Other test cards:
- Success: 5555 5555 5555 4444
- Failure: 4000 0000 0000 0002
```

### UPI Testing
```
UPI ID: success@razorpay
Status: Payment will succeed

UPI ID: failure@razorpay
Status: Payment will fail
```

---

## 📁 Implementation Files

### 1. Backend Files

#### `gaming_cafe/settings.py`
```python
# Razorpay Configuration
RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID', default='')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET', default='')
RAZORPAY_WEBHOOK_SECRET = config('RAZORPAY_WEBHOOK_SECRET', default='')
```

#### `booking/razorpay_service.py`
**Purpose:** Core service for Razorpay operations
- Create orders
- Verify payment signatures
- Handle webhook verification
- Payment capture and refunds

#### `booking/payment_views.py`
**Purpose:** Payment API endpoints
- `create_razorpay_order()` - Create payment order
- `verify_razorpay_payment()` - Verify payment signature
- `razorpay_webhook()` - Handle payment webhooks

#### `booking/models.py`
**New Fields in Booking Model:**
```python
razorpay_order_id = models.CharField(max_length=100, blank=True)
razorpay_payment_id = models.CharField(max_length=100, blank=True)
razorpay_signature = models.CharField(max_length=500, blank=True)
```

### 2. Frontend Files

#### `templates/booking/hybrid_confirm.html`
**Razorpay Checkout Integration:**
- Razorpay JavaScript SDK included
- Payment flow implementation
- Success/failure handling

---

## 🔄 Payment Flow

### Step-by-Step Process

```
1. Customer selects a game slot and booking type
   ↓
2. Booking created with status = 'PENDING'
   ↓
3. Customer clicks "Proceed to Payment"
   ↓
4. Frontend calls: POST /booking/payment/create-order/<booking_id>/
   ↓
5. Backend creates Razorpay order via API
   ↓
6. Order ID saved to booking.razorpay_order_id
   ↓
7. Frontend receives order details and Razorpay key
   ↓
8. Razorpay checkout modal opens
   ↓
9. Customer completes payment
   ↓
10. Razorpay returns payment details (order_id, payment_id, signature)
   ↓
11. Frontend calls: POST /booking/payment/verify/
   ↓
12. Backend verifies signature using HMAC-SHA256
   ↓
13. If valid:
    - booking.status = 'CONFIRMED'
    - booking.payment_status = 'PAID'
    - booking.razorpay_payment_id = payment_id
    - booking.razorpay_signature = signature
   ↓
14. Customer redirected to My Bookings page
   ↓
15. Webhook (async) confirms payment and updates records
```

---

## 🔐 Security Features

### 1. Signature Verification
- **Algorithm:** HMAC-SHA256
- **Key:** Razorpay Secret Key
- **Message:** `{order_id}|{payment_id}`
- **Protection:** Prevents payment manipulation

### 2. Webhook Verification
- **Header:** `X-Razorpay-Signature`
- **Verification:** HMAC-SHA256 of webhook body
- **Protection:** Ensures webhooks are from Razorpay

### 3. CSRF Protection
- All POST endpoints require CSRF token
- Django's built-in CSRF middleware

### 4. Authentication
- `@customer_required` decorator on payment endpoints
- Ensures only booking owner can make payment

---

## 📡 API Endpoints

### 1. Create Order
```
POST /booking/payment/create-order/<booking_id>/

Headers:
- X-CSRFToken: <token>
- Content-Type: application/json

Response:
{
    "success": true,
    "order_id": "order_xxx",
    "amount": 11800,  // in paise (₹118.00)
    "currency": "INR",
    "key": "rzp_test_xxx",
    "booking_id": "uuid",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "9876543210"
}
```

### 2. Verify Payment
```
POST /booking/payment/verify/

Headers:
- X-CSRFToken: <token>
- Content-Type: application/json

Body:
{
    "razorpay_order_id": "order_xxx",
    "razorpay_payment_id": "pay_xxx",
    "razorpay_signature": "signature_xxx",
    "booking_id": "uuid"
}

Response:
{
    "success": true,
    "message": "Payment verified successfully",
    "booking_id": "uuid",
    "status": "CONFIRMED"
}
```

### 3. Webhook Handler
```
POST /booking/payment/webhook/

Headers:
- X-Razorpay-Signature: <webhook_signature>

Body: (Razorpay event payload)

Events Handled:
- payment.captured
- payment.failed
- order.paid
- refund.processed
```

---

## 🎨 Frontend Integration

### JavaScript Code Example
```javascript
function proceedToPayment() {
    // 1. Create Razorpay order
    fetch('/booking/payment/create-order/<booking_id>/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // 2. Initialize Razorpay checkout
        const options = {
            key: data.key,
            amount: data.amount,
            currency: data.currency,
            order_id: data.order_id,
            name: 'TapNex - Gaming Cafe',
            handler: function(response) {
                // 3. Verify payment
                verifyPayment(response, data.booking_id);
            }
        };
        
        const rzp = new Razorpay(options);
        rzp.open();
    });
}
```

---

## 🧪 Testing Instructions

### 1. Local Testing

1. **Install razorpay package:**
   ```bash
   pip install razorpay
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Start development server:**
   ```bash
   python manage.py runserver
   ```

4. **Test payment flow:**
   - Navigate to booking page
   - Select a game slot
   - Choose booking type
   - Click "Proceed to Payment"
   - Use test card: 4111 1111 1111 1111
   - Complete payment

### 2. Webhook Testing

1. **Install ngrok:**
   ```bash
   ngrok http 8000
   ```

2. **Configure webhook in Razorpay Dashboard:**
   ```
   URL: https://your-ngrok-url.ngrok.io/booking/payment/webhook/
   Events: payment.captured, payment.failed, order.paid, refund.processed
   ```

3. **Get webhook secret from Razorpay Dashboard**

4. **Update settings:**
   ```python
   RAZORPAY_WEBHOOK_SECRET = 'your_webhook_secret'
   ```

### 3. Test Scenarios

#### ✅ Successful Payment
```
1. Select slot → Book → Pay with 4111 1111 1111 1111
2. Expected: Payment success → Booking CONFIRMED
```

#### ❌ Failed Payment
```
1. Select slot → Book → Pay with 4000 0000 0000 0002
2. Expected: Payment failure → Booking remains PENDING
```

#### 🔙 Payment Cancelled
```
1. Select slot → Book → Close payment modal
2. Expected: Booking remains PENDING, can retry payment
```

---

## 🚀 Production Deployment

### 1. Environment Variables

Add to Vercel/Production:
```env
RAZORPAY_KEY_ID=rzp_live_xxxxx
RAZORPAY_KEY_SECRET=live_secret_key
RAZORPAY_WEBHOOK_SECRET=whsec_xxxxx
```

### 2. Razorpay Dashboard Setup

1. **Create Production API Keys:**
   - Go to Razorpay Dashboard → Settings → API Keys
   - Generate Live API keys

2. **Configure Webhooks:**
   ```
   URL: https://forge.tapnex.tech/booking/payment/webhook/
   Events: 
     - payment.captured
     - payment.failed
     - order.paid
     - refund.processed
   ```

3. **Domain Whitelisting:**
   - Add domain: `forge.tapnex.tech`
   - Upload policy pages (Privacy, Terms, Refund)
   - Submit for verification

### 3. SSL/HTTPS
- ✅ Required for production
- ✅ Vercel provides automatic HTTPS

---

## 📊 Database Schema

### Booking Model Fields
```sql
-- Razorpay specific fields
razorpay_order_id VARCHAR(100)      -- Order ID from Razorpay
razorpay_payment_id VARCHAR(100)    -- Payment ID after success
razorpay_signature VARCHAR(500)     -- Signature for verification

-- Payment status fields
payment_status VARCHAR(20)          -- PENDING, PAID, FAILED, REFUNDED
status VARCHAR(20)                  -- PENDING, CONFIRMED, CANCELLED, etc.
```

---

## 🔍 Troubleshooting

### Issue: "Module 'razorpay' not found"
**Solution:**
```bash
pip install razorpay
```

### Issue: "Invalid signature"
**Solution:**
- Check if RAZORPAY_KEY_SECRET is correct
- Verify order_id and payment_id are correct
- Ensure signature verification uses correct HMAC algorithm

### Issue: "Webhook not received"
**Solution:**
- Check webhook URL is accessible
- Verify webhook signature verification
- Check Razorpay Dashboard → Webhooks → Logs

### Issue: "Payment successful but booking not confirmed"
**Solution:**
- Check Django logs for errors
- Verify signature verification is working
- Check database for booking status
- Review webhook logs in Razorpay Dashboard

---

## 📝 Payment Status States

```python
PAYMENT_STATUS_CHOICES = [
    ('PENDING', 'Payment Pending'),
    ('PAID', 'Payment Successful'),
    ('FAILED', 'Payment Failed'),
    ('REFUNDED', 'Payment Refunded'),
]

BOOKING_STATUS_CHOICES = [
    ('PENDING', 'Pending Payment'),
    ('CONFIRMED', 'Confirmed'),
    ('IN_PROGRESS', 'In Progress'),
    ('COMPLETED', 'Completed'),
    ('CANCELLED', 'Cancelled'),
    ('NO_SHOW', 'No Show'),
]
```

---

## 🎯 Next Steps

### Immediate
- ✅ Test complete payment flow locally
- ✅ Verify webhook integration with ngrok
- ✅ Test success and failure scenarios

### Before Production
- [ ] Switch to live API keys
- [ ] Configure production webhooks
- [ ] Complete Razorpay domain whitelisting
- [ ] Test on staging environment
- [ ] Set up payment monitoring alerts

### Optional Enhancements
- [ ] Add email notifications for payment status
- [ ] Implement SMS notifications
- [ ] Add payment retry logic
- [ ] Create admin dashboard for payment tracking
- [ ] Add refund management interface

---

## 📞 Support

### Razorpay Support
- **Dashboard:** https://dashboard.razorpay.com
- **Docs:** https://razorpay.com/docs/
- **Support:** support@razorpay.com

### TapNex Support
- **Email:** support@tapnex.tech
- **Domain:** forge.tapnex.tech

---

## ✅ Integration Checklist

- [x] Install razorpay Python package
- [x] Configure Razorpay credentials in settings
- [x] Create razorpay_service.py
- [x] Implement payment views
- [x] Add payment URLs
- [x] Update Booking model with Razorpay fields
- [x] Create database migrations
- [x] Integrate Razorpay checkout in frontend
- [x] Implement payment verification
- [x] Add webhook handler
- [x] Update booking service for payment confirmation
- [ ] Test complete flow end-to-end
- [ ] Configure production webhooks
- [ ] Submit for Razorpay domain whitelisting

---

**Last Updated:** November 2, 2025  
**Version:** 1.0.0  
**Status:** ✅ Ready for Testing
