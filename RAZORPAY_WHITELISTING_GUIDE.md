# Razorpay Domain Whitelisting Guide

## Overview
This guide contains all the information needed to register and whitelist your domain `forge.tapnex.tech` with Razorpay for payment processing.

---

## 🏢 Company Information

### Business Details
- **Company Name:** TapNex Technologies
- **Parent Company:** NEXGEN FC (Registered Firm)
- **Domain:** forge.tapnex.tech
- **Email:** support@tapnex.tech
- **Registered Address:**  
  H. no. 770/2 near Arihant Hospital, Dr Vivek Jain,  
  Ankur Colony, Makroniya, Sagar,  
  Madhya Pradesh - 470004, India

### Platform Purpose
Gaming cafe booking platform for Forge Gaming Cafe, powered by TapNex Technologies

---

## 📋 Razorpay Whitelisting Requirements

### 1. Mandatory Policy Pages (Already Created ✓)

All policy pages are accessible on your domain and include:

#### Privacy Policy
- **URL:** https://forge.tapnex.tech/privacy/
- **Content:** Data collection, usage, security, and user rights
- **Status:** ✅ Created and accessible

#### Terms & Conditions
- **URL:** https://forge.tapnex.tech/terms/
- **Content:** Platform usage terms, booking policies, responsibilities
- **Status:** ✅ Created and accessible

#### Refund & Cancellation Policy
- **URL:** https://forge.tapnex.tech/refund-policy/
- **Content:** 
  - **NO REFUNDS POLICY** - All bookings are final
  - Rescheduling allowed **ONCE** only, subject to availability
  - No cancellations permitted
- **Status:** ✅ Created and accessible

#### Contact Us
- **URL:** https://forge.tapnex.tech/contact/
- **Content:** Support email and business contact information
- **Status:** ✅ Created and accessible

#### About Us
- **URL:** https://forge.tapnex.tech/about/
- **Content:** Company information and mission
- **Status:** ✅ Created and accessible

---

## 🔐 Steps to Apply for Razorpay Domain Whitelisting

### Step 1: Access Razorpay Dashboard
1. Login to your Razorpay account at https://dashboard.razorpay.com/
2. Navigate to **Settings** → **Website and App Settings**

### Step 2: Add Domain
1. Click on **"Add Domain"** or **"Website Details"**
2. Enter your domain: `forge.tapnex.tech`
3. Select domain type: **Production/Live**

### Step 3: Provide Required Information

#### Business Information
```
Business Name: TapNex Technologies
Parent Company: NEXGEN FC
Business Type: Technology/Gaming Services
Website: https://forge.tapnex.tech
Support Email: support@tapnex.tech
```

#### Policy Pages URLs
```
Privacy Policy: https://forge.tapnex.tech/privacy/
Terms & Conditions: https://forge.tapnex.tech/terms/
Refund/Cancellation Policy: https://forge.tapnex.tech/refund-policy/
Contact Us: https://forge.tapnex.tech/contact/
About Us: https://forge.tapnex.tech/about/
```

### Step 4: Verify Domain Ownership
Razorpay may require one of these verification methods:
- **DNS TXT Record:** Add a TXT record to your domain DNS
- **HTML File Upload:** Upload a verification HTML file to your website
- **Meta Tag:** Add a meta tag to your website header

### Step 5: Submit for Review
1. Review all entered information
2. Ensure all policy pages are accessible and properly formatted
3. Submit the whitelisting request
4. Wait for Razorpay approval (typically 1-3 business days)

---

## ✅ Pre-Whitelisting Checklist

Before submitting your whitelisting request, ensure:

- [ ] Domain `forge.tapnex.tech` is live and accessible
- [ ] SSL certificate is properly configured (HTTPS)
- [ ] All policy pages are accessible without authentication
- [ ] Privacy policy mentions Razorpay as payment processor
- [ ] Terms & Conditions clearly state booking terms
- [ ] Refund policy is clear (NO REFUNDS, RESCHEDULING ONCE)
- [ ] Contact information is accurate and functional
- [ ] Company branding is consistent across all pages
- [ ] Footer displays "© 2025 TapNex Technologies | A brand of NEXGEN FC"

---

## 🔧 Technical Configuration

### Environment Variables Required
Add these to your `.env` file:

```env
# Razorpay Configuration
RAZORPAY_KEY_ID=your_razorpay_key_id_here
RAZORPAY_KEY_SECRET=your_razorpay_key_secret_here

# Domain Configuration
ALLOWED_HOSTS=localhost,127.0.0.1,forge.tapnex.tech

# Company Information
COMPANY_EMAIL=support@tapnex.tech
COMPANY_DOMAIN=forge.tapnex.tech
```

### Django Settings (Already Configured ✓)
The following settings have been added to `settings.py`:

```python
# Razorpay Configuration
RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID', default='')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET', default='')

# Company Information
COMPANY_NAME = 'TapNex Technologies'
COMPANY_PARENT = 'NEXGEN FC'
COMPANY_EMAIL = 'support@tapnex.tech'
COMPANY_DOMAIN = 'forge.tapnex.tech'
COMPANY_ADDRESS = 'H. no. 770/2 near Arihant Hospital, Dr Vivek Jain, Ankur Colony, Makroniya, Sagar, (Madhya Pradesh) 470004, India'
```

---

## 📧 Communication with Razorpay

### Sample Email for Support Queries

```
Subject: Domain Whitelisting Request - forge.tapnex.tech

Dear Razorpay Support Team,

I am requesting domain whitelisting for my production website forge.tapnex.tech.

Business Details:
- Business Name: TapNex Technologies (Powered by NEXGEN FC)
- Domain: forge.tapnex.tech
- Support Email: support@tapnex.tech
- Business Type: Gaming Cafe Booking Platform

All mandatory policy pages are live and accessible:
- Privacy Policy: https://forge.tapnex.tech/privacy/
- Terms & Conditions: https://forge.tapnex.tech/terms/
- Refund Policy: https://forge.tapnex.tech/refund-policy/
- Contact Us: https://forge.tapnex.tech/contact/

Please review and approve the whitelisting request.

Best regards,
TapNex Technologies
support@tapnex.tech
```

---

## 🚨 Common Razorpay Whitelisting Rejections & Solutions

### Issue 1: Policy Pages Not Accessible
**Solution:** Ensure all URLs are publicly accessible without login requirements

### Issue 2: Incomplete Refund Policy
**Solution:** Clearly state your NO REFUND policy with all conditions (Already done ✓)

### Issue 3: Contact Information Missing
**Solution:** Ensure support email and business address are visible (Already done ✓)

### Issue 4: Domain Mismatch
**Solution:** Ensure the domain in Razorpay matches exactly: `forge.tapnex.tech`

### Issue 5: SSL Certificate Issues
**Solution:** Verify HTTPS is working properly on your domain

---

## 🎯 Post-Whitelisting Steps

After Razorpay approves your domain:

1. **Test Payment Integration**
   - Create test bookings
   - Verify payment flows
   - Test refund scenarios (if applicable)

2. **Update Razorpay Keys**
   - Replace test keys with live keys in `.env`
   - Restart your application

3. **Monitor Transactions**
   - Check Razorpay dashboard regularly
   - Set up webhook notifications
   - Monitor for failed payments

4. **Compliance**
   - Keep policy pages updated
   - Respond to customer queries promptly
   - Maintain accurate records

---

## 📞 Support Contacts

### Razorpay Support
- **Email:** support@razorpay.com
- **Phone:** +91 76780 80809
- **Dashboard:** https://dashboard.razorpay.com/

### TapNex Technologies
- **Support Email:** support@tapnex.tech
- **Domain:** forge.tapnex.tech

---

## 📝 Notes

### Branding Strategy
- **TapNex Technologies:** Used on all authentication, dashboard, and policy pages
- **Forge Gaming Cafe:** Used only on game selection and gaming stations pages
- **Footer:** Always shows "© 2025 TapNex Technologies | A brand of NEXGEN FC"

### Payment Policy
- All payments are processed through Razorpay payment gateway
- NO REFUNDS once payment is confirmed
- Rescheduling allowed ONCE, subject to slot availability
- No cancellations permitted under any circumstances

---

## ✨ Implementation Status

- ✅ Domain configured in settings.py
- ✅ Razorpay configuration added to settings.py
- ✅ Privacy Policy created and accessible
- ✅ Terms & Conditions created and accessible
- ✅ Refund Policy created and accessible
- ✅ Contact page created and accessible
- ✅ About page created and accessible
- ✅ Footer updated with proper branding
- ✅ Navigation updated with policy links
- ✅ Company information properly displayed

### Next Steps
1. Deploy application to forge.tapnex.tech
2. Verify all policy pages are accessible via HTTPS
3. Apply for Razorpay domain whitelisting
4. Add Razorpay keys to environment variables
5. Test payment integration thoroughly

---

**Document Created:** November 1, 2025  
**Last Updated:** November 1, 2025  
**Version:** 1.0
