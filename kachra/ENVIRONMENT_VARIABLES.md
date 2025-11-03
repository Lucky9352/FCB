# 🔐 Environment Variables Reference

## Complete list of all credentials and configuration

---

## 📋 Razorpay Credentials (Payment Gateway)

### Test Mode (Development)
```env
RAZORPAY_KEY_ID=your_test_key_id
RAZORPAY_KEY_SECRET=your_test_key_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
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
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your_supabase_anon_key
DATABASE_URL=postgresql://postgres.your-project-ref:your-password@aws-0-region.pooler.supabase.com:6543/postgres
```

---

## 🔑 Google OAuth (Social Login)

```env
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
```

---

## ⚙️ Django Configuration

```env
SECRET_KEY=your-secret-key-here
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

##  For Vercel Deployment

### Required Environment Variables

Add these to **Vercel Dashboard → Settings → Environment Variables:**

```
# Django
SECRET_KEY=django-insecure--1qn5na%ea)^-@n7_!cc+#p$n^38(^b0%3zan2b$ezh^vkh3mi
DEBUG=False
ALLOWED_HOSTS=.vercel.app,forge.tapnex.tech

# Database
DATABASE_URL=postgresql://postgres.your-project-ref:your-password@aws-0-region.pooler.supabase.com:6543/postgres
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# Razorpay (CHANGE TO LIVE KEYS IN PRODUCTION)
RAZORPAY_KEY_ID=your_test_key_id
RAZORPAY_KEY_SECRET=your_test_key_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret

# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

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
- **Test Webhook Secret:** Get from Razorpay Dashboard when creating webhook
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
