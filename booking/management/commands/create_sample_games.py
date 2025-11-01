"""
Django management command to create sample games for testing
"""
from django.core.management.base import BaseCommand
from booking.models import Game
from booking.slot_generator import SlotGenerator
from datetime import date, timedelta, time


class Command(BaseCommand):
    help = 'Create sample games for testing the hybrid booking system'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating sample games...')
        
        # Sample games data
        games_data = [
            {
                'name': '8-Ball Pool',
                'description': 'Classic pool table game for up to 4 players. Perfect for friends and competitive play.',
                'capacity': 4,
                'booking_type': 'HYBRID',
                'opening_time': time(11, 0),  # 11:00 AM
                'closing_time': time(23, 0),  # 11:00 PM
                'slot_duration_minutes': 60,
                'available_days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                'private_price': 400.00,
                'shared_price': 100.00,
                'is_active': True
            },
            {
                'name': 'Table Tennis',
                'description': 'Fast-paced table tennis for 2-4 players. Great for exercise and fun.',
                'capacity': 4,
                'booking_type': 'HYBRID',
                'opening_time': time(10, 0),  # 10:00 AM
                'closing_time': time(22, 0),  # 10:00 PM
                'slot_duration_minutes': 60,
                'available_days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                'private_price': 300.00,
                'shared_price': 75.00,
                'is_active': True
            },
            {
                'name': 'PS5 Console 1',
                'description': 'Latest PlayStation 5 console with popular games. Single player experience.',
                'capacity': 1,
                'booking_type': 'SINGLE',
                'opening_time': time(12, 0),  # 12:00 PM
                'closing_time': time(23, 59),  # 11:59 PM
                'slot_duration_minutes': 60,
                'available_days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                'private_price': 200.00,
                'shared_price': None,
                'is_active': True
            },
            {
                'name': 'Gaming PC 1',
                'description': 'High-end gaming PC with latest games and VR support. Single player setup.',
                'capacity': 1,
                'booking_type': 'SINGLE',
                'opening_time': time(9, 0),   # 9:00 AM
                'closing_time': time(23, 0),  # 11:00 PM
                'slot_duration_minutes': 60,
                'available_days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                'private_price': 250.00,
                'shared_price': None,
                'is_active': True
            },
            {
                'name': 'Carrom Board',
                'description': 'Traditional carrom board game for 2-4 players. Family-friendly fun.',
                'capacity': 4,
                'booking_type': 'HYBRID',
                'opening_time': time(10, 0),  # 10:00 AM
                'closing_time': time(21, 0),  # 9:00 PM
                'slot_duration_minutes': 90,  # 1.5 hour slots
                'available_days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                'private_price': 200.00,
                'shared_price': 50.00,
                'is_active': True
            }
        ]
        
        created_count = 0
        
        for game_data in games_data:
            # Check if game already exists
            if Game.objects.filter(name=game_data['name']).exists():
                self.stdout.write(f'Game "{game_data["name"]}" already exists, skipping...')
                continue
            
            # Create the game
            game = Game.objects.create(**game_data)
            created_count += 1
            
            self.stdout.write(f'Created game: {game.name}')
            
            # Generate initial slots for next 30 days
            start_date = date.today()
            end_date = start_date + timedelta(days=30)
            
            slots_created = SlotGenerator.generate_slots_for_game(game, start_date, end_date)
            self.stdout.write(f'  - Generated {slots_created} time slots')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} games!')
        )
        
        if created_count > 0:
            self.stdout.write('\nNext steps:')
            self.stdout.write('1. Visit /booking/games/ to see the new game selection interface')
            self.stdout.write('2. Test hybrid booking with pool and table tennis')
            self.stdout.write('3. Test single booking with PS5 and Gaming PC')
            self.stdout.write('4. Check the admin panel to manage games and slots')
        else:
            self.stdout.write('\nAll sample games already exist. You can:')
            self.stdout.write('1. Visit /booking/games/ to test the booking system')
            self.stdout.write('2. Use the admin panel to modify existing games')
            self.stdout.write('3. Run with --force to recreate games')