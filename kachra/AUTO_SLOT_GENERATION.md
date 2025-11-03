# Automatic Slot Generation System

## Overview
This system automatically maintains a **rolling 7-day window** of available booking slots **without requiring cron jobs or manual intervention**.

## How It Works

### 🔄 Background Processing
1. **Middleware Check** - On the first request each day, the system checks if slots need to be generated
2. **Background Thread** - Slot generation runs in a separate thread, never blocking user requests
3. **Smart Caching** - Each game is only checked once per hour to avoid overhead
4. **Rolling Window** - Always maintains 7 days of slots ahead

### 📍 Where It Runs

**Primary Trigger:**
- `booking.middleware.AutoSlotMaintenanceMiddleware` - Runs on first request of the day

**Secondary Trigger:**
- `booking/views.py:game_selection()` - Ensures slots exist when customers view booking page

### ⚡ Performance

- **User Impact:** ZERO - Runs in background threads
- **Page Load:** Normal speed (0.5-1 second)
- **Slot Check:** Once per hour per game (cached)
- **Daily Check:** Once per day (cached for 24 hours)

## Components

### 1. AutoSlotGenerator (`booking/auto_slot_generator.py`)
Main logic for slot generation:
- Checks if slots exist for next 7 days
- Generates missing slots in background
- Uses caching to avoid excessive checks

### 2. AutoSlotMaintenanceMiddleware (`booking/middleware.py`)
Django middleware that:
- Runs on every request (but checks are cached)
- Triggers daily slot generation in background
- Never blocks user requests

### 3. Integration Points
- **Game Selection View** - Ensures slots before showing booking page
- **Game Creation** - Generates initial 7 days via AJAX with progress bar

## Configuration

### Settings
Located in `booking/auto_slot_generator.py`:

```python
DAYS_TO_MAINTAIN = 7  # Always keep 7 days of slots ahead
CHECK_INTERVAL = 3600  # Check each game once per hour
```

### Adjust Settings
To change behavior:
- **More days ahead:** Increase `DAYS_TO_MAINTAIN` (e.g., 14 for 2 weeks)
- **Check more frequently:** Decrease `CHECK_INTERVAL` (e.g., 1800 for every 30 min)

## Manual Operations

### Force Slot Generation
```bash
# For all games
python manage.py generate_daily_slots

# For specific game
python manage.py generate_daily_slots --game-id <UUID>

# For more days
python manage.py generate_daily_slots --days 14
```

### Test Auto-Generation
```python
from booking.auto_slot_generator import auto_generate_slots_all_games

# Test in Django shell
auto_generate_slots_all_games(async_mode=False)  # Synchronous for testing
```

## Deployment

### Vercel/Serverless
✅ Works perfectly - no cron needed  
✅ Background threads supported  
✅ Caching via Django cache  

### Traditional Servers
✅ Works perfectly  
✅ Can optionally add cron job for redundancy  
✅ No special configuration needed  

## Monitoring

### Check Logs
```python
import logging
logger = logging.getLogger(__name__)

# Look for these log messages:
# 🔄 Auto-generating slots for {game.name}
# ✅ Created {X} slots for {game.name}
# ❌ Error auto-generating slots
```

### Verify Slots
```python
from booking.models import GameSlot
from datetime import date, timedelta

# Check if slots exist for next 7 days
today = date.today()
future_date = today + timedelta(days=7)

slots = GameSlot.objects.filter(
    date__range=[today, future_date],
    is_active=True
).count()

print(f"Available slots: {slots}")
```

## Benefits

✅ **No Cron Jobs** - Works on serverless platforms like Vercel  
✅ **Self-Healing** - Automatically fixes missing slots  
✅ **Zero User Impact** - Runs in background  
✅ **Smart Caching** - Efficient, doesn't waste resources  
✅ **Maintenance-Free** - Set it and forget it  
✅ **Rolling Window** - Always maintains 7 days ahead  

## Troubleshooting

### Slots Not Generating?
1. Check if games are active: `Game.objects.filter(is_active=True)`
2. Check Django cache: `python manage.py shell` → `from django.core.cache import cache; cache.clear()`
3. Force generation: `python manage.py generate_daily_slots`

### Too Many Checks?
- Increase `CHECK_INTERVAL` in `auto_slot_generator.py`
- Adjust middleware to check less frequently

### Need More Days Ahead?
- Change `DAYS_TO_MAINTAIN` in `auto_slot_generator.py`
- Run manual command: `python manage.py generate_daily_slots --days 14`
