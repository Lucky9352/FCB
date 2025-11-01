"""
Management command to create a test game (8 Ball Pool) with always-available slots
for Razorpay testing purposes.

Usage: python manage.py setup_razorpay_test_game
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time
from booking.models import Game
from decimal import Decimal


class Command(BaseCommand):
    help = 'Creates test game "8 Ball Pool" with always-available slots for Razorpay testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Setting up Razorpay Test Game: 8 Ball Pool'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')

        # Create Game 1: 8 Ball Pool with 23-minute slots
        game_23min = self.create_test_game(
            name='8 Ball Pool (23 min)',
            duration=23,
            private_price=Decimal('46.00'),  # ₹2 per minute
            shared_price=Decimal('23.00')    # Half for shared
        )
        
        # Create Game 2: 8 Ball Pool with 59-minute slots
        game_59min = self.create_test_game(
            name='8 Ball Pool (59 min)',
            duration=59,
            private_price=Decimal('118.00'),  # ₹2 per minute
            shared_price=Decimal('59.00')     # Half for shared
        )
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('✅ Test Games Setup Complete!'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('Game 1 Details:'))
        self.stdout.write(f'  Name: {game_23min.name}')
        self.stdout.write(f'  Duration: {game_23min.slot_duration_minutes} minutes')
        self.stdout.write(f'  Private Price: ₹{game_23min.private_price}')
        self.stdout.write(f'  Shared Price: ₹{game_23min.shared_price}/person')
        self.stdout.write(f'  Capacity: {game_23min.capacity} players')
        self.stdout.write(f'  Available: 11:00 AM - 11:00 PM (All days)')
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('Game 2 Details:'))
        self.stdout.write(f'  Name: {game_59min.name}')
        self.stdout.write(f'  Duration: {game_59min.slot_duration_minutes} minutes')
        self.stdout.write(f'  Private Price: ₹{game_59min.private_price}')
        self.stdout.write(f'  Shared Price: ₹{game_59min.shared_price}/person')
        self.stdout.write(f'  Capacity: {game_59min.capacity} players')
        self.stdout.write(f'  Available: 11:00 AM - 11:00 PM (All days)')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎮 Razorpay testers can now book these games anytime!'))
        self.stdout.write(self.style.SUCCESS('📅 Slots are auto-generated for the next 30 days'))
        self.stdout.write('')

    def create_test_game(self, name, duration, private_price, shared_price):
        """Create or update a test game with specific settings"""
        self.stdout.write(f'🎮 Creating game: {name}...')
        
        # All weekdays available
        all_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        
        game, created = Game.objects.update_or_create(
            name=name,
            defaults={
                'description': f'Classic 8 Ball Pool game ({duration} min slots) - Available daily for Razorpay testing. Book anytime to test the payment integration!',
                'capacity': 2,  # 2 players for pool
                'booking_type': 'HYBRID',  # Allows both private and shared bookings
                'opening_time': time(11, 0),  # 11:00 AM
                'closing_time': time(23, 0),  # 11:00 PM
                'slot_duration_minutes': duration,
                'available_days': all_days,
                'private_price': private_price,
                'shared_price': shared_price,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✅ Created new game: {name}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'  ✅ Updated existing game: {name}'))
        
        # Trigger slot generation
        game.generate_slots()
        slot_count = game.slots.count()
        self.stdout.write(self.style.SUCCESS(f'  ✅ Generated {slot_count} slots'))
        
        return game
