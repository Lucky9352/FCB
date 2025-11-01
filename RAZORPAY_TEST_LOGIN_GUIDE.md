# Razorpay Testing - Customer Login Guide

## Problem Solved
Previously, the website only had Google OAuth login, which made it difficult for Razorpay testers to use the provided username/password credentials.

## Solution Implemented
✅ **Added Traditional Email/Password Login** alongside Google OAuth on the customer login page.

---

## For Razorpay Testers

### How to Login with Test Credentials

1. **Visit the Customer Login Page**
   - URL: `https://your-domain.com/accounts/login/`
   - Or click "Get Started" or "Customer Login" from the homepage

2. **Choose Login Method**
   - **Option 1: Google OAuth** (Continue with Google button)
   - **Option 2: Email/Password Login** (Use the form below the divider)

3. **Use Test Credentials**
   ```
   Username/Email: [Your provided username]
   Password: [Your provided password]
   ```

4. **After Login**
   - You'll be redirected to the Customer Dashboard
   - You can now test all booking and payment features
   - Make test bookings and verify Razorpay integration

---

## Creating Test Accounts

### Option 1: Using Django Admin
```bash
python manage.py createsuperuser
# Then create users from admin panel at /admin/
```

### Option 2: Using Django Shell
```python
from django.contrib.auth.models import User
from authentication.models import Customer

# Create a test user
user = User.objects.create_user(
    username='razorpay_tester',
    email='tester@razorpay.com',
    password='TestPassword123!',
    first_name='Razorpay',
    last_name='Tester'
)

# Create customer profile
customer = Customer.objects.create(user=user)
```

---

## Features Available for Testing

### ✅ Customer Features
- **Game Selection**: Browse available games
- **Slot Booking**: Book gaming stations with time slots
- **Payment Integration**: Test Razorpay payment gateway
- **Booking Management**: View and cancel bookings
- **Real-time Updates**: Receive booking notifications
- **Receipt Generation**: Download booking receipts

### 🔒 Staff/Admin Login (Separate)
- Staff should use: `/accounts/cafe-owner/login/`
- Admin access: `/admin/`

---

## Login Page Features

### Google OAuth Login (Primary)
- One-click sign-in with Google account
- Automatic profile creation
- Secure authentication

### Email/Password Login (For Testing)
- Traditional form-based login
- Username or email accepted
- Customer profile auto-created if needed

---

## User Display Fixed
✅ **Removed debug output** - The navbar now properly displays:
- User's first name (if available)
- Username (fallback)
- Profile avatar (if uploaded)

Previously showed: `{'user': <User: username>}`
Now shows: Clean name display

---

## Security Notes

1. **Test Credentials**: Only share test credentials with authorized Razorpay team
2. **Production**: Consider disabling email/password login in production if only OAuth is desired
3. **Password Requirements**: Ensure test passwords meet Django's validation rules
4. **Two-Factor Auth**: Can be added for enhanced security if needed

---

## Testing Checklist for Razorpay

- [ ] Login with provided test credentials
- [ ] Browse available games
- [ ] Select a game and time slot
- [ ] Proceed to payment
- [ ] Test Razorpay payment flow (test mode)
- [ ] Verify booking confirmation
- [ ] Check email notifications
- [ ] View booking in dashboard
- [ ] Test booking cancellation
- [ ] Verify refund process
- [ ] Check receipt generation

---

## Troubleshooting

### Cannot Login?
1. Verify username/password are correct
2. Check if user account exists in database
3. Ensure customer profile is created for the user
4. Check Django logs for authentication errors

### No Customer Profile?
The system automatically creates a customer profile if:
- User logs in via Google OAuth
- User logs in via email/password

### Still Having Issues?
Contact: support@tapnex.com or check the server logs

---

## Technical Details

### Files Modified
1. `templates/authentication/customer_login.html` - Added email/password form
2. `authentication/views.py` - Added `customer_email_login_view` handler
3. `authentication/urls.py` - Added URL pattern for email login
4. `templates/base.html` - Fixed user display in navigation

### Authentication Flow
```
Customer Login Page
    ↓
Google OAuth OR Email/Password
    ↓
Authenticate User
    ↓
Check/Create Customer Profile
    ↓
Redirect to Dashboard
```

---

## Contact & Support

For any issues or questions regarding the testing process:
- **Email**: support@tapnex.com
- **Developer**: Check logs at `/var/log/django/`
- **Admin Panel**: `/admin/` (superuser access required)

---

**Last Updated**: January 2025
**Version**: 1.0
**Status**: Ready for Razorpay Testing ✅
