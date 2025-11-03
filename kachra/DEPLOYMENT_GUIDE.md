# Deployment Guide for Vercel

## 🚀 Quick Deployment Steps

### 1. Prerequisites
- Vercel account (sign up at https://vercel.com)
- GitHub repository with your code
- All required API keys and credentials ready

### 2. Environment Variables Setup

Before deploying, you need to set up the following environment variables in Vercel Dashboard:

#### Required Environment Variables

```bash
# Django Configuration
SECRET_KEY=<generate-a-secure-secret-key>
DEBUG=False
ALLOWED_HOSTS=forge.tapnex.tech,.vercel.app

# Database (Supabase PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DEFAULT_FROM_EMAIL=noreply@tapnex.tech

# Stripe Payment
STRIPE_PUBLISHABLE_KEY=pk_test_or_live_key
STRIPE_SECRET_KEY=sk_test_or_live_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Razorpay Payment
RAZORPAY_KEY_ID=rzp_test_or_live_key
RAZORPAY_KEY_SECRET=your_razorpay_secret

# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-google-secret
```

### 3. Deploy to Vercel

#### Option A: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

#### Option B: Via Vercel Dashboard

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Configure the project:
   - **Framework Preset:** Other
   - **Build Command:** `bash build_files.sh`
   - **Output Directory:** `staticfiles_build`
4. Add all environment variables from the list above
5. Click "Deploy"

### 4. Post-Deployment Steps

#### A. Run Database Migrations

```bash
# Using Vercel CLI
vercel env pull .env.local
python manage.py migrate
```

Or set up a GitHub Action to run migrations automatically.

#### B. Create Superuser (if needed)

```bash
python manage.py createsuperuser
```

#### C. Create Test Users (Optional)

```bash
# For cafe owner and TapNex admin
python manage.py create_test_users

# For Razorpay verification
python manage.py create_razorpay_test_customer
```

### 5. Configure Custom Domain

1. Go to Vercel Dashboard > Your Project > Settings > Domains
2. Add your custom domain: `forge.tapnex.tech`
3. Follow Vercel's instructions to update your DNS records
4. Wait for DNS propagation (usually 24-48 hours)

### 6. Update OAuth Redirect URIs

After deployment, update your OAuth settings:

#### Google OAuth Console
1. Go to https://console.cloud.google.com/
2. Select your project
3. Navigate to APIs & Services > Credentials
4. Add authorized redirect URIs:
   - `https://forge.tapnex.tech/accounts/google/login/callback/`
   - `https://your-project.vercel.app/accounts/google/login/callback/`

#### Razorpay Dashboard
1. Login to https://dashboard.razorpay.com/
2. Go to Settings > Website and App Settings
3. Add your domain: `https://forge.tapnex.tech`
4. Submit all required policy pages and test credentials

### 7. Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` configured
- [ ] All API keys are environment variables
- [ ] HTTPS enabled (automatic on Vercel)
- [ ] CSRF protection enabled
- [ ] Secure cookies configured
- [ ] Database backups configured
- [ ] `.env` file in `.gitignore`

### 8. Testing Your Deployment

1. Visit your live URL
2. Test user registration and login
3. Test Google OAuth login
4. Test booking flow
5. Test payment processing (use test mode)
6. Check admin panel access
7. Verify email notifications

### 9. Monitoring & Logs

- **Vercel Logs:** Dashboard > Your Project > Deployments > View Function Logs
- **Error Tracking:** Consider integrating Sentry or similar service
- **Uptime Monitoring:** Set up uptime monitoring (UptimeRobot, Pingdom, etc.)

### 10. Troubleshooting

#### Static Files Not Loading
```bash
python manage.py collectstatic --noinput --clear
```

#### Database Connection Issues
- Verify `DATABASE_URL` is correct
- Check Supabase connection limits
- Ensure IP whitelisting is configured

#### OAuth Issues
- Verify redirect URIs match exactly
- Check that OAuth credentials are correct
- Ensure site domain is configured in Django admin

#### Build Failures
- Check Node.js version compatibility
- Verify all dependencies are in requirements.txt
- Review build logs in Vercel dashboard

---

## 📞 Support

For issues or questions:
- Email: support@tapnex.tech
- GitHub Issues: Create an issue in the repository

---

## 🔄 Continuous Deployment

Every push to the `main` branch will automatically trigger a new deployment on Vercel.

To disable auto-deployment:
1. Go to Project Settings > Git
2. Toggle "Production Branch" settings

---

*Last Updated: November 1, 2025*
