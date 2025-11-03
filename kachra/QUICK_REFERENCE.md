# Quick Reference - Razorpay Whitelisting

## 🚀 What's Been Done

### 1. Branding Implementation ✅
- **TapNex Technologies** branding on all standard pages (home, login, dashboard, policies)
- **Forge Gaming Cafe** branding only on game-related pages (game selection, gaming stations)
- Footer displays: "© 2025 TapNex Technologies | A brand of NEXGEN FC" on all pages

### 2. Policy Pages Created ✅
All required policy pages have been created and are accessible:

| Page | URL | Status |
|------|-----|--------|
| Privacy Policy | /privacy/ | ✅ Ready |
| Terms & Conditions | /terms/ | ✅ Ready |
| Refund Policy | /refund-policy/ | ✅ Ready |
| Contact Us | /contact/ | ✅ Ready |
| About Us | /about/ | ✅ Ready |

### 3. Configuration Updated ✅
- Domain `forge.tapnex.tech` added to `ALLOWED_HOSTS`
- Razorpay configuration added to `settings.py`
- Company information properly configured
- URL routes created for all policy pages

---

## 📋 Quick Action Checklist

### Before Deploying to forge.tapnex.tech

- [ ] Update `.env` file with Razorpay keys:
  ```env
  RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxxx
  RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxx
  ```

- [ ] Ensure domain is properly configured and pointing to your server

- [ ] Verify SSL certificate is installed and working (HTTPS)

- [ ] Test all policy pages are accessible

### After Deploying

- [ ] Visit https://forge.tapnex.tech and verify site is live

- [ ] Check all policy page URLs:
  - https://forge.tapnex.tech/privacy/
  - https://forge.tapnex.tech/terms/
  - https://forge.tapnex.tech/refund-policy/
  - https://forge.tapnex.tech/contact/
  - https://forge.tapnex.tech/about/

- [ ] Verify footer shows correct branding on all pages

- [ ] Test navigation links work correctly

---

## 🔐 Razorpay Whitelisting Application

### Step-by-Step Process

1. **Login to Razorpay Dashboard**
   - Go to: https://dashboard.razorpay.com/
   - Login with your credentials

2. **Navigate to Settings**
   - Click on "Settings" in the sidebar
   - Select "Website and App Settings"

3. **Add Your Domain**
   - Click "Add Domain" or "Website Details"
   - Enter: `forge.tapnex.tech`
   - Select: Production/Live environment

4. **Fill in Business Information**
   ```
   Business Name: TapNex Technologies
   Parent Company: NEXGEN FC
   Business Type: Technology Services / Gaming
   Website URL: https://forge.tapnex.tech
   Support Email: support@tapnex.tech
   ```

5. **Add Policy Page URLs**
   ```
   Privacy Policy: https://forge.tapnex.tech/privacy/
   Terms & Conditions: https://forge.tapnex.tech/terms/
   Refund Policy: https://forge.tapnex.tech/refund-policy/
   Contact: https://forge.tapnex.tech/contact/
   ```

6. **Domain Verification**
   - Choose verification method (DNS, HTML file, or Meta tag)
   - Follow Razorpay's instructions to verify
   - Usually takes a few minutes

7. **Submit for Review**
   - Review all information for accuracy
   - Click "Submit for Review"
   - Wait for approval (1-3 business days)

---

## 📧 Support Email Template

If you need to contact Razorpay support, use this template:

```
Subject: Domain Whitelisting Request - forge.tapnex.tech

Dear Razorpay Support,

I am requesting domain whitelisting for forge.tapnex.tech.

Business Details:
- Company: TapNex Technologies (A brand of NEXGEN FC - Registered Firm)
- Domain: forge.tapnex.tech
- Email: support@tapnex.tech
- Service: Gaming Cafe Booking Platform

All policy pages are live at:
- Privacy: https://forge.tapnex.tech/privacy/
- Terms: https://forge.tapnex.tech/terms/
- Refund: https://forge.tapnex.tech/refund-policy/
- Contact: https://forge.tapnex.tech/contact/

Our refund policy is clearly stated: NO REFUNDS, with one-time rescheduling allowed subject to availability.

Please review and approve.

Best regards,
TapNex Technologies
support@tapnex.tech
```

---

## ⚠️ Important Notes

### Payment Policy (Key Points)
- ✅ **NO REFUNDS** - All payments are final
- ✅ **Rescheduling** - Allowed ONCE only, subject to availability
- ✅ **No Cancellations** - Not permitted under any circumstances
- ✅ **Payment Method** - Razorpay gateway only

### What Razorpay Checks
1. All policy pages are publicly accessible (no login required)
2. Privacy policy mentions payment processor
3. Refund policy is clear and transparent
4. Contact information is accurate
5. Domain has valid SSL certificate
6. Business information is complete

### Common Rejection Reasons
- Policy pages require login/authentication ❌
- Refund policy is vague or missing ❌
- Contact information not provided ❌
- SSL certificate not properly configured ❌
- Domain name mismatch ❌

**All of the above have been properly addressed in your setup ✅**

---

## 🎯 Next Immediate Steps

1. **Deploy your application to forge.tapnex.tech**
2. **Verify HTTPS is working**
3. **Test all policy page links**
4. **Get Razorpay API keys** (if you don't have them yet)
5. **Apply for domain whitelisting** using the steps above

---

## 📞 Contact Information

**TapNex Technologies**
- Email: support@tapnex.tech
- Domain: forge.tapnex.tech
- Parent: NEXGEN FC (Registered Firm)

**Razorpay Support**
- Email: support@razorpay.com
- Phone: +91 76780 80809
- Dashboard: https://dashboard.razorpay.com/

---

## 💡 Pro Tips

1. **Before Applying:** Make sure your site is fully deployed and all links work
2. **Response Time:** Razorpay typically responds within 24-48 hours
3. **Follow-up:** If no response in 3 days, send a follow-up email
4. **Documentation:** Keep this guide handy for reference during application
5. **Testing:** After approval, test thoroughly in test mode first

---

**Created:** November 1, 2025  
**Status:** Implementation Complete - Ready for Deployment
