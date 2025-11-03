# 🔔 Razorpay Webhook Setup Guide

## 📋 Complete Webhook Configuration Instructions

---

## 🎯 **Webhook URL**

### Production URL
```
https://forge.tapnex.tech/booking/payment/webhook/
```

### For Local Testing (using ngrok)
```
https://your-ngrok-url.ngrok.io/booking/payment/webhook/
```

---

## ⚙️ **Setup Steps**

### **Step 1: Access Razorpay Dashboard**

1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com)
2. Login with your credentials
3. Navigate to **Settings** → **Webhooks**

### **Step 2: Create New Webhook**

1. Click **"Create New Webhook"** or **"+ Add Webhook"**
2. Enter the webhook details as shown in the image you provided

### **Step 3: Configure Webhook URL**

```
Webhook URL: https://forge.tapnex.tech/booking/payment/webhook/
```

**OR for local testing:**
```
Webhook URL: https://your-ngrok-url.ngrok.io/booking/payment/webhook/
```

### **Step 4: Set Alert Email**

```
Alert Email: tapnex.fc@gmail.com
```

This email will receive notifications if webhooks fail.

### **Step 5: Select Active Events**

#### ✅ **Required Events for Gaming Cafe Booking System**

Select **ONLY** these events from the Razorpay webhook setup:

##### **Payment Events** (Essential - Must Select All)
- ☑️ `payment.authorized` - Payment has been authorized by bank
- ☑️ `payment.captured` - Payment has been successfully captured
- ☑️ `payment.failed` - Payment attempt failed

##### **Order Events** (Essential)
- ☑️ `order.paid` - Order has been fully paid

##### **DO NOT SELECT** (Refunds Not Supported)
- ☐ ~~refund.processed~~ - NOT NEEDED
- ☐ ~~refund.failed~~ - NOT NEEDED  
- ☐ ~~refund.created~~ - NOT NEEDED

**⚠️ IMPORTANT:** This system does NOT support refunds. As per your refund policy:
- **NO REFUNDS** - All bookings are final
- Rescheduling allowed **ONCE** only
- No cancellations permitted

##### **Optional Events** (Not Required)
- ☐ `payment.dispute.created` - Only if you want dispute notifications
- ☐ `settlement.processed` - Only for settlement tracking

### **Step 6: Generate Webhook Secret**

1. After creating the webhook, Razorpay will generate a **Webhook Secret**
2. **IMPORTANT:** Copy this secret immediately
3. It will look like: `whsec_xxxxxxxxxxxxxxxxxxxxx`

### **Step 7: Add Secret to Your Application**

#### For Local Development (.env file):
```env
RAZORPAY_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

#### For Vercel Production:
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add new variable:
   - **Name:** `RAZORPAY_WEBHOOK_SECRET`
   - **Value:** `whsec_your_webhook_secret_here`
   - **Environment:** Production (and Preview if needed)
3. Click **Save**
4. **Redeploy** your application

---

## 🧪 **Testing Webhooks Locally with ngrok**

### **Step 1: Install ngrok**

**Windows:**
```bash
# Download from https://ngrok.com/download
# Or use chocolatey
choco install ngrok
```

**Mac/Linux:**
```bash
# Using Homebrew
brew install ngrok
```

### **Step 2: Create ngrok Account**
1. Sign up at https://ngrok.com/
2. Get your auth token from dashboard
3. Configure ngrok:
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### **Step 3: Start Django Development Server**
```bash
cd e:/FGC
python manage.py runserver
```

### **Step 4: Start ngrok Tunnel**

Open a **new terminal** and run:
```bash
ngrok http 8000
```

You'll see output like:
```
Session Status                online
Account                       Your Name (Plan: Free)
Version                       3.x.x
Region                        India (in)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000
```

### **Step 5: Use ngrok URL in Razorpay**

Copy the HTTPS forwarding URL (e.g., `https://abc123.ngrok.io`) and configure webhook:
```
Webhook URL: https://abc123.ngrok.io/booking/payment/webhook/
```

### **Step 6: Monitor Webhook Requests**

Open in browser: `http://127.0.0.1:4040`

This shows all incoming webhook requests in real-time.

---

## 📝 **Webhook Configuration Summary**

### **Events We Handle in Code:**

| Event | Handler Function | Description |
|-------|-----------------|-------------|
| `payment.authorized` | `handle_payment_authorized()` | Payment authorized by bank, not captured yet |
| `payment.captured` | `handle_payment_captured()` | Payment successfully captured - booking confirmed |
| `payment.failed` | `handle_payment_failed()` | Payment attempt failed |
| `order.paid` | `handle_order_paid()` | Order fully paid |

**Note:** Refund events are NOT handled as per NO REFUND policy.

### **Booking Status Updates:**

| Webhook Event | Booking Status | Payment Status | Notes |
|--------------|----------------|----------------|-------|
| `payment.authorized` | PENDING | AUTHORIZED | Payment approved but not yet captured |
| `payment.captured` | CONFIRMED | PAID | ✅ Booking confirmed - payment successful |
| `payment.failed` | PENDING | FAILED | Customer can retry payment |
| `order.paid` | CONFIRMED | PAID | ✅ Alternative confirmation event |

**⚠️ NO REFUND EVENTS** - All sales are final as per company policy.

---

## 🔐 **Security Verification**

### **How Signature Verification Works:**

1. Razorpay sends webhook with header: `X-Razorpay-Signature`
2. Our code verifies this signature using HMAC-SHA256
3. Only valid webhooks are processed

### **Verification Code (Already Implemented):**
```python
def verify_webhook_signature(webhook_body, webhook_signature):
    expected_signature = hmac.new(
        RAZORPAY_WEBHOOK_SECRET.encode('utf-8'),
        webhook_body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, webhook_signature)
```

---

## 🧪 **Testing Webhook Events**

### **Method 1: Razorpay Dashboard Test Mode**

1. Go to Razorpay Dashboard → Webhooks
2. Find your webhook
3. Click **"Send Test Webhook"**
4. Select event type (e.g., `payment.captured`)
5. Click **Send**

### **Method 2: Make Real Test Payment**

1. Create a booking in your application
2. Complete payment with test card: `4111 1111 1111 1111`
3. Webhook will be triggered automatically
4. Check Django logs to verify webhook received

### **Method 3: Check Webhook Logs**

Razorpay Dashboard → Webhooks → Your Webhook → Logs

You can see:
- All webhook deliveries
- Response codes
- Retry attempts
- Error messages

---

## 🔍 **Troubleshooting Webhooks**

### **Issue: Webhook not received**

**Solutions:**
1. Check webhook URL is correct and accessible
2. Verify ngrok is running (for local testing)
3. Check Razorpay webhook logs for errors
4. Ensure your server is running

### **Issue: Signature verification failed**

**Solutions:**
1. Verify `RAZORPAY_WEBHOOK_SECRET` is set correctly
2. Check environment variable is loaded in settings.py
3. Ensure webhook secret matches Razorpay dashboard

### **Issue: Webhook received but booking not updated**

**Solutions:**
1. Check Django logs: `python manage.py runserver`
2. Verify booking exists with matching `razorpay_order_id`
3. Check webhook event type is handled in code
4. Look for error messages in logs

### **Issue: 400 Bad Request**

**Causes:**
- Missing `X-Razorpay-Signature` header
- Invalid signature

**Solution:**
- Verify webhook secret is configured correctly

### **Issue: 500 Internal Server Error**

**Causes:**
- Error in webhook handler code
- Database connection issue

**Solution:**
- Check Django logs for Python traceback
- Fix any errors in payment_views.py

---

## 📊 **Monitoring Webhooks**

### **Django Logs**
```bash
cd e:/FGC
python manage.py runserver

# Watch for logs like:
# INFO: Received Razorpay webhook: payment.captured
# INFO: Payment captured for booking <uuid>
```

### **Razorpay Dashboard**

**Settings → Webhooks → Your Webhook → Logs**

Monitor:
- ✅ Success count
- ❌ Failure count
- 🔄 Retry attempts
- 📝 Response details

### **ngrok Web Interface (Local Testing)**

**http://127.0.0.1:4040**

See:
- All HTTP requests
- Request/response headers
- Request body
- Response status

---

## 🚀 **Production Checklist**

### **Before Going Live:**

- [ ] Create webhook in Razorpay **Live Mode** Dashboard
- [ ] Set webhook URL to production: `https://forge.tapnex.tech/booking/payment/webhook/`
- [ ] Copy webhook secret from Razorpay
- [ ] Add `RAZORPAY_WEBHOOK_SECRET` to Vercel environment variables
- [ ] Redeploy application on Vercel
- [ ] Test webhook with **Send Test Webhook** in Razorpay Dashboard
- [ ] Monitor webhook logs for any failures
- [ ] Verify booking status updates correctly

### **Recommended Events for Production:**

**✅ REQUIRED (Select These):**
```
✓ payment.authorized
✓ payment.captured
✓ payment.failed
✓ order.paid
```

**❌ DO NOT SELECT (Not Supported):**
```
✗ refund.processed
✗ refund.failed
✗ refund.created
```

**Optional (For Monitoring):**
```
? payment.dispute.created
? settlement.processed
```

**⚠️ REFUND POLICY:** No refunds are issued. All bookings are final.

---

## 📱 **Webhook Event Examples**

### **payment.captured Event**
```json
{
  "event": "payment.captured",
  "payload": {
    "payment": {
      "entity": {
        "id": "pay_xxxxxxxxxxxxx",
        "order_id": "order_xxxxxxxxxxxxx",
        "amount": 11800,
        "currency": "INR",
        "status": "captured",
        "method": "card",
        "email": "customer@example.com",
        "contact": "9876543210"
      }
    }
  }
}
```

### **payment.failed Event**
```json
{
  "event": "payment.failed",
  "payload": {
    "payment": {
      "entity": {
        "id": "pay_xxxxxxxxxxxxx",
        "order_id": "order_xxxxxxxxxxxxx",
        "amount": 11800,
        "status": "failed",
        "error_code": "BAD_REQUEST_ERROR",
        "error_description": "Payment processing failed"
      }
    }
  }
}
```

### **refund.processed Event**
```
NOT SUPPORTED - Refunds are not issued
All sales are final as per company policy
```

---

## 🎯 **Quick Setup Summary**

### **For Production:**

1. **Razorpay Dashboard:**
   - URL: `https://forge.tapnex.tech/booking/payment/webhook/`
   - Email: `tapnex.fc@gmail.com`
   - Events: **payment.authorized, payment.captured, payment.failed, order.paid**
   - **DO NOT SELECT:** refund events (not supported)
   - Copy webhook secret

2. **Vercel:**
   - Add environment variable: `RAZORPAY_WEBHOOK_SECRET`
   - Redeploy application

3. **Test:**
   - Use "Send Test Webhook" in Razorpay Dashboard
   - Monitor webhook logs

### **For Local Testing:**

1. **Start ngrok:** `ngrok http 8000`
2. **Copy ngrok URL:** `https://abc123.ngrok.io`
3. **Create webhook:** `https://abc123.ngrok.io/booking/payment/webhook/`
4. **Add secret to .env:** `RAZORPAY_WEBHOOK_SECRET=whsec_xxx`
5. **Test:** Make a test payment

---

## 📞 **Support**

### **Razorpay Webhook Documentation:**
https://razorpay.com/docs/webhooks/

### **Razorpay Support:**
support@razorpay.com

### **Check Webhook Status:**
Dashboard → Settings → Webhooks → Logs

---

## ✅ **Webhook Setup Checklist**

- [ ] Webhook URL configured in Razorpay
- [ ] Alert email set to tapnex.fc@gmail.com
- [ ] Required events selected
- [ ] Webhook secret copied
- [ ] RAZORPAY_WEBHOOK_SECRET added to environment
- [ ] Application redeployed (if production)
- [ ] Test webhook sent successfully
- [ ] Webhook logs show successful deliveries
- [ ] Booking status updates correctly

---

**Status:** 🟢 Ready to Configure  
**Last Updated:** November 2, 2025  
**Version:** 1.0.0
