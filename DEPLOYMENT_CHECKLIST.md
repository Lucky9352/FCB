# Pre-Deployment Checklist for Vercel

## 🎯 Critical Items - MUST BE COMPLETED

### 1. Environment Variables
- [ ] Create `.env` file locally with all required variables (use `.env.example` as template)
- [ ] Set `SECRET_KEY` in Vercel dashboard (generate a new secure key)
- [ ] Set `DEBUG=False` in Vercel dashboard
- [ ] Set `DATABASE_URL` with Supabase PostgreSQL connection string
- [ ] Set `SUPABASE_URL` and `SUPABASE_KEY`
- [ ] Set `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`
- [ ] Set `STRIPE_PUBLISHABLE_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
- [ ] Set `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET`
- [ ] Set `ALLOWED_HOSTS` to include your domain and `.vercel.app`

### 2. Security Review
- [ ] No hardcoded secrets in any Python files
- [ ] No passwords or API keys in code
- [ ] `.env` file is in `.gitignore`
- [ ] `db.sqlite3` is in `.gitignore`
- [ ] Test account passwords removed from production code
- [ ] Default Django SECRET_KEY removed from settings.py
- [ ] DEBUG is False for production

### 3. Code Quality
- [ ] Remove all print statements (use logging instead)
- [ ] Remove test/development comments
- [ ] All imports are used
- [ ] No unused files in repository
- [ ] Remove any local testing scripts

### 4. Database
- [ ] Database migrations are up to date
- [ ] Supabase PostgreSQL is configured and accessible
- [ ] Database connection string is correct
- [ ] Supabase RLS (Row Level Security) policies are set if needed

### 5. Static Files
- [ ] Run `npm run build-css-prod` locally to test
- [ ] Run `python manage.py collectstatic` locally to test
- [ ] Verify `staticfiles/` is in `.gitignore`
- [ ] Verify all CSS/JS files are properly linked in templates

### 6. OAuth Configuration
- [ ] Google OAuth redirect URIs updated with production URLs
- [ ] OAuth consent screen is properly configured
- [ ] Test login flow with Google

### 7. Payment Gateways
- [ ] Razorpay domain whitelisting submitted
- [ ] Razorpay test credentials provided
- [ ] Stripe webhook endpoints configured
- [ ] Test payment flows work

### 8. Git Repository
- [ ] All changes committed
- [ ] Push to main/production branch
- [ ] No sensitive files tracked by git
- [ ] `.gitignore` is properly configured

## 📋 Recommended Items

### 9. Documentation
- [ ] README.md updated with project description
- [ ] API documentation if applicable
- [ ] Setup instructions for new developers

### 10. Testing
- [ ] Test all user flows locally
- [ ] Test booking system
- [ ] Test payment processing (test mode)
- [ ] Test admin dashboard
- [ ] Test email notifications

### 11. Performance
- [ ] Database queries optimized
- [ ] Images optimized
- [ ] Unnecessary dependencies removed from requirements.txt

### 12. Monitoring
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Set up uptime monitoring
- [ ] Configure logging properly

## 🚀 Deployment Steps

1. **Review this checklist** - Ensure all items are completed
2. **Test locally** - Make sure everything works
3. **Commit and push** - Push all changes to GitHub
4. **Import to Vercel** - Connect your GitHub repository
5. **Add environment variables** - Add all required env vars in Vercel dashboard
6. **Deploy** - Trigger the first deployment
7. **Run migrations** - Run database migrations after first deployment
8. **Test production** - Test all features on live site
9. **Configure domain** - Add custom domain in Vercel
10. **Update OAuth** - Update redirect URIs with production domain

## ⚠️ Common Issues & Solutions

### Build Fails
- Check Node.js version in `package.json`
- Verify all Python dependencies are in `requirements.txt`
- Check build logs for specific errors

### Static Files Not Loading
- Verify `STATIC_ROOT` and `STATIC_URL` in settings.py
- Check `vercel.json` routes configuration
- Run `collectstatic` again

### Database Connection Error
- Verify `DATABASE_URL` is correct
- Check Supabase connection limits
- Ensure IP whitelisting allows Vercel

### OAuth Not Working
- Verify redirect URIs match exactly (including trailing slash)
- Check that OAuth credentials are correct
- Ensure domain is properly configured

### 500 Internal Server Error
- Check Vercel function logs
- Verify all environment variables are set
- Check for missing dependencies
- Review Django error logs

## 📞 Support Contacts

- **Vercel Support:** https://vercel.com/support
- **Django Documentation:** https://docs.djangoproject.com/
- **Project Support:** support@tapnex.tech

---

**Last Updated:** November 1, 2025  
**Version:** 1.0
