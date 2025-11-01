# Custom Slots Feature - Complete Guide

## Overview
The Custom Slots feature allows cafe owners to add special time slots outside the regular game schedule. This is perfect for:
- **Extended hours** during holidays
- **Special events** or tournaments
- **Emergency availability** when regular slots are full
- **One-time sessions** for VIP customers

## How to Access
1. Log in as a cafe owner
2. Click **"Add Custom Slots"** button in the sidebar (green button with calendar+ icon)
3. Fill out the form and preview slots before creating

## Feature Highlights

### 🎮 Game Selection
- Dropdown showing all active games
- Automatically shows game type (Per Hour/Per Game/PC Station)
- Auto-fills default slot duration when game is selected

### 📅 Flexible Date Range
- **Single Day**: Just select start date
- **Multiple Days**: Select both start and end date
- System prevents past dates
- Can create slots for up to weeks in advance

### ⏰ Time Range
- Choose start time (e.g., 10:00 AM)
- Choose end time (e.g., 6:00 PM)
- System validates end time is after start time

### ⏱️ Slot Duration
- Default: 60 minutes per slot
- Common options: 30, 60, 90, 120 minutes
- Minimum: 15 minutes
- Maximum: 480 minutes (8 hours)
- Auto-updates based on selected game

### 👁️ Preview Function
- Click "Preview Slots" to see what will be created
- Shows:
  - Selected game name
  - Date range (number of days)
  - Time range
  - Slot duration
  - **Total slots to create**
  - Calculation breakdown

### ✅ Smart Slot Generation
- Automatically generates ALL slots in the time range
- **Example**: 10:00 AM - 6:00 PM with 60-min duration = 8 slots
  - 10:00-11:00, 11:00-12:00, 12:00-1:00, etc.
- Skips already existing slots (no duplicates)
- Works across multiple days seamlessly
- Atomic transaction (all or nothing)

## Usage Examples

### Example 1: Holiday Extended Hours
**Scenario**: Christmas Day, stay open late
- Game: PS5 Gaming Station
- Date: 2024-12-25 (single day)
- Time: 8:00 PM - 12:00 AM
- Duration: 60 minutes
- **Result**: 4 extra slots created

### Example 2: Weekend Tournament
**Scenario**: 3-day tournament event
- Game: Valorant PC Station
- Start Date: 2024-06-14
- End Date: 2024-06-16
- Time: 9:00 AM - 9:00 PM
- Duration: 120 minutes (2-hour sessions)
- **Result**: 6 slots/day × 3 days = 18 total slots

### Example 3: Emergency Availability
**Scenario**: Regular slots full, need more capacity today
- Game: FIFA 24
- Date: Today
- Time: 2:00 PM - 5:00 PM
- Duration: 30 minutes
- **Result**: 6 quick slots added immediately

## Technical Details

### Backend Logic
- **View**: `booking/game_management_views.py::custom_slot_create()`
- **Template**: `templates/authentication/owner_custom_slots.html`
- **URL**: `/booking/games/manage/custom-slots/create/`
- **Database**: Creates `GameSlot` objects with `is_available=True`

### Validation Rules
1. End date cannot be before start date
2. End time must be after start time
3. Only active games shown
4. Duplicate slots are skipped (not errors)
5. Minimum date is today (no past slots)

### Calculation Formula
```
Slots per day = floor((end_time - start_time) / slot_duration)
Total slots = slots_per_day × number_of_days
```

### Database Transaction
- Uses `transaction.atomic()` for safety
- If any error occurs, NO slots are created
- All slots created successfully or none at all

## User Interface

### Navigation
- Highlighted in **green** in sidebar
- Icon: Calendar with plus sign
- Always visible when logged in as owner

### Form Layout
- Clear sections with icons
- Helpful tooltips and examples
- Real-time validation
- Preview before committing

### Success Message
```
Successfully created 18 custom slot(s) for Valorant PC Station
from 2024-06-14 to 2024-06-16.
```

### Error Handling
- Clear error messages
- Form preserves entered data
- Validation errors highlighted
- Network errors caught gracefully

## Best Practices

### ✅ Do's
- **Preview first** - Always check slot count before creating
- **Reasonable durations** - Stick to 30/60/90/120 minutes
- **Check calendar** - Avoid conflicts with existing bookings
- **Test with single day** - For large ranges, test one day first

### ❌ Don'ts
- **Too many slots** - Creating 1000+ slots may slow down
- **Too short duration** - 15-min slots create maintenance overhead
- **Random times** - Keep slot times consistent with regular schedule
- **Past dates** - System blocks this, but don't try

## Monitoring

### How to Check Created Slots
1. Go to **Games & Stations** in sidebar
2. Click on the game you created slots for
3. View all slots including custom ones
4. Custom slots look identical to auto-generated slots

### Deleting Custom Slots
- No bulk delete yet (future feature)
- Contact support if you need to remove many slots
- Individual slots can be deleted from game detail page

## Troubleshooting

### "No games available"
- **Cause**: All games are inactive
- **Solution**: Activate at least one game first

### "Invalid date or time format"
- **Cause**: Browser autocomplete or manual typing
- **Solution**: Use date/time pickers provided

### "0 slots created"
- **Cause**: All slots already exist in that range
- **Solution**: Check game detail page for existing slots

### Preview shows wrong count
- **Cause**: JavaScript calculation doesn't account for existing slots
- **Solution**: Preview is estimate; actual may be less

## Future Enhancements (Planned)
- 📊 Bulk delete custom slots
- 🔄 Clone custom slot ranges
- 📧 Email notification when slots created
- 📈 Analytics on custom slot usage
- 🎯 Recurring custom slots (weekly/monthly)

## Support
If you encounter issues:
1. Check this guide first
2. Verify your game is active
3. Try with a small test (1 day, 2-3 slots)
4. Contact technical support with screenshot

---

**Last Updated**: June 2024  
**Version**: 1.0.0  
**Component**: Owner Dashboard - Custom Slots Management
