#!/usr/bin/env python
"""
Update 8 Ball Pool games with reasonable slot settings
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaming_cafe.settings')
django.setup()

from booking.models import Game, GameSlot, SlotAvailability
from datetime import time
from decimal import Decimal

def main():
    print("=" * 70)
    print("Creating 8 Ball Pool Game - 60 min slots, 24/7 availability")
    print("=" * 70)
    print()
    
    # Clear all existing 8 Ball Pool games and slots
    print("Clearing existing 8 Ball Pool games...")
    Game.objects.filter(name__contains='8 Ball Pool').delete()
    print("  Cleared old games and slots")
    print()
    
    # All days available
    all_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    # Create single game: 8 Ball Pool with 60-minute slots
    print("Creating Game: 8 Ball Pool (60 min slots)...")
    game = Game.objects.create(
        name='8 Ball Pool',
        description='Classic 8 Ball Pool game with 60-minute slots. Available 24/7 for Razorpay testing!',
        capacity=2,
        booking_type='HYBRID',
        opening_time=time(0, 0),     # Midnight - 24 hours
        closing_time=time(23, 59),   # 11:59 PM
        slot_duration_minutes=60,     # 60-minute slots
        available_days=all_days,
        private_price=Decimal('120.00'),  # Rs.2 per minute x 60
        shared_price=Decimal('60.00'),    # Half for shared
        is_active=True
    )
    print(f"  Created: {game.name}")
    print(f"  Duration: 60 minutes per slot")
    print(f"  Private Price: Rs.{game.private_price}")
    print(f"  Shared Price: Rs.{game.shared_price}/person")
    print()
    
    # Generate slots for next 7 days
    print("Generating slots for next 7 days...")
    game.generate_slots(days_ahead=7)
    slot_count = game.slots.count()
    print(f"  Generated {slot_count} slots (24 slots/day x 7 days)")
    print()
    
    print("=" * 70)
    print("SUCCESS! Game ready for testing")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  Game: {game.name}")
    print(f"  Slot Duration: 60 minutes")
    print(f"  Total Slots: {slot_count}")
    print(f"  Private Booking: Rs.{game.private_price}")
    print(f"  Shared Booking: Rs.{game.shared_price}/person")
    print(f"  Operating Hours: 24/7")
    print(f"  Available: Next 7 days")
    print()
    print("Razorpay testers can book anytime!")
    print()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)
