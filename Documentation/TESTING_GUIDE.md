# 🧪 TapNex Arena - Comprehensive Testing Guide

**Version:** 1.0  
**Last Updated:** November 5, 2025  
**Purpose:** Manual testing instructions to verify all functionalities across all user roles

---

## 📋 Table of Contents

1. [Pre-Testing Setup](#pre-testing-setup)
2. [Testing Order](#testing-order)
3. [Public/Guest User Testing](#publicguest-user-testing)
4. [Customer Role Testing](#customer-role-testing)
5. [Cafe Owner/Staff Role Testing](#cafe-ownerstaff-role-testing)
6. [TapNex Superuser Testing](#tapnex-superuser-testing)
7. [Payment Integration Testing](#payment-integration-testing)
8. [QR Code Verification Testing](#qr-code-verification-testing)
9. [Notification System Testing](#notification-system-testing)
10. [Error Handling Testing](#error-handling-testing)
11. [Checklist Summary](#checklist-summary)

---

## 🚀 Pre-Testing Setup

### Prerequisites
- [ ] Python 3.9+ installed
- [ ] PostgreSQL database accessible (Supabase)
- [ ] All environment variables configured in `.env` file
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Node.js and npm installed
- [ ] Tailwind CSS built: `npm run build-css-prod`
- [ ] Static files collected: `python manage.py collectstatic --noinput`
- [ ] Database migrations applied: `python manage.py migrate`

### Environment Variables Required
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-supabase-postgres-url
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
RAZORPAY_WEBHOOK_SECRET=your-razorpay-webhook-secret
GOOGLE_OAUTH_CLIENT_ID=your-google-oauth-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-oauth-client-secret
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id
```

### Start the Server
```bash
python manage.py runserver
```
Access at: `http://localhost:8000`

---

## 🔄 Testing Order

**Important:** Follow this exact order to ensure proper test coverage and avoid dependency issues.

1. ✅ Public/Guest User Testing (No authentication)
2. ✅ Customer Role Testing (Google OAuth + Email Login)
3. ✅ Cafe Owner/Staff Role Testing (Username/Password)
4. ✅ TapNex Superuser Testing (Superuser credentials)
5. ✅ Payment Integration Testing (Razorpay)
6. ✅ QR Code Verification Testing (Owner/Staff)
7. ✅ Notification System Testing (Real-time)
8. ✅ Error Handling Testing (Edge cases)

---

## 👥 Public/Guest User Testing

**Role:** Unauthenticated visitors  
**Access:** `http://localhost:8000/`

### 1.1 Home Page
- [ ] Navigate to `http://localhost:8000/`
- [ ] Verify TapNex Arena branding displays correctly
- [ ] Check navigation bar shows: Home, About, Contact, Sign In
- [ ] Verify hero section with call-to-action buttons
- [ ] Scroll through features section
- [ ] Check footer displays: About, Legal links, Contact info, Social media icons
- [ ] Verify "Powered by TapNex" and "NexGen FC" branding in footer

### 1.2 Policy Pages
- [ ] Click "Privacy Policy" in footer → `/privacy/`
- [ ] Verify privacy policy content displays
- [ ] Click "Terms & Conditions" → `/terms/`
- [ ] Verify terms content displays
- [ ] Click "Refund Policy" → `/refund-policy/`
- [ ] Verify refund policy displays
- [ ] Click "Shipping Policy" → `/shipping-policy/`
- [ ] Verify shipping policy displays
- [ ] Click "About" → `/about/`
- [ ] Verify about page content
- [ ] Click "Contact" → `/contact/`
- [ ] Verify contact page with form

### 1.3 Browse Games (Without Login)
- [ ] Navigate to `/booking/games/`
- [ ] Verify redirect to login page or game listing
- [ ] Check if games display with images and descriptions
- [ ] Verify prices display correctly (Private/Shared)
- [ ] Try clicking "Book Now" → Should redirect to login

### 1.4 Error Pages
- [ ] Navigate to non-existent URL → `/nonexistent-page/`
- [ ] Verify custom 404 page displays
- [ ] Check "Go Home" button works
- [ ] Verify 404 page has TapNex branding

---

## 🎮 Customer Role Testing

**Role:** Regular customers  
**Login Methods:** Google OAuth or Email/Password

### 2.1 Customer Registration & Login

#### Google OAuth Login
- [ ] Navigate to `/accounts/login/`
- [ ] Click "Sign in with Google" button
- [ ] Complete Google OAuth flow
- [ ] Verify redirect to customer dashboard
- [ ] Check user profile created with Google avatar
- [ ] Verify welcome message displays

#### Email/Password Login
- [ ] Click "Sign in with Email" on login page
- [ ] Navigate to `/accounts/login/email/`
- [ ] Enter valid email and password
- [ ] Click "Sign In"
- [ ] Verify successful login
- [ ] Verify redirect to customer dashboard

#### First-Time Login (Google)
- [ ] Use new Google account
- [ ] Complete OAuth flow
- [ ] Verify Customer profile auto-created
- [ ] Check phone number prompt (if applicable)
- [ ] Verify avatar fetched from Google

### 2.2 Customer Dashboard
- [ ] Access `/accounts/customer/dashboard/`
- [ ] Verify dashboard displays:
  - Welcome message with customer name
  - Quick stats (Upcoming, Completed, Total bookings)
  - Recent bookings list
  - Quick action buttons
- [ ] Check navigation shows: Dashboard, Book Tables, My Bookings, Logout
- [ ] Verify notification bell icon displays
- [ ] Check user avatar displays in header

### 2.3 Browse & Select Games
- [ ] Click "Book Tables" → `/booking/games/`
- [ ] Verify all active games display
- [ ] Check each game card shows:
  - Game name (e.g., "8-Ball Pool", "Table Tennis")
  - Game image
  - Capacity
  - Booking type (Private/Shared)
  - Price information
  - "Book Now" button
- [ ] Click on a game card
- [ ] Verify game detail view opens

### 2.4 View Game Details
- [ ] Select any game → `/booking/games/<game-id>/`
- [ ] Verify game details display:
  - Game name and description
  - Large game image
  - Capacity and booking type
  - Schedule (opening/closing time)
  - Slot duration
  - Available days
  - Pricing breakdown
- [ ] Check "Book This Game" button present
- [ ] Verify "Back to Games" button works

### 2.5 Create Booking - Private Mode

#### Select Date & Time
- [ ] Click "Book This Game"
- [ ] Verify booking modal opens
- [ ] Select booking type: **Private**
- [ ] Select today's date from calendar
- [ ] Verify available time slots display
- [ ] Check unavailable slots are greyed out
- [ ] Select an available time slot
- [ ] Verify slot highlights on selection

#### Confirm Booking Details
- [ ] Click "Continue to Payment"
- [ ] Navigate to confirmation page
- [ ] Verify booking summary displays:
  - Game name
  - Date and time
  - Duration
  - Booking type: Private
  - Number of spots (full capacity)
  - Total price
- [ ] Check phone number field (editable)
- [ ] Review terms and conditions checkbox

#### Complete Payment
- [ ] Check "I agree to terms" checkbox
- [ ] Click "Proceed to Payment"
- [ ] Verify Razorpay payment modal opens
- [ ] **DO NOT PAY** - Close modal (for testing cancellation)
- [ ] Verify redirect to payment cancelled page
- [ ] Check booking status: PENDING

### 2.6 Create Booking - Shared Mode (Hybrid Games)

#### Select Shared Booking
- [ ] Navigate back to game selection
- [ ] Select a **Hybrid** game (supports shared)
- [ ] Click "Book This Game"
- [ ] Select booking type: **Shared**
- [ ] Select date and time slot
- [ ] Enter number of spots (1-4 typically)
- [ ] Verify price calculation: spots × per-person price
- [ ] Click "Continue to Payment"

#### Confirm Shared Booking
- [ ] Verify booking summary shows:
  - Booking type: Shared
  - Number of spots selected
  - Per-person price
  - Total calculated correctly
- [ ] Add phone number if required
- [ ] Check terms checkbox
- [ ] Click "Proceed to Payment"

#### Complete Payment (Test Success)
- [ ] Razorpay modal opens
- [ ] Enter test card: `4111 1111 1111 1111`
- [ ] Enter future expiry: `12/25`
- [ ] Enter CVV: `123`
- [ ] Click "Pay"
- [ ] Verify payment success
- [ ] Check redirect to success page
- [ ] Verify booking status: CONFIRMED

### 2.7 View My Bookings
- [ ] Navigate to `/booking/my-bookings/`
- [ ] Verify all bookings list displays
- [ ] Check booking cards show:
  - Game name
  - Date and time
  - Status badge (PENDING, CONFIRMED, IN_PROGRESS, COMPLETED, CANCELLED)
  - Booking type (Private/Shared)
  - Total amount paid
  - Action buttons (Cancel, View QR)

#### Filter Bookings
- [ ] Test filter: Show **Upcoming** only
- [ ] Verify only future bookings display
- [ ] Test filter: Show **Completed** only
- [ ] Verify only past bookings display
- [ ] Test filter: Show **All**
- [ ] Verify all bookings display

### 2.8 View Booking QR Code
- [ ] Click on a CONFIRMED booking
- [ ] Click "View QR Code" button
- [ ] Verify QR code modal displays
- [ ] Check QR code image renders
- [ ] Verify booking details shown below QR
- [ ] Check "Download QR Code" button
- [ ] Click download → Verify PNG file downloads
- [ ] Close modal

### 2.9 Cancel Booking
- [ ] Select a CONFIRMED booking
- [ ] Click "Cancel Booking" button
- [ ] Verify confirmation dialog appears
- [ ] Confirm cancellation
- [ ] Verify booking status changes to CANCELLED
- [ ] Check notification appears
- [ ] Verify refund policy message (if applicable)

### 2.10 Update Booking Spots (Shared Bookings)
- [ ] Find a CONFIRMED shared booking
- [ ] Click "Update Spots" button
- [ ] Increase number of spots (within capacity)
- [ ] Verify additional payment calculation
- [ ] Complete payment for additional spots
- [ ] Verify booking updated successfully
- [ ] Check new total amount reflects

### 2.11 Real-Time Availability
- [ ] Open game booking in one browser
- [ ] Open same game in another browser (different user)
- [ ] Book a slot in browser 1
- [ ] Verify slot becomes unavailable in browser 2 instantly
- [ ] Check real-time updates work without page refresh

### 2.12 Notifications
- [ ] Click notification bell icon
- [ ] Verify dropdown opens
- [ ] Check notifications display:
  - Booking confirmed
  - Payment successful
  - Booking starting soon (if time-based)
  - Booking completed
- [ ] Click on a notification
- [ ] Verify notification marked as read
- [ ] Check unread count updates

### 2.13 Profile & Settings
- [ ] Click user avatar in header
- [ ] Verify dropdown shows:
  - User name
  - Email
  - Profile link (if available)
  - Logout
- [ ] Update phone number
- [ ] Verify phone number saves
- [ ] Check validation for invalid phone

### 2.14 Logout
- [ ] Click "Logout" button
- [ ] Verify redirect to home page
- [ ] Check user session cleared
- [ ] Try accessing `/accounts/customer/dashboard/`
- [ ] Verify redirect to login page

---

## 🏪 Cafe Owner/Staff Role Testing

**Role:** Cafe owners managing bookings and games  
**Login:** Username/Password at `/accounts/cafe-owner/login/`

### 3.1 Owner Login
- [ ] Navigate to `/accounts/cafe-owner/login/`
- [ ] Enter valid owner username
- [ ] Enter valid password
- [ ] Click "Sign In"
- [ ] Verify redirect to owner dashboard
- [ ] Check welcome message shows cafe name

### 3.2 Owner Dashboard Overview
- [ ] Access `/accounts/owner/dashboard/`
- [ ] Verify dashboard displays:
  - **Overview Cards:**
    - Total Revenue (Today, This Month)
    - Active Bookings Count
    - Pending Verifications
    - Total Games/Tables
  - **Quick Stats Charts** (if implemented)
  - **Recent Bookings List**
  - **Quick Actions** (Scan QR, Manage Games, View Reports)

### 3.3 View All Bookings
- [ ] Navigate to `/accounts/owner/bookings/`
- [ ] Verify bookings table displays:
  - Booking ID
  - Customer name
  - Game/Table name
  - Date & Time
  - Status
  - Payment status
  - Total amount
  - Actions (View, Complete, Cancel)

#### Filter & Search
- [ ] Filter by status: PENDING
- [ ] Filter by status: CONFIRMED
- [ ] Filter by status: IN_PROGRESS
- [ ] Filter by status: COMPLETED
- [ ] Search by customer name
- [ ] Search by booking ID
- [ ] Filter by date range

### 3.4 View Booking Details (Owner)
- [ ] Click "View" on any booking
- [ ] Verify booking detail page shows:
  - Customer information (name, email, phone)
  - Game details
  - Time slot information
  - Payment details
  - QR code
  - Status timeline
  - Notes section

### 3.5 QR Code Scanner (Staff Verification)
- [ ] Navigate to `/booking/qr-scanner/`
- [ ] Verify QR scanner page loads
- [ ] Check camera permission prompt
- [ ] Allow camera access
- [ ] Scan a valid booking QR code (from customer)
- [ ] Verify booking details appear
- [ ] Check customer name and booking info display
- [ ] Click "Mark as In Progress"
- [ ] Verify booking status updates to IN_PROGRESS
- [ ] Scan same QR again
- [ ] Click "Complete Booking"
- [ ] Verify status updates to COMPLETED

#### Manual QR Verification
- [ ] On QR scanner page, click "Enter Manually"
- [ ] Enter valid booking ID
- [ ] Click "Verify"
- [ ] Verify booking details load
- [ ] Proceed with status update

### 3.6 Active Bookings View
- [ ] Navigate to `/booking/active-bookings/`
- [ ] Verify currently IN_PROGRESS bookings display
- [ ] Check real-time updates
- [ ] Verify timer shows time remaining (if applicable)
- [ ] Test "Complete" button for each active booking
- [ ] Confirm completion
- [ ] Verify booking moves to COMPLETED

### 3.7 Manage Games/Tables

#### View All Games
- [ ] Navigate to `/booking/games/manage/`
- [ ] Verify all games list
- [ ] Check each game shows:
  - Name, capacity, type
  - Status (Active/Inactive)
  - Edit and Delete buttons

#### Create New Game
- [ ] Click "Add New Game" button
- [ ] Fill in game details:
  - Name: "Test Pool Table #5"
  - Description: "Professional 8-ball pool table"
  - Capacity: 4
  - Booking Type: Hybrid
  - Opening Time: 10:00 AM
  - Closing Time: 10:00 PM
  - Slot Duration: 60 minutes
  - Available Days: Mon-Sun (select all)
  - Private Price: ₹400
  - Shared Price: ₹100
  - Upload image
- [ ] Click "Create Game"
- [ ] Verify game created successfully
- [ ] Check automatic slot generation confirmation
- [ ] Verify slots created for next 30 days

#### Edit Existing Game
- [ ] Click "Edit" on any game
- [ ] Update game name
- [ ] Change pricing
- [ ] Update schedule
- [ ] Click "Save Changes"
- [ ] Verify updates reflected
- [ ] Check existing bookings unaffected

#### Activate/Deactivate Game
- [ ] Toggle game status to Inactive
- [ ] Verify game no longer appears in customer booking list
- [ ] Check existing bookings remain valid
- [ ] Toggle back to Active
- [ ] Verify game reappears for customers

#### Delete Game
- [ ] Click "Delete" on a game with NO bookings
- [ ] Confirm deletion
- [ ] Verify game removed
- [ ] Try deleting game WITH bookings
- [ ] Verify error message (cannot delete)

### 3.8 Manage Custom Time Slots

#### View Schedule
- [ ] Navigate to `/booking/games/manage/schedules/`
- [ ] Select a game
- [ ] Verify calendar view shows all slots
- [ ] Check auto-generated slots marked
- [ ] Check custom slots marked differently

#### Create Custom Slot
- [ ] Click "Add Custom Slot"
- [ ] Select game
- [ ] Choose date (future date)
- [ ] Set start time
- [ ] Set end time
- [ ] Click "Create"
- [ ] Verify custom slot appears in calendar
- [ ] Verify slot available for customer booking

#### Block Time Slot
- [ ] Find an available slot
- [ ] Click "Block Slot"
- [ ] Add reason: "Maintenance"
- [ ] Confirm blocking
- [ ] Verify slot becomes unavailable
- [ ] Check customers cannot book this slot

#### Delete Custom Slot
- [ ] Find a custom slot with NO bookings
- [ ] Click "Delete"
- [ ] Confirm deletion
- [ ] Verify slot removed

### 3.9 Revenue Reports
- [ ] Navigate to `/accounts/owner/revenue/`
- [ ] Verify revenue dashboard displays:
  - Total revenue (Today, This Week, This Month)
  - Revenue by game breakdown
  - Payment method breakdown
  - Revenue trend chart
  - Top performing games

#### Filter Reports
- [ ] Select date range: Last 7 days
- [ ] Verify data updates
- [ ] Select date range: Last 30 days
- [ ] Verify data updates
- [ ] Select custom date range
- [ ] Click "Generate Report"
- [ ] Verify filtered data displays

#### Export Reports
- [ ] Click "Export CSV" button
- [ ] Verify CSV file downloads
- [ ] Open CSV file
- [ ] Check data accuracy

### 3.10 Customer Management
- [ ] Navigate to `/accounts/owner/customers/`
- [ ] Verify customer list displays
- [ ] Check customer details:
  - Name, email, phone
  - Total bookings
  - Total spent
  - Last booking date
- [ ] Search for specific customer
- [ ] Click customer name
- [ ] Verify customer detail view shows booking history

### 3.11 Notifications (Owner)
- [ ] Check notification system for:
  - New booking notifications
  - Payment received notifications
  - Booking cancellation alerts
  - Customer no-show alerts (if applicable)
- [ ] Verify Telegram notifications (if configured)
- [ ] Check email notifications (if configured)

### 3.12 Owner Logout
- [ ] Click "Logout"
- [ ] Verify redirect to home or login page
- [ ] Try accessing owner dashboard
- [ ] Verify access denied

---

## 🔐 TapNex Superuser Testing

**Role:** Platform administrators (TapNex staff)  
**Login:** Superuser credentials at `/accounts/cafe-owner/login/` (same form, but with superuser account)

### 4.1 Superuser Login
- [ ] Navigate to `/accounts/cafe-owner/login/`
- [ ] Enter superuser username
- [ ] Enter superuser password
- [ ] Click "Sign In"
- [ ] Verify redirect to TapNex Dashboard
- [ ] Check URL: `/accounts/tapnex/dashboard/`

### 4.2 TapNex Dashboard Overview
- [ ] Verify superuser dashboard displays:
  - **Platform-Wide Stats:**
    - Total Revenue (All Cafes)
    - Total Active Bookings
    - Total Registered Users
    - Total Cafe Owners
    - Total Games/Tables
  - **System Health Indicators**
  - **Recent Activity Feed**
  - **Quick Actions**

### 4.3 User Management

#### View All Users
- [ ] Navigate to `/accounts/tapnex/users/`
- [ ] Verify users table displays:
  - Username, Email, Role
  - Date Joined
  - Last Login
  - Status (Active/Inactive)
  - Actions

#### Filter Users by Role
- [ ] Filter: Customers only
- [ ] Verify only customer profiles display
- [ ] Filter: Cafe Owners only
- [ ] Verify only owner profiles display
- [ ] Filter: All Users

#### View User Details
- [ ] Click on any user
- [ ] Navigate to `/accounts/tapnex/users/<user-id>/`
- [ ] Verify user details page shows:
  - Full profile information
  - Booking history (if customer)
  - Associated cafe (if owner)
  - Activity timeline
  - Account status

#### User Actions
- [ ] Test "Activate User" (if inactive)
- [ ] Test "Deactivate User"
- [ ] Verify confirmation prompt
- [ ] Confirm action
- [ ] Verify user status updates
- [ ] Check user can/cannot login accordingly

### 4.4 Manage Cafe Owners

#### View All Cafe Owners
- [ ] Navigate to `/accounts/tapnex/cafe-owner-management/`
- [ ] Verify cafe owners list
- [ ] Check each owner shows:
  - Cafe name
  - Owner name
  - Contact email
  - Phone number
  - Status
  - Actions

#### Create New Cafe Owner
- [ ] Click "Create Cafe Owner"
- [ ] Navigate to `/accounts/tapnex/cafe-owner/create/`
- [ ] Fill in details:
  - Username: testcafe_owner
  - Email: testowner@example.com
  - Password: Strong_Password_123
  - Cafe Name: Test Gaming Cafe
  - Contact Email: contact@testcafe.com
  - Phone: +1234567890
  - Razorpay Account Email: razorpay@testcafe.com
- [ ] Click "Create Owner"
- [ ] Verify owner account created
- [ ] Check confirmation message
- [ ] Verify email sent to owner (if email configured)

#### Reset Cafe Owner Password
- [ ] Navigate to `/accounts/tapnex/reset-cafe-owner-password/`
- [ ] Select cafe owner from dropdown
- [ ] Enter new password
- [ ] Confirm password
- [ ] Click "Reset Password"
- [ ] Verify success message
- [ ] Test login with new password (in incognito/another browser)

### 4.5 Manage All Bookings (System-Wide)

#### View All Bookings
- [ ] Navigate to `/accounts/tapnex/bookings/`
- [ ] Verify all bookings across all cafes display
- [ ] Check booking details include cafe/owner info

#### Filter Bookings
- [ ] Filter by cafe owner
- [ ] Filter by status
- [ ] Filter by date range
- [ ] Search by customer name
- [ ] Search by booking ID

#### View Booking Details (Superuser)
- [ ] Click on any booking
- [ ] Navigate to `/accounts/tapnex/bookings/<booking-id>/`
- [ ] Verify complete booking information
- [ ] Check payment details
- [ ] Verify commission calculation (if applicable)
- [ ] Check cafe owner payout amount

#### Booking Actions (Admin Override)
- [ ] Test "Cancel Booking" (admin override)
- [ ] Add cancellation reason
- [ ] Confirm cancellation
- [ ] Verify booking status updates
- [ ] Check refund initiated (if policy allows)
- [ ] Test "Complete Booking" (admin override)
- [ ] Verify status updates

### 4.6 Manage All Games (System-Wide)

#### View All Games
- [ ] Navigate to `/accounts/tapnex/games/`
- [ ] Verify all games across all cafes display
- [ ] Check each game shows owner/cafe association

#### View Game Details
- [ ] Click on any game
- [ ] Navigate to `/accounts/tapnex/games/<game-id>/`
- [ ] Verify game details
- [ ] Check booking statistics
- [ ] View revenue generated by game

#### Game Actions (Admin)
- [ ] Test "Activate/Deactivate" game
- [ ] Verify action applied
- [ ] Test "Edit Game Details" (admin override)
- [ ] Update game information
- [ ] Verify changes saved

### 4.7 Commission & Revenue Management

#### View Commission Settings
- [ ] Navigate to `/accounts/tapnex/commission-settings/`
- [ ] Verify current commission settings display
- [ ] Check commission types:
  - Percentage (e.g., 10% of booking)
  - Fixed amount (e.g., ₹20 per booking)
  - Tiered (based on volume)

#### Update Commission Settings
- [ ] Select commission type: Percentage
- [ ] Enter commission rate: 8%
- [ ] Click "Save Settings"
- [ ] Verify settings updated
- [ ] Check future bookings apply new commission

#### View Revenue Reports (Platform-Wide)
- [ ] Navigate to `/accounts/tapnex/revenue-reports/`
- [ ] Verify revenue dashboard shows:
  - Total platform revenue
  - TapNex commission earned
  - Cafe owner payouts
  - Revenue by cafe breakdown
  - Revenue trend over time

#### Generate Revenue Report
- [ ] Select date range
- [ ] Select specific cafe owner (optional)
- [ ] Click "Generate Report"
- [ ] Verify detailed breakdown displays
- [ ] Check export options

#### AJAX Revenue Data
- [ ] Navigate to `/accounts/tapnex/ajax/revenue-data/`
- [ ] Verify API returns JSON data
- [ ] Check data structure accuracy

### 4.8 System Settings

#### View System Settings
- [ ] Navigate to `/accounts/tapnex/settings/`
- [ ] Verify settings page displays:
  - Platform configuration
  - Telegram notification settings
  - Email settings
  - Payment gateway settings
  - System maintenance mode

#### Update Telegram Settings
- [ ] Enter Telegram Bot Token
- [ ] Enter Telegram Chat ID
- [ ] Click "Save Settings"
- [ ] Click "Test Telegram Notification"
- [ ] Verify test message received in Telegram

#### Update Payment Settings
- [ ] Enter/Update Razorpay API keys
- [ ] Save settings
- [ ] Verify keys encrypted/stored securely

#### Enable/Disable Features
- [ ] Toggle "Allow Google OAuth Login"
- [ ] Toggle "Enable Email Login"
- [ ] Toggle "Auto-generate Slots"
- [ ] Save settings
- [ ] Verify features enabled/disabled accordingly

### 4.9 Database Browser (Admin Tool)

#### Access Database Browser
- [ ] Navigate to `/accounts/tapnex/database/`
- [ ] Verify database browser interface loads
- [ ] Check tables list:
  - Users
  - Customers
  - CafeOwners
  - Games
  - Bookings
  - Payments
  - Notifications

#### Browse Tables
- [ ] Select "Bookings" table
- [ ] Verify records display
- [ ] Check pagination works
- [ ] Test search functionality
- [ ] Test sorting by columns

#### View Record Details
- [ ] Click on any record
- [ ] Verify detailed view displays all fields
- [ ] Check related records linked

### 4.10 System Analytics

#### View Analytics Dashboard
- [ ] Navigate to `/accounts/tapnex/system-analytics/`
- [ ] Verify analytics display:
  - User growth chart
  - Booking trends
  - Revenue trends
  - Popular games/tables
  - Peak booking hours
  - Geographic distribution (if applicable)

#### Filter Analytics
- [ ] Select time range: Last 7 days
- [ ] Verify charts update
- [ ] Select time range: Last 30 days
- [ ] Select custom date range
- [ ] Export analytics data

### 4.11 Test Telegram Notifications

#### Send Test Notification
- [ ] Navigate to `/accounts/tapnex/test-telegram/`
- [ ] Click "Send Test Notification"
- [ ] Verify success message
- [ ] Check Telegram chat for test message
- [ ] Verify message format correct

### 4.12 Superuser Logout
- [ ] Click "Logout"
- [ ] Verify redirect
- [ ] Try accessing superuser dashboard
- [ ] Verify access denied

---

## 💳 Payment Integration Testing

**Component:** Razorpay Payment Gateway  
**Test Cards:** Use Razorpay test mode

### 5.1 Test Payment Success

#### Setup
- [ ] Ensure Razorpay test mode enabled
- [ ] Have test API keys configured
- [ ] Create a booking as customer

#### Execute Payment
- [ ] Proceed to payment page
- [ ] Verify Razorpay modal opens
- [ ] Enter test card: `4111 1111 1111 1111`
- [ ] Expiry: Any future date (e.g., `12/25`)
- [ ] CVV: Any 3 digits (e.g., `123`)
- [ ] Click "Pay ₹XXX"
- [ ] Verify payment processing
- [ ] Check redirect to success page
- [ ] Verify booking status: CONFIRMED

#### Verify Backend
- [ ] Check payment record created in database
- [ ] Verify Razorpay payment ID stored
- [ ] Check payment status: SUCCESS
- [ ] Verify commission calculated (if applicable)
- [ ] Check Telegram notification sent (if configured)

### 5.2 Test Payment Failure

#### Card Decline Test
- [ ] Create new booking
- [ ] Proceed to payment
- [ ] Enter test card: `4000 0000 0000 0002` (Decline card)
- [ ] Enter expiry and CVV
- [ ] Click "Pay"
- [ ] Verify payment fails
- [ ] Check error message displays
- [ ] Verify booking status remains PENDING
- [ ] Check user redirected to payment cancelled page

### 5.3 Test Payment Cancellation
- [ ] Create booking
- [ ] Open Razorpay modal
- [ ] Click "X" to close modal (cancel)
- [ ] Verify redirect to cancellation page
- [ ] Check booking status: PENDING
- [ ] Verify user can retry payment
- [ ] Click "Retry Payment"
- [ ] Verify modal opens again

### 5.4 Test Multiple Payment Attempts
- [ ] Create booking
- [ ] Attempt payment 1: Cancel
- [ ] Attempt payment 2: Use declined card
- [ ] Attempt payment 3: Successful payment
- [ ] Verify booking confirmed after success
- [ ] Check all payment attempts logged

### 5.5 Razorpay Webhook Testing

#### Setup Webhook
- [ ] Configure Razorpay webhook URL: `https://yourdomain.com/booking/payment/webhook/`
- [ ] Set webhook secret in environment
- [ ] Enable events: `payment.captured`, `payment.failed`

#### Test Webhook
- [ ] Complete a payment
- [ ] Verify webhook received at `/booking/payment/webhook/`
- [ ] Check webhook signature validation
- [ ] Verify payment status updated
- [ ] Check booking status synced

### 5.6 Refund Testing (If Implemented)
- [ ] Complete a successful payment
- [ ] Cancel booking (with refund policy)
- [ ] Verify refund initiated in Razorpay
- [ ] Check refund status updated
- [ ] Verify customer notified of refund

### 5.7 Payment Status Check
- [ ] Navigate to `/booking/payment/status/<booking-id>/`
- [ ] Verify payment status API returns correct data:
  - Payment ID
  - Amount
  - Status
  - Timestamp
- [ ] Test with different booking statuses

---

## 📱 QR Code Verification Testing

**Component:** QR Code generation and scanning for booking verification

### 6.1 QR Code Generation

#### Customer Side
- [ ] Complete a booking with payment
- [ ] Navigate to "My Bookings"
- [ ] Click on CONFIRMED booking
- [ ] Click "View QR Code"
- [ ] Verify QR code displays
- [ ] Check QR code contains booking ID
- [ ] Verify booking details below QR:
  - Booking ID
  - Game name
  - Date and time
  - Customer name
- [ ] Click "Download QR Code"
- [ ] Verify PNG file downloads
- [ ] Open downloaded file → Check QR readable

#### Verify QR Content
- [ ] Use external QR scanner app
- [ ] Scan downloaded QR code
- [ ] Verify decoded data contains booking ID
- [ ] Check format: `BOOKING:{booking_id}`

### 6.2 QR Code Scanning (Staff)

#### Access Scanner
- [ ] Login as cafe owner/staff
- [ ] Navigate to `/booking/qr-scanner/`
- [ ] Verify QR scanner page loads
- [ ] Check camera permission prompt
- [ ] Allow camera access
- [ ] Verify camera feed displays

#### Scan Valid QR Code
- [ ] Open customer's QR code on phone
- [ ] Hold QR code to camera
- [ ] Verify scanner detects QR
- [ ] Check booking details popup:
  - Customer name
  - Game name
  - Time slot
  - Booking status
  - Current status options
- [ ] Verify only valid actions available (based on current status)

#### Mark Booking In Progress
- [ ] With CONFIRMED booking QR
- [ ] Click "Mark as In Progress"
- [ ] Verify confirmation dialog
- [ ] Confirm action
- [ ] Check booking status updates to IN_PROGRESS
- [ ] Verify customer receives notification
- [ ] Verify timestamp recorded

#### Complete Booking
- [ ] Scan same booking QR again
- [ ] Verify status now IN_PROGRESS
- [ ] Click "Complete Booking"
- [ ] Confirm completion
- [ ] Verify status updates to COMPLETED
- [ ] Check completion timestamp
- [ ] Verify customer notified

### 6.3 QR Code Edge Cases

#### Scan Invalid QR Code
- [ ] Generate random QR code (not booking)
- [ ] Scan with scanner
- [ ] Verify error message: "Invalid booking QR code"
- [ ] Check no action buttons appear

#### Scan Expired Booking QR
- [ ] Find old booking (past date)
- [ ] Scan QR code
- [ ] Verify warning message: "This booking has expired"
- [ ] Check limited actions available

#### Scan Cancelled Booking QR
- [ ] Cancel a booking
- [ ] Scan its QR code
- [ ] Verify status: CANCELLED
- [ ] Check no action buttons (cannot process)

#### Double Scan Prevention
- [ ] Complete a booking via QR scan
- [ ] Scan same QR again
- [ ] Verify status: COMPLETED
- [ ] Check message: "Booking already completed"
- [ ] Verify no further actions allowed

### 6.4 Manual Booking ID Entry
- [ ] On QR scanner page
- [ ] Click "Enter Booking ID Manually"
- [ ] Enter valid booking ID
- [ ] Click "Verify"
- [ ] Verify booking details load
- [ ] Test status update actions
- [ ] Enter invalid booking ID
- [ ] Verify error message

### 6.5 QR Storage Location
- [ ] Check QR codes stored at: `/media/booking_qr_codes/`
- [ ] Verify filename format: `booking_{id}_qr.png`
- [ ] Test direct URL access: `/media/booking_qr_codes/booking_<id>_qr.png`
- [ ] Verify image loads

---

## 🔔 Notification System Testing

**Component:** Real-time notifications for customers and owners

### 7.1 Customer Notifications

#### Booking Confirmed Notification
- [ ] Create and confirm a booking
- [ ] Check notification bell icon
- [ ] Verify unread count increases
- [ ] Click notification bell
- [ ] Verify dropdown opens
- [ ] Check notification displays:
  - Title: "Booking Confirmed"
  - Message: Details of booking
  - Icon: Success (green checkmark)
  - Timestamp: "Just now"

#### Payment Success Notification
- [ ] Complete payment for booking
- [ ] Check notification appears
- [ ] Verify payment amount shown
- [ ] Verify Razorpay payment ID included

#### Booking Starting Soon Notification
- [ ] Create booking for near future (e.g., 15 mins ahead)
- [ ] Wait for scheduled notification
- [ ] Verify "Booking starting soon" notification appears
- [ ] Check time remaining shown

#### Booking Completed Notification
- [ ] Staff marks booking as completed
- [ ] Customer receives notification
- [ ] Verify notification shows completion details

#### Booking Cancelled Notification
- [ ] Cancel a booking
- [ ] Verify cancellation notification
- [ ] Check refund information (if applicable)

### 7.2 Cafe Owner Notifications

#### New Booking Notification
- [ ] Customer creates booking
- [ ] Owner receives notification
- [ ] Verify notification shows:
  - Customer name
  - Game/table
  - Time slot
  - Amount paid

#### Payment Received Notification
- [ ] Customer completes payment
- [ ] Owner receives notification
- [ ] Verify payment details included

#### Booking Cancellation Notification
- [ ] Customer cancels booking
- [ ] Owner receives notification
- [ ] Verify cancellation reason (if provided)

### 7.3 Notification Features

#### Mark as Read
- [ ] Click on unread notification
- [ ] Verify notification background changes (marked as read)
- [ ] Check unread count decreases
- [ ] Reload page
- [ ] Verify notification remains marked as read

#### Notification Dropdown
- [ ] Verify max 10 recent notifications displayed
- [ ] Check "See All" link present
- [ ] Click "See All"
- [ ] Navigate to full notifications page
- [ ] Verify all notifications listed

#### Notification Types
- [ ] Success (green): Confirmations, completions
- [ ] Warning (yellow): Reminders, upcoming events
- [ ] Error (red): Cancellations, failures
- [ ] Info (blue): General information

### 7.4 Real-Time Updates (Polling)
- [ ] Open application in browser
- [ ] Check notifications poll every 60 seconds
- [ ] Create booking in different session
- [ ] Within 60 seconds, verify notification appears without refresh
- [ ] Check browser console for AJAX calls

### 7.5 Telegram Notifications (If Configured)

#### Setup
- [ ] Ensure Telegram bot token configured
- [ ] Chat ID configured

#### Test Telegram Notifications
- [ ] Create new booking
- [ ] Check Telegram chat receives message
- [ ] Verify message format:
  - Booking details
  - Customer info
  - Payment status
  - Links to dashboard
- [ ] Complete payment
- [ ] Verify payment notification in Telegram
- [ ] Cancel booking
- [ ] Verify cancellation notification

---

## ⚠️ Error Handling Testing

**Component:** Error pages and edge case handling

### 8.1 404 Not Found
- [ ] Navigate to `/nonexistent-page/`
- [ ] Verify custom 404 page displays
- [ ] Check TapNex branding present
- [ ] Verify "Go Home" button works
- [ ] Test multiple invalid URLs

### 8.2 403 Forbidden
- [ ] As customer, try accessing `/accounts/owner/dashboard/`
- [ ] Verify 403 error page displays
- [ ] Check error message: "Access Denied"
- [ ] Verify "Go Home" button
- [ ] As owner, try accessing `/accounts/tapnex/dashboard/`
- [ ] Verify 403 error

### 8.3 500 Internal Server Error
- [ ] **Note:** Difficult to test without breaking code
- [ ] Temporarily introduce error in view
- [ ] Trigger error condition
- [ ] Verify custom 500 page displays
- [ ] Check error logged (if logging configured)
- [ ] Revert code change

### 8.4 Session Timeout
- [ ] Login as any user
- [ ] Wait 30 minutes (or modify SESSION_COOKIE_AGE in settings for faster test)
- [ ] Try navigating to protected page
- [ ] Verify redirect to login
- [ ] Check session expired message

### 8.5 Invalid Form Submissions

#### Registration Form
- [ ] Try registering with invalid email
- [ ] Verify error message
- [ ] Try weak password
- [ ] Verify password strength error
- [ ] Try mismatched password confirmation
- [ ] Verify error

#### Booking Form
- [ ] Try booking with invalid phone number
- [ ] Verify validation error
- [ ] Try booking past date
- [ ] Verify error
- [ ] Try booking with 0 spots
- [ ] Verify minimum spot validation

### 8.6 Payment Errors
- [ ] Test network failure during payment
- [ ] Verify graceful error handling
- [ ] Check user can retry
- [ ] Test Razorpay timeout
- [ ] Verify timeout error message

### 8.7 Database Connection Issues
- [ ] **Warning:** Test on staging only
- [ ] Temporarily disable database connection
- [ ] Try accessing application
- [ ] Verify appropriate error page
- [ ] Check connection error logged
- [ ] Restore connection

### 8.8 Permission Errors
- [ ] Try accessing QR scanner as customer
- [ ] Verify permission denied
- [ ] Try creating game as customer
- [ ] Verify error
- [ ] Try accessing superuser pages as owner
- [ ] Verify access denied

### 8.9 Concurrent Booking Conflict
- [ ] Open game booking in two browsers
- [ ] Select same slot in both
- [ ] Complete booking in browser 1
- [ ] Try completing in browser 2
- [ ] Verify error: "Slot no longer available"
- [ ] Check slot locked properly

---

## ✅ Checklist Summary

Use this quick checklist to track overall testing progress:

### Public/Guest Testing
- [ ] Home page and navigation
- [ ] Policy pages (Privacy, Terms, Refund, Shipping)
- [ ] Browse games without login
- [ ] Error pages (404, 403, 500)

### Customer Testing
- [ ] Google OAuth login
- [ ] Email/password login
- [ ] Customer dashboard
- [ ] Browse and view games
- [ ] Create private booking
- [ ] Create shared booking
- [ ] View my bookings
- [ ] View and download QR code
- [ ] Cancel booking
- [ ] Update booking spots
- [ ] Real-time availability
- [ ] Notifications
- [ ] Profile and settings
- [ ] Logout

### Cafe Owner Testing
- [ ] Owner login
- [ ] Owner dashboard
- [ ] View all bookings
- [ ] QR code scanner
- [ ] Active bookings view
- [ ] Create new game
- [ ] Edit game
- [ ] Manage time slots
- [ ] Revenue reports
- [ ] Customer management
- [ ] Owner notifications
- [ ] Logout

### TapNex Superuser Testing
- [ ] Superuser login
- [ ] TapNex dashboard
- [ ] User management
- [ ] Cafe owner management
- [ ] System-wide bookings
- [ ] System-wide games
- [ ] Commission settings
- [ ] Revenue reports
- [ ] System settings
- [ ] Database browser
- [ ] System analytics
- [ ] Test Telegram notifications
- [ ] Logout

### Payment Integration
- [ ] Payment success
- [ ] Payment failure
- [ ] Payment cancellation
- [ ] Multiple payment attempts
- [ ] Razorpay webhooks
- [ ] Refunds (if applicable)
- [ ] Payment status check

### QR Code System
- [ ] QR code generation
- [ ] QR code download
- [ ] QR code scanning
- [ ] Mark in progress
- [ ] Complete booking
- [ ] Invalid QR handling
- [ ] Manual ID entry

### Notifications
- [ ] Customer notifications (all types)
- [ ] Owner notifications (all types)
- [ ] Mark as read
- [ ] Real-time updates
- [ ] Telegram notifications

### Error Handling
- [ ] 404 Not Found
- [ ] 403 Forbidden
- [ ] 500 Internal Server Error
- [ ] Session timeout
- [ ] Invalid forms
- [ ] Payment errors
- [ ] Permission errors
- [ ] Concurrent booking conflicts

---

## 📊 Test Results Template

Use this template to document your test results:

```
Date: ___________
Tester: ___________
Environment: [ ] Local  [ ] Staging  [ ] Production

Section: __________________
Test Case: __________________
Status: [ ] Pass  [ ] Fail  [ ] Blocked
Notes: __________________
Screenshots/Evidence: __________________

Issues Found:
1. __________________
2. __________________

Recommendations:
1. __________________
2. __________________
```

---

## 🚨 Critical Bugs - Report Immediately

If you encounter any of these issues during testing, report immediately:

1. **Payment Processing Failures** - Money charged but booking not confirmed
2. **Double Booking** - Same slot booked by multiple users
3. **QR Code Not Working** - Cannot verify bookings at venue
4. **Security Vulnerabilities** - Unauthorized access to admin functions
5. **Data Loss** - Bookings or user data disappearing
6. **Critical UI Breakage** - Application completely unusable

---

## 📝 Additional Notes

### Testing Best Practices
- Clear browser cache between major test sections
- Use incognito/private windows for multi-user testing
- Take screenshots of issues encountered
- Note browser and device used for each test
- Test on multiple devices (desktop, tablet, mobile)
- Test on multiple browsers (Chrome, Firefox, Safari, Edge)

### Post-Testing Cleanup
After completing all tests:
- [ ] Delete all test bookings
- [ ] Remove test games created
- [ ] Delete test user accounts (except staff/admin)
- [ ] Clear test payment records
- [ ] Reset commission settings to production values

### Support Contacts
- Technical Issues: [Your Tech Support Email]
- Payment Issues: [Your Payment Support Email]
- General Inquiries: [Your General Support Email]

---

**End of Testing Guide**

**Last Updated:** November 5, 2025  
**Version:** 1.0  
**TapNex Arena Booking System**
