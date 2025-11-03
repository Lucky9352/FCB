"""
Test script to explain slot timing behavior and timezone handling
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaming_cafe.settings')
django.setup()

from django.utils import timezone
from booking.models import GameSlot, Game
from datetime import datetime, time
import pytz

ist = pytz.timezone('Asia/Kolkata')
now = timezone.now()
now_ist = now.astimezone(ist)

print('=' * 70)
print('SLOT TIMING & TIMEZONE BEHAVIOR EXPLANATION')
print('=' * 70)
print()

print('CURRENT TIME')
print(f'   IST: {now_ist.strftime("%I:%M %p")} ({now_ist.strftime("%H:%M")})')
print()

print('=' * 70)
print('QUESTION 1: If slot is 5:00 PM - 6:00 PM, will it show at 5:15 PM?')
print('=' * 70)

# Simulate a 5:00 PM slot
slot_time = time(17, 0)  # 5:00 PM
slot_datetime = timezone.make_aware(
    datetime.combine(now_ist.date(), slot_time),
    timezone=ist
)

# Simulate checking at 5:15 PM
check_time_515 = timezone.make_aware(
    datetime.combine(now_ist.date(), time(17, 15)),
    timezone=ist
)

print(f'Slot Start: {slot_datetime.strftime("%I:%M %p")}')
print(f'Checking at: {check_time_515.strftime("%I:%M %p")}')
print(f'Slot < Check Time: {slot_datetime < check_time_515}')
print()
print('ANSWER: NO - The slot will NOT show at 5:15 PM')
print('   Reason: Slot started at 5:00 PM, current time 5:15 PM is AFTER start')
print('   Status: PAST SLOT - Already started, so hidden from booking')
print()

print('=' * 70)
print('QUESTION 2: What timezone are game times stored in?')
print('=' * 70)

# Check a real game
game = Game.objects.filter(is_active=True).first()
if game:
    print(f'Game: {game.name}')
    print(f'Opening Time (DB): {game.opening_time}')
    print(f'Closing Time (DB): {game.closing_time}')
    print()
    print('IMPORTANT: Times are stored as TIME objects (no timezone)')
    print('   When you create a game with opening_time = 09:00')
    print('   It stores: 09:00 (no timezone attached)')
    print()
    print('   When slots are generated:')
    print('   1. System takes this 09:00 time')
    print('   2. Combines with date to create datetime')
    print('   3. Makes it timezone-aware using IST (Asia/Kolkata)')
    print('   4. So 09:00 becomes 09:00 IST')
    print()
    print('ANSWER: Times you enter are DIRECTLY used as IST times')
    print('   If you enter 5:00 PM, it creates 5:00 PM IST slot')
    print('   NO conversion happens - what you enter is what customers see')
    print()
    
print('=' * 70)
print('CURRENT SYSTEM BEHAVIOR SUMMARY')
print('=' * 70)
print()
print('1. GAME CREATION:')
print('   - You enter: Opening 9:00 AM, Closing 11:00 PM')
print('   - System stores: 09:00 and 23:00 (as time objects)')
print('   - Interpretation: These are IST times')
print()
print('2. SLOT GENERATION:')
print('   - Creates slots: 09:00, 10:00, 11:00... 23:00')
print('   - All times treated as IST')
print('   - Stored in database as time values')
print()
print('3. SLOT DISPLAY:')
print('   - Frontend fetches slots via API')
print('   - API checks: is slot_start_time < current_IST_time?')
print('   - If YES: Hide slot (already passed)')
print('   - If NO: Show slot (still in future)')
print()
print('4. EXAMPLE AT 5:15 PM IST:')
print('   - Slot 2:00 PM - 3:00 PM: HIDDEN (past)')
print('   - Slot 5:00 PM - 6:00 PM: HIDDEN (started 15 min ago)')
print('   - Slot 6:00 PM - 7:00 PM: SHOWN (future)')
print('   - Slot 8:00 PM - 9:00 PM: SHOWN (future)')
print()
print('=' * 70)
print('SYSTEM IS CONFIGURED FOR IST!')
print('=' * 70)
