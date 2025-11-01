# Owner Dashboard - Quick Start Guide

## 🚀 Getting Started

### **Step 1: Start the Server**
```bash
python manage.py runserver
```

### **Step 2: Login**
Go to: `http://127.0.0.1:8000/cafe-owner/login/`

### **Step 3: Dashboard Access**
After login, you'll be automatically redirected to the Overview section.

---

## 📍 Dashboard URLs

| Section | URL | What You Can Do |
|---------|-----|-----------------|
| **Overview** | `/owner/overview/` | View real-time stats, today's timeline, alerts, upcoming bookings |
| **Bookings** | `/owner/bookings/` | Manage all bookings, filter by status/game/date, view details |
| **Games & Stations** | `/owner/games/` | Manage games, view station status, add new games, track maintenance |
| **Customers** | `/owner/customers/` | Browse customers, segment by VIP/frequency, view profiles |
| **Revenue & Finance** | `/owner/revenue/` | Track revenue, manage payments, view trends, monitor commission |
| **Reports & Analytics** | `/owner/reports/` | Analyze business metrics, generate reports, view charts |

---

## 🎯 Quick Navigation Tips

### **Using the Sidebar**
- Click any menu item to navigate to that section
- Active section is highlighted with a light background
- On desktop: Click the hamburger icon to collapse/expand
- On mobile: Tap hamburger to open/close menu

### **Top Bar Features**
- **Search bar** (desktop): Quick search across bookings/customers
- **New Booking button**: Quick access to create booking
- **Profile dropdown**: Access profile and logout

---

## 📊 What Each Section Shows

### **1. Overview**
**Perfect for:** Daily operations, quick status check

**You'll see:**
- 6 stat cards with today's numbers
- Revenue comparison with yesterday
- Hour-by-hour timeline of today's bookings
- Alert notifications
- Next 3 upcoming bookings

**Best used for:**
- Morning check-in to see the day ahead
- Quick status updates throughout the day
- Monitoring active sessions

---

### **2. Bookings**
**Perfect for:** Managing all reservations

**You'll see:**
- Status summary (Confirmed, In Progress, Completed, etc.)
- Complete booking list with all details
- Advanced filters (status, game, date, search)
- Booking details modal

**Best used for:**
- Viewing all bookings
- Finding specific bookings
- Monitoring cancellations
- Checking payment status

---

### **3. Games & Stations**
**Perfect for:** Resource management

**You'll see:**
- Games overview stats
- Grid view of all games with images
- Today's bookings and revenue per game
- Real-time station status board
- Color-coded availability

**Best used for:**
- Adding new games
- Marking games for maintenance
- Checking which stations are occupied
- Viewing game performance

---

### **4. Customers**
**Perfect for:** Customer relationship management

**You'll see:**
- Customer stats (total, VIP, new)
- Customer directory with contact info
- Segmentation filters
- Total bookings and spending per customer

**Best used for:**
- Finding customer information
- Identifying VIP customers
- Contacting customers
- Viewing customer history

---

### **5. Revenue & Finance**
**Perfect for:** Financial tracking

**You'll see:**
- Revenue summary cards
- Revenue trend chart
- Payment method breakdown
- Top revenue-generating games
- Pending and failed payments
- Platform commission tracking

**Best used for:**
- Daily revenue monitoring
- Payment reconciliation
- Financial reporting
- Commission calculations

---

### **6. Reports & Analytics**
**Perfect for:** Business insights

**You'll see:**
- Key metrics (bookings, avg value, cancellation rate, utilization)
- Revenue comparison (current vs previous period)
- Booking trend charts
- Peak hours analysis
- Customer analytics
- Pre-built report templates

**Best used for:**
- Weekly/monthly reviews
- Identifying trends
- Making business decisions
- Performance analysis

---

## 🎨 Color Coding Guide

### **Status Colors:**
- 🟢 **Green** = Confirmed, Active, Paid, Available
- 🔵 **Blue** = In Progress, Processing
- ⚫ **Gray** = Completed, Inactive
- 🔴 **Red** = Cancelled, Failed, Occupied
- 🟡 **Yellow** = Pending, Warning, Maintenance
- 🟠 **Orange** = No Show

---

## 📱 Mobile Tips

### **Navigation:**
1. Tap the **☰** icon (top left) to open sidebar
2. Tap outside sidebar to close it
3. Scroll horizontally on tables if needed

### **Best Practices:**
- Use portrait mode for better card layouts
- Use landscape for tables and charts
- Tap stat cards to see details
- Swipe through charts

---

## 🔥 Power User Tips

### **Keyboard Shortcuts** (Future Feature)
- `Ctrl + /` - Focus search bar
- `Ctrl + N` - New booking
- `Esc` - Close modals

### **Efficient Workflow:**

**Morning Routine:**
1. Check **Overview** for today's schedule
2. Review **Alerts** for any issues
3. Check **Revenue** from yesterday

**During the Day:**
1. Monitor **Overview** for active sessions
2. Use **Bookings** to handle walk-ins
3. Check **Games & Stations** for availability

**End of Day:**
1. Review **Revenue** for daily earnings
2. Check **Bookings** for tomorrow
3. Update **Games** maintenance if needed

**Weekly Review:**
1. Use **Reports** to analyze the week
2. Check **Customers** for new sign-ups
3. Review **Revenue** trends

---

## 🛠️ Troubleshooting

### **Dashboard not loading?**
- Check if server is running
- Verify you're logged in as cafe owner
- Clear browser cache

### **Data not showing?**
- Make sure you have some bookings/games in the database
- Check date filters (might be filtering out data)
- Refresh the page

### **Charts not displaying?**
- Ensure internet connection (Chart.js CDN)
- Check browser console for errors
- Try a different browser

---

## 📞 Quick Actions Reference

### **From Overview:**
- "Create Manual Booking" → Opens booking form
- "Send Announcement" → Future feature for notifications
- "Emergency Shutdown" → Disable all bookings

### **From Bookings:**
- Click status badges → Filter by that status
- "View" icon → See full booking details
- "Edit" icon → Modify booking
- "Cancel" icon → Cancel booking

### **From Games:**
- "Add New Game" → Create new game
- "Edit" button → Modify game details
- "Maintenance" button → Toggle maintenance mode
- Chart icon → View analytics (coming soon)

### **From Customers:**
- "View" icon → See customer profile
- "Email" icon → Contact customer
- Click segment → Filter by that segment

---

## 🎯 Next Steps

1. **Explore each section** to familiarize yourself
2. **Try the filters** to see how they work
3. **Check the charts** for visual insights
4. **Test mobile view** on your phone
5. **Create test bookings** to see data populate

---

## 💡 Pro Tips

1. **Bookmark frequently used sections** in your browser
2. **Check Overview first thing** each day
3. **Use filters** to find data quickly
4. **Monitor Revenue daily** for payment issues
5. **Review Reports weekly** for trends

---

Enjoy your new powerful Owner Dashboard! 🎉

For support, check the main documentation or contact your administrator.
