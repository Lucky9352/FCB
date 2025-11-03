# Razorpay Route - Quick Reference Card

## 💰 Payment Split Formula

```
For a ₹100 booking:

USER PAYS:
  Booking Amount:     ₹100.00
  Platform Fee (2%):  +  ₹2.00
  ─────────────────────────────
  TOTAL CHARGED:      ₹102.00

OWNER RECEIVES:
  Booking Amount:     ₹100.00
  Commission (7%):    -  ₹7.00
  ─────────────────────────────
  OWNER PAYOUT:        ₹93.00

PLATFORM KEEPS:
  Platform Fee:        ₹2.00
  Commission:        +  ₹7.00
  ─────────────────────────────
  PLATFORM TOTAL:      ₹9.00
```

## 🔧 Setup Checklist

### 1. Razorpay Dashboard
- [ ] Enable Razorpay Route
- [ ] Create/Get Linked Account ID
- [ ] Format: `acc_xxxxx` or `route_xxxxx`

### 2. Application Settings
- [ ] Go to: `/accounts/tapnex/settings/`
- [ ] Enter Account ID
- [ ] Enter Account Email
- [ ] Save settings
- [ ] Verify status = ACTIVE

### 3. Test Transaction
- [ ] Create test booking (₹100)
- [ ] User charged ₹102 ✓
- [ ] Owner receives ₹93 ✓
- [ ] Transfer status = PROCESSED ✓
- [ ] Dashboard shows ₹93 ✓

## 📊 Key Database Fields

| Booking Field | Value for ₹100 |
|---------------|----------------|
| `subtotal` | ₹100.00 |
| `platform_fee` | ₹2.00 |
| `total_amount` | ₹102.00 |
| `commission_amount` | ₹7.00 |
| `owner_payout` | ₹93.00 |
| `transfer_status` | PROCESSED |

## 🎯 Dashboard Metrics

**Owner Dashboard NOW shows:**
- Daily Revenue: Sum of `owner_payout` ✅
- Monthly Revenue: Sum of `owner_payout` ✅
- Customer LTV: Based on `owner_payout` ✅
- All charts: Use `owner_payout` ✅

**Owner sees their ACTUAL earnings (after commission)**

## 🔔 Webhook Events

| Event | Action |
|-------|--------|
| `payment.captured` | Payment successful |
| `transfer.processed` | ✅ Transfer to owner OK |
| `transfer.failed` | ❌ Transfer failed - Alert |
| `transfer.reversed` | ⚠️ Transfer reversed |

## 🚨 Troubleshooting

**Problem**: Transfer shows FAILED  
**Fix**: Check account ID is correct and ACTIVE

**Problem**: Dashboard shows wrong amount  
**Fix**: Verify `owner_payout` field is populated

**Problem**: No transfer created  
**Fix**: Ensure `razorpay_account_id` is set

## 📍 Quick Links

- **Settings**: `/accounts/tapnex/settings/`
- **Owner Dashboard**: `/accounts/owner/dashboard/`
- **Bookings**: `/accounts/owner/bookings/`
- **Revenue**: `/accounts/owner/revenue/`

## 💡 Remember

- Commission = **7%** (FIXED)
- Platform Fee = **2%** (Configurable)
- User pays = Booking + Platform Fee
- Owner gets = Booking - Commission

**ALL OWNER METRICS USE `owner_payout` FIELD**
