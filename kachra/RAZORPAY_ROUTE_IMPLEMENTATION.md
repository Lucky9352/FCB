# Razorpay Route (Transfer) Implementation - Complete Guide

**Implementation Date**: November 3, 2025  
**Status**: ✅ COMPLETE - Ready for Testing

---

## 🎯 Overview

Implemented Razorpay Route (Transfer) functionality to automatically split payments between platform and cafe owner with the following structure:

### Payment Split Breakdown

**Example: ₹100 Booking**

| Component | Amount | Who Pays/Receives |
|-----------|--------|-------------------|
| **Booking Amount** | ₹100.00 | Base price |
| **Platform Fee (2%)** | + ₹2.00 | **User pays** (added to total) |
| **Total Charged to User** | **₹102.00** | **Customer pays this** |
| | | |
| **Commission (7%)** | - ₹7.00 | Deducted from owner |
| **Owner Receives** | **₹93.00** | **Owner gets this** |

---

## 📊 Implementation Summary

### ✅ Phase 1: Database Schema Updates

**Modified Models:**

1. **CafeOwner Model** (`authentication/models.py`)
   - ✅ `razorpay_account_id` - Stores Razorpay Account/Route ID
   - ✅ `razorpay_account_email` - Account email
   - ✅ `razorpay_account_status` - PENDING/ACTIVE/SUSPENDED

2. **Booking Model** (`booking/models.py`)
   - ✅ `commission_amount` - 7% commission deducted
   - ✅ `owner_payout` - Net amount transferred to owner
   - ✅ `razorpay_transfer_id` - Transfer transaction ID
   - ✅ `transfer_status` - PENDING/PROCESSED/FAILED
   - ✅ `transfer_processed_at` - Transfer timestamp

**Migrations:**
- ✅ `authentication/migrations/0004_cafeowner_razorpay_account_email_and_more.py`
- ✅ `booking/migrations/0006_booking_commission_amount_booking_owner_payout_and_more.py`

---

### ✅ Phase 2: Razorpay Service Extensions

**File**: `booking/razorpay_service.py`

**New Methods:**

1. **`calculate_payment_split()`** ✅
   - Calculates booking amount, platform fee, commission, and owner payout
   - Returns complete breakdown for transparency

2. **`create_order_with_transfer()`** ✅
   - Creates Razorpay order with optional transfer configuration
   - Includes owner payout in order notes
   - Supports both immediate and post-payment transfers

3. **`create_transfer()`** ✅
   - Creates manual transfer to owner's account
   - Used when transfer not included in order creation
   - Includes detailed notes for tracking

4. **`fetch_transfer()`** ✅
   - Retrieves transfer status and details
   - Used for monitoring and troubleshooting

---

### ✅ Phase 3: Payment Flow Updates

**File**: `booking/payment_views.py`

**Modified Functions:**

1. **`create_razorpay_order()`** ✅
   - Calculates payment split using commission (7%) and platform fee (2%)
   - Updates booking with all calculated amounts
   - Creates order with transfer configuration if owner account is set
   - Falls back to manual transfer if account not configured

2. **`verify_razorpay_payment()`** ✅
   - Verifies payment signature
   - Creates transfer to owner if not done during order creation
   - Updates transfer status (PROCESSED/FAILED)
   - Sends notifications including transfer status

3. **Webhook Handlers** ✅
   - `handle_transfer_processed()` - Marks transfer as successful
   - `handle_transfer_failed()` - Logs failure and alerts
   - `handle_transfer_reversed()` - Handles reversal scenarios

---

### ✅ Phase 4: Settings UI

**File**: `templates/authentication/system_settings.html`

**New Section Added:**
- 💳 Razorpay Route Configuration panel
- Input field for Razorpay Account ID
- Email field for account verification
- Visual payment split breakdown with example
- Account status indicator
- Commission and platform fee display

**Location**: https://forge.tapnex.tech/accounts/tapnex/settings/

---

### ✅ Phase 5: Backend Settings Handler

**File**: `authentication/superuser_views.py`

**Modified Function**: `system_settings()` ✅
- Handles `update_razorpay` action
- Saves account ID and email
- Auto-sets status to ACTIVE when account configured
- Validates cafe owner exists

---

### ✅ Phase 6: Owner Dashboard Revenue Updates

**File**: `authentication/dashboard_views.py`

**All revenue metrics now use `owner_payout` instead of `total_amount`:**

1. **`owner_overview()`** ✅
   - Today's revenue = Sum of owner_payout
   - Yesterday's revenue comparison
   - Shows what owner actually receives

2. **`owner_revenue()`** ✅
   - Total revenue = owner's net after commission
   - Gross revenue displayed for reference
   - Commission breakdown visible
   - All charts use owner_payout

3. **`owner_customers()`** ✅
   - Customer lifetime value uses owner_payout
   - VIP threshold based on owner revenue
   - Total spent shows owner earnings

4. **`owner_reports()`** ✅
   - Average booking value = owner_payout
   - Revenue trends use owner earnings
   - Customer LTV calculated from owner_payout

---

## 🔧 Configuration Steps

### Step 1: Set Up Razorpay Route Account

1. Log into Razorpay Dashboard
2. Go to **Settings → Route**
3. Enable Razorpay Route (may require approval)
4. Create a Linked Account for the cafe owner or use existing account ID
5. Copy the Account ID (format: `acc_xxxxx` or `route_xxxxx`)

### Step 2: Configure in Application

1. Navigate to: https://forge.tapnex.tech/accounts/tapnex/settings/
2. Scroll to "💳 Razorpay Route Configuration"
3. Enter the **Razorpay Account ID**
4. Enter the **Account Email**
5. Click **Save Razorpay Settings**
6. Status will change to "ACTIVE"

### Step 3: Test Payment Flow

1. Create a test booking
2. Complete payment as a customer
3. Verify in booking details:
   - `owner_payout` is calculated correctly
   - `commission_amount` = 7% of booking
   - `transfer_status` = PROCESSED
   - `razorpay_transfer_id` is present

### Step 4: Verify Owner Dashboard

1. Log in as cafe owner
2. Check dashboard revenue shows owner_payout amounts
3. Example: ₹100 booking should show as ₹93 revenue
4. Commission deducted should be visible

---

## 💡 Payment Flow Diagram

```
Customer Booking (₹100)
         ↓
Calculate Split:
  - Platform Fee: ₹2 (added)
  - Total to charge: ₹102
         ↓
Customer Pays ₹102
         ↓
Razorpay Processes Payment
         ↓
    [Split Happens]
         ├─→ Platform keeps: ₹2 (platform fee) + ₹7 (commission) = ₹9
         └─→ Owner receives: ₹93 (via Route Transfer)
```

---

## 📊 Database Fields Reference

### Booking Model Fields

| Field | Type | Purpose | Example |
|-------|------|---------|---------|
| `subtotal` | Decimal | Base booking price | ₹100.00 |
| `platform_fee` | Decimal | 2% fee (user pays) | ₹2.00 |
| `total_amount` | Decimal | What user pays | ₹102.00 |
| `commission_amount` | Decimal | 7% from owner | ₹7.00 |
| `owner_payout` | Decimal | What owner gets | ₹93.00 |
| `razorpay_transfer_id` | String | Transfer ID | `trf_xxxxx` |
| `transfer_status` | String | Status | PROCESSED |
| `transfer_processed_at` | DateTime | When transferred | 2025-11-03 10:30 |

### CafeOwner Model Fields

| Field | Type | Purpose | Example |
|-------|------|---------|---------|
| `razorpay_account_id` | String | Account/Route ID | `acc_ABC123` |
| `razorpay_account_email` | Email | Account email | owner@cafe.com |
| `razorpay_account_status` | String | Account status | ACTIVE |

---

## 🧪 Testing Checklist

- [ ] Configure Razorpay Account ID in settings
- [ ] Create test booking for ₹100
- [ ] Verify user is charged ₹102
- [ ] Check booking shows:
  - [ ] `owner_payout = ₹93`
  - [ ] `commission_amount = ₹7`
  - [ ] `platform_fee = ₹2`
  - [ ] `transfer_status = PROCESSED`
- [ ] Verify owner dashboard shows ₹93 revenue (not ₹102)
- [ ] Check Razorpay dashboard shows transfer to owner account
- [ ] Test webhook for transfer.processed event
- [ ] Test failed transfer scenario

---

## 🚨 Webhook Configuration

**Required Webhooks:**

1. **payment.captured** - Already configured
2. **transfer.processed** - ✅ NEW - Confirms transfer success
3. **transfer.failed** - ✅ NEW - Alerts on transfer failure
4. **transfer.reversed** - ✅ NEW - Handles reversal

**Webhook URL**: `https://forge.tapnex.tech/booking/payment/webhook/`

---

## 📈 Owner Dashboard Changes

### Before Implementation:
- Revenue showed `total_amount` (₹102 for ₹100 booking)
- Included platform fee in owner's revenue
- No commission tracking

### After Implementation:
- Revenue shows `owner_payout` (₹93 for ₹100 booking)
- Accurate representation of owner earnings
- Commission and platform fee visible separately
- All metrics (daily, weekly, monthly) use owner_payout

---

## 🔐 Security Considerations

1. ✅ Transfer only created after payment verification
2. ✅ Webhook signature verification enabled
3. ✅ Database transactions for atomic updates
4. ✅ Transfer status tracking for audit trail
5. ✅ Detailed logging of all transfer operations

---

## 📝 Code Changes Summary

| File | Changes | Lines Modified |
|------|---------|----------------|
| `authentication/models.py` | Added Razorpay fields to CafeOwner | ~25 |
| `booking/models.py` | Added transfer tracking to Booking | ~35 |
| `booking/razorpay_service.py` | Added transfer methods | ~200 |
| `booking/payment_views.py` | Updated payment flow & webhooks | ~150 |
| `authentication/superuser_views.py` | Added settings handler | ~20 |
| `authentication/dashboard_views.py` | Updated revenue calculations | ~80 |
| `templates/authentication/system_settings.html` | Added UI panel | ~120 |

**Total**: ~630 lines of code

---

## 🎓 Revenue Metrics Guide

### Owner's Perspective (Dashboard)
- **Today's Revenue**: Sum of `owner_payout` for today
- **Monthly Revenue**: Sum of `owner_payout` for month
- **Per Booking**: Shows `owner_payout` amount
- **Customer LTV**: Based on `owner_payout` across all bookings

### Platform's Perspective (TapNex Admin)
- **Platform Fee Revenue**: Sum of `platform_fee`
- **Commission Revenue**: Sum of `commission_amount`
- **Total Platform Earnings**: Platform Fee + Commission
- **Gross GMV**: Sum of `total_amount`

---

## ⚙️ Configuration Variables

### Commission Settings
- **Commission Rate**: 7% (Fixed)
- **Platform Fee**: 2% (Configurable in TapNex settings)
- **Platform Fee Type**: PERCENT or FIXED

### Transfer Settings
- **Transfer Method**: Automatic via Razorpay Route
- **Fallback**: Manual transfer if Route not configured
- **Retry**: Automatic on webhook for failed transfers

---

## 📞 Support & Troubleshooting

### Common Issues

**Issue 1**: Transfer shows as FAILED
- **Solution**: Check Razorpay account status is ACTIVE
- Verify account ID format is correct
- Check Razorpay Route is enabled on account

**Issue 2**: Owner dashboard shows wrong revenue
- **Solution**: Ensure all bookings have `owner_payout` calculated
- Run migration to set default values for existing bookings
- Recalculate using: `booking.owner_payout = booking.subtotal * 0.93`

**Issue 3**: Transfer not created
- **Solution**: Verify `razorpay_account_id` is set for cafe owner
- Check webhook logs for errors
- Manual transfer can be created via admin panel

---

## ✅ Implementation Complete!

All features implemented and ready for testing. The system now properly:
1. ✅ Splits payments automatically
2. ✅ Transfers owner share via Razorpay Route
3. ✅ Shows accurate revenue on owner dashboard
4. ✅ Tracks all transactions with full audit trail
5. ✅ Handles errors and failures gracefully

**Next Steps:**
1. Configure Razorpay Route in production
2. Test with real transactions in test mode
3. Monitor webhook logs for any issues
4. Deploy to production when ready

---

**Documentation Created**: November 3, 2025  
**Implementation Status**: COMPLETE ✅  
**Version**: 1.0.0
