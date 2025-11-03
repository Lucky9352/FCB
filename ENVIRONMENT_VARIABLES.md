# 🔐 Environment Variables Reference

## Complete list of all credentials and configuration

---

## 📋 Razorpay Credentials (Payment Gateway)

### Test Mode (Development)
```env
RAZORPAY_KEY_ID=rzp_test_Rat3BJ8CMAJh83
RAZORPAY_KEY_SECRET=iuCEUkHFhzmBXLZZa6BVTv3C
RAZORPAY_WEBHOOK_SECRET=Prabhav@770jain
```

### Production (Live Mode)
```env
# Replace with live credentials from Razorpay Dashboard
RAZORPAY_KEY_ID=rzp_live_xxxxx
RAZORPAY_KEY_SECRET=live_secret_xxxxx
RAZORPAY_WEBHOOK_SECRET=whsec_xxxxx
```

---

## 🗄️ Database (Supabase PostgreSQL)

```env
SUPABASE_URL=https://wektxjtwsohaisjpayim.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indla3R4anR3c29oYWlzanBheWltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3NzI4NDEsImV4cCI6MjA3NzM0ODg0MX0.kuPH6aiLNxbhO6XYd3uFj-ZGMqKmsm18z58fz2aY8lI
DATABASE_URL=postgresql://postgres.wektxjtwsohaisjpayim:aadijain@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
```

---

## 🔑 Google OAuth (Social Login)

```env
GOOGLE_OAUTH_CLIENT_ID=325233701971-k0qpv18co8opur874aguuhq1sdarhok4.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=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
```

---

## ⚙️ Django Configuration

```env
SECRET_KEY=django-insecure--1qn5na%ea)^-@n7_!cc+#p$n^38(^b0%3zan2b$ezh^vkh3mi
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app,forge.tapnex.tech
```

---

## 📧 Email Configuration

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@gamingcafe.com
```

---

## 💳 Stripe Configuration (Optional - if using Stripe)

```env
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```

---

## 🚀 For Vercel Deployment

### Required Environment Variables

Add these to **Vercel Dashboard → Settings → Environment Variables:**

```
# Django
SECRET_KEY=django-insecure--1qn5na%ea)^-@n7_!cc+#p$n^38(^b0%3zan2b$ezh^vkh3mi
DEBUG=False
ALLOWED_HOSTS=.vercel.app,forge.tapnex.tech

# Database
DATABASE_URL=postgresql://postgres.wektxjtwsohaisjpayim:aadijain@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
SUPABASE_URL=https://wektxjtwsohaisjpayim.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indla3R4anR3c29oYWlzanBheWltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3NzI4NDEsImV4cCI6MjA3NzM0ODg0MX0.kuPH6aiLNxbhO6XYd3uFj-ZGMqKmsm18z58fz2aY8lI

# Razorpay (CHANGE TO LIVE KEYS IN PRODUCTION)
RAZORPAY_KEY_ID=rzp_test_Rat3BJ8CMAJh83
RAZORPAY_KEY_SECRET=iuCEUkHFhzmBXLZZa6BVTv3C
RAZORPAY_WEBHOOK_SECRET=Prabhav@770jain

# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=325233701971-k0qpv18co8opur874aguuhq1sdarhok4.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=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

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DEFAULT_FROM_EMAIL=support@tapnex.tech
```

---

## 📝 Notes

### ⚠️ Security
- **NEVER** commit `.env` file to Git
- `.env` is already in `.gitignore`
- Keep credentials secure and private

### 🔄 Razorpay Test vs Live
- **Test Mode:** Use for development/testing
  - Keys start with `rzp_test_`
  - Test cards work: `4111 1111 1111 1111`
  
- **Live Mode:** Use for production
  - Keys start with `rzp_live_`
  - Real payments processed
  - Must be KYC verified

### 🔐 Webhook Secret
- **Test Webhook Secret:** `Prabhav@770jain`
- **Production:** Get from Razorpay Dashboard after creating webhook
- Format: `whsec_xxxxxxxxxxxxx`

---

## ✅ Checklist

### Development (.env file)
- [x] Razorpay test keys configured
- [x] Razorpay webhook secret added
- [x] Database connection working
- [x] Google OAuth configured
- [x] Django secret key set

### Production (Vercel)
- [ ] Add all environment variables to Vercel
- [ ] Change DEBUG to False
- [ ] Use live Razorpay keys
- [ ] Update webhook secret (get from Razorpay Dashboard)
- [ ] Configure email backend for production
- [ ] Test all configurations

---

## 🔍 How to Verify

### Check if credentials are loaded:
```bash
cd e:/FGC
python manage.py shell
```

```python
from django.conf import settings

# Check Razorpay
print(f"Razorpay Key ID: {settings.RAZORPAY_KEY_ID[:15]}...")
print(f"Razorpay Secret: {settings.RAZORPAY_KEY_SECRET[:15]}...")
print(f"Webhook Secret: {settings.RAZORPAY_WEBHOOK_SECRET}")

# Check Database
print(f"Database: {settings.DATABASES['default']['NAME']}")

# Check Google OAuth
print(f"Google Client ID: {settings.GOOGLE_OAUTH_CLIENT_ID[:20]}...")
```

---

## 📞 Support

If credentials are not loading:
1. Check `.env` file exists in project root
2. Verify `python-decouple` is installed
3. Restart Django server
4. Check for typos in variable names

---

**Last Updated:** November 2, 2025  
**Status:** ✅ All Credentials Configured
