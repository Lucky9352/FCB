# 🎮 TapNex - Razorpay Testing Quick Reference

## 🔐 Test Login Credentials

### Customer Login (For Payment Testing)
```
URL: https://your-domain.com/accounts/login/

Method 1 - Email/Password:
  Username: razorpay_tester
  Password: TestPass123!

Method 2 - Google OAuth:
  Click "Continue with Google" button
```

### Admin/Staff Login (Backend Access)
```
Staff URL: https://your-domain.com/accounts/cafe-owner/login/
Admin URL: https://your-domain.com/admin/

[Your admin credentials here]
```

---

## 🧪 Quick Test Workflow

1. **Login** → Use credentials above
2. **Browse Games** → Select any available game
3. **Choose Slot** → Pick a time slot
4. **Proceed to Payment** → Click "Book Now"
5. **Razorpay Checkout** → Opens payment modal
6. **Test Payment** → Use Razorpay test cards
7. **Verify Booking** → Check dashboard for confirmation

---

## 💳 Razorpay Test Cards

### Success Scenarios
```
Card: 4111 1111 1111 1111
CVV: Any 3 digits
Expiry: Any future date
Name: Any name
```

### Failure Scenarios
```
Card: 4000 0000 0000 0002 (Generic failure)
Card: 4000 0000 0000 9995 (Insufficient funds)
```

### UPI Test
```
VPA: success@razorpay
```

---

## 🎯 What to Test

### ✅ Core Features
- [ ] User registration/login (both methods)
- [ ] Browse available games
- [ ] Select game and time slot
- [ ] Razorpay payment integration
- [ ] Booking confirmation
- [ ] Email notifications
- [ ] Booking history
- [ ] Cancellation & refunds
- [ ] Receipt generation

### ✅ Payment Flows
- [ ] Successful payment
- [ ] Failed payment handling
- [ ] Payment timeout
- [ ] Duplicate payment prevention
- [ ] Refund processing
- [ ] Webhook handling

---

## 📧 Contact Information

### Business Details
```
Business Name: TapNex Technologies
Brand: NEXGEN FC
Category: Entertainment & Gaming
Website: [Your domain]
Support Email: support@tapnex.com
```

### Technical Contact
```
Developer: [Your name]
Email: [Your email]
Phone: [Your phone]
```

---

## 🔗 Important URLs

```
Homepage: https://your-domain.com/
Customer Login: https://your-domain.com/accounts/login/
Staff Login: https://your-domain.com/accounts/cafe-owner/login/
Admin Panel: https://your-domain.com/admin/
Privacy Policy: https://your-domain.com/privacy/
Terms & Conditions: https://your-domain.com/terms/
Refund Policy: https://your-domain.com/refund-policy/
```

---

## 📱 Features Implemented

### Customer Features
✅ Google OAuth & Email/Password Login
✅ Game browsing and filtering
✅ Real-time slot availability
✅ Razorpay payment integration
✅ Booking management
✅ Real-time notifications
✅ Email confirmations
✅ Receipt generation
✅ Booking history
✅ Cancellation & refunds

### Admin Features
✅ TapNex super admin dashboard
✅ Cafe owner management
✅ Commission settings
✅ Revenue reports
✅ System analytics
✅ Game management
✅ Slot management
✅ Booking oversight

---

## 🚀 Production Checklist

### Before Going Live
- [ ] Update Razorpay keys (Test → Live)
- [ ] Configure webhook URLs
- [ ] Test live payment flows
- [ ] Verify email notifications
- [ ] Check SSL certificate
- [ ] Review security settings
- [ ] Test on mobile devices
- [ ] Load testing
- [ ] Backup database
- [ ] Monitor error logs

---

## 📊 API Integration Details

### Razorpay Webhooks
```
Endpoint: /booking/razorpay-webhook/
Events: payment.captured, payment.failed, refund.processed
Authentication: Webhook signature verification
```

### Payment Flow
```
1. User selects slot → Creates booking (PENDING)
2. Razorpay order created → Order ID generated
3. Payment modal opens → User pays
4. Webhook received → Booking status updated
5. Confirmation sent → Email + SMS notification
```

---

## 🐛 Common Issues & Solutions

### Issue: Login not working
**Solution**: Verify user exists and customer profile is created

### Issue: Payment not completing
**Solution**: Check webhook configuration and logs

### Issue: Email not sending
**Solution**: Verify SMTP settings in Django settings

### Issue: Slots not showing
**Solution**: Ensure games and slots are created in admin

---

## 📞 Support Contacts

### During Testing Phase
- **Technical Issues**: [Your email]
- **Account Issues**: Create test users via script
- **Payment Issues**: Check Razorpay dashboard logs

### For Razorpay Team
- **Questions**: support@tapnex.com
- **Emergency**: [Your phone]
- **Documentation**: See RAZORPAY_APPLICATION_DATA.md

---

## 🎉 Ready to Test!

Everything is set up and ready for Razorpay testing. Use the credentials above to login and test all payment flows.

**Good Luck! 🚀**

---

**Last Updated**: January 2025  
**Status**: ✅ Ready for Testing  
**Version**: 1.0
