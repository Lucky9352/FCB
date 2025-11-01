#!/usr/bin/env python
"""
Quick script to create 8 Ball Pool test games for Razorpay testing
Run: python setup_test_games.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaming_cafe.settings')
django.setup()

from booking.models import Game
from datetime import time
from decimal import Decimal

def main():
    print("=" * 70)
    print("Setting up 8 Ball Pool Test Games for Razorpay Testing")
    print("=" * 70)
    print()
    
    # All days available
    all_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    # Create Game 1: 8 Ball Pool (23 min)
    print("Creating Game 1: 8 Ball Pool (23 min)...")
    game1, created1 = Game.objects.update_or_create(
        name='8 Ball Pool (23 min)',
        defaults={
            'description': 'Classic 8 Ball Pool game with 23-minute slots. Perfect for quick matches! Available 24/7 for testing the payment system.',
            'capacity': 2,
            'booking_type': 'HYBRID',
            'opening_time': time(0, 0),    # Midnight
            'closing_time': time(23, 59),  # 11:59 PM
            'slot_duration_minutes': 23,
            'available_days': all_days,
            'private_price': Decimal('46.00'),
            'shared_price': Decimal('23.00'),
            'is_active': True
        }
    )
    print(f"  Status: {'Created' if created1 else 'Updated'}")
    print(f"  Duration: {game1.slot_duration_minutes} minutes")
    print(f"  Private Price: Rs.{game1.private_price}")
    print(f"  Shared Price: Rs.{game1.shared_price}/person")
    print(f"  Slots generated: {game1.slots.count()}")
    print()
    
    # Create Game 2: 8 Ball Pool (59 min)
    print("Creating Game 2: 8 Ball Pool (59 min)...")
    game2, created2 = Game.objects.update_or_create(
        name='8 Ball Pool (59 min)',
        defaults={
            'description': 'Classic 8 Ball Pool game with 59-minute slots. Extended playtime for serious players! Available 24/7 for testing the payment system.',
            'capacity': 2,
            'booking_type': 'HYBRID',
            'opening_time': time(0, 0),    # Midnight
            'closing_time': time(23, 59),  # 11:59 PM
            'slot_duration_minutes': 59,
            'available_days': all_days,
            'private_price': Decimal('118.00'),
            'shared_price': Decimal('59.00'),
            'is_active': True
        }
    )
    print(f"  Status: {'Created' if created2 else 'Updated'}")
    print(f"  Duration: {game2.slot_duration_minutes} minutes")
    print(f"  Private Price: Rs.{game2.private_price}")
    print(f"  Shared Price: Rs.{game2.shared_price}/person")
    print(f"  Slots generated: {game2.slots.count()}")
    print()
    
    print("=" * 70)
    print("SUCCESS! Test games are ready for Razorpay testing")
    print("=" * 70)
    print()
    print("Next Steps for Testing:")
    print("1. Login to customer dashboard")
    print("2. Browse available games")
    print("3. Select '8 Ball Pool' (either version)")
    print("4. Choose a time slot")
    print("5. Select booking type (Private or Shared)")
    print("6. Proceed to checkout")
    print("7. Test Razorpay payment")
    print()
    print("Access URLs:")
    print("- Customer Login: http://localhost:8000/accounts/login/")
    print("- Browse Games: http://localhost:8000/booking/games/")
    print()

if __name__ == '__main__':
    main()
