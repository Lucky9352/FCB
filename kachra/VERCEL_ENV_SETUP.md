# Environment Variables Template for Vercel

Copy these to your Vercel Dashboard under Settings > Environment Variables

## Required for ALL Environments (Production, Preview, Development)

```
SECRET_KEY=
DEBUG=False
ALLOWED_HOSTS=forge.tapnex.tech,.vercel.app
DATABASE_URL=
SUPABASE_URL=
SUPABASE_KEY=
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=
```

## Optional (with defaults)

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DEFAULT_FROM_EMAIL=noreply@tapnex.tech
```

## How to Get Each Value

### SECRET_KEY
Run: `python generate_secret_key.py`
Copy the generated key

### DEBUG
Set to: `False` (for production)
Set to: `True` (for development/preview only if needed)

### ALLOWED_HOSTS
Production: `forge.tapnex.tech,.vercel.app`
Development: `localhost,127.0.0.1,.vercel.app`

### DATABASE_URL (Supabase)
Format: `postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres`
Get from: Supabase Dashboard > Project Settings > Database > Connection String (URI)

### SUPABASE_URL
Format: `https://[YOUR-PROJECT-REF].supabase.co`
Get from: Supabase Dashboard > Project Settings > API > Project URL

### SUPABASE_KEY
Get from: Supabase Dashboard > Project Settings > API > Project API keys > anon/public key

### RAZORPAY_KEY_ID
Format: `rzp_test_...` or `rzp_live_...`
Get from: Razorpay Dashboard > Settings > API Keys

### RAZORPAY_KEY_SECRET
Get from: Razorpay Dashboard > Settings > API Keys (shown when generating new key)

### GOOGLE_OAUTH_CLIENT_ID
Format: `...apps.googleusercontent.com`
Get from: Google Cloud Console > APIs & Services > Credentials

### GOOGLE_OAUTH_CLIENT_SECRET
Get from: Google Cloud Console > APIs & Services > Credentials

## Quick Copy-Paste for Vercel CLI

If using Vercel CLI, you can set env vars like this:

```bash
vercel env add SECRET_KEY
vercel env add DATABASE_URL
vercel env add SUPABASE_URL
vercel env add SUPABASE_KEY
vercel env add RAZORPAY_KEY_ID
vercel env add RAZORPAY_KEY_SECRET
vercel env add GOOGLE_OAUTH_CLIENT_ID
vercel env add GOOGLE_OAUTH_CLIENT_SECRET
```

Then follow the prompts to enter each value.
