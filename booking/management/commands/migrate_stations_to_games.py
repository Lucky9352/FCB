"""
Django management command to migrate existing GamingStation data to Game model
This is a one-time migration script to help transition from the old model to the new one
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from booking.models import GamingStation, Game, GameSlot, SlotAvailability
from booking.slot_generator import SlotGenerator
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Migrate existing GamingStation data to new Game model'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without making changes'
        )
        
        parser.add_argument(
            '--generate-slots',
            action='store_true',
            help='Generate initial slots for migrated games'
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        generate_slots = options['generate_slots']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        self.stdout.write('Starting migration from GamingStation to Game model...')
        
        # Get all gaming stations
        stations = GamingStation.objects.all()
        
        if not stations.exists():
            self.stdout.write(self.style.SUCCESS('No gaming stations found to migrate'))
            return
        
        self.stdout.write(f'Found {stations.count()} gaming stations to migrate')
        
        migrated_count = 0
        
        with transaction.atomic():
            for station in stations:
                self.stdout.write(f'Migrating: {station.name}')
                
                # Create equivalent Game
                game_data = {
                    'name': station.name,
                    'description': station.description or f'{station.get_station_type_display()} gaming setup',
                    'capacity': 1,  # Default to single player
                    'booking_type': 'SINGLE',  # Default to single booking
                    'opening_time': '10:00',  # Default opening time
                    'closing_time': '22:00',  # Default closing time
                    'slot_duration_minutes': 60,  # Default 1 hour slots
                    'available_days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                    'private_price': station.hourly_rate,
                    'shared_price': None,  # Single booking only
                    'is_active': station.is_active and not station.is_maintenance,
                    'image': station.image
                }
                
                if not dry_run:
                    # Check if game already exists
                    existing_game = Game.objects.filter(name=station.name).first()
                    if existing_game:
                        self.stdout.write(f'  - Game already exists: {existing_game.name}')
                        continue
                    
                    # Create the game
                    game = Game.objects.create(**game_data)
                    
                    # Generate initial slots if requested
                    if generate_slots:
                        start_date = date.today()
                        end_date = start_date + timedelta(days=30)
                        slots_created = SlotGenerator.generate_slots_for_game(game, start_date, end_date)
                        self.stdout.write(f'  - Created {slots_created} initial slots')
                    
                    migrated_count += 1
                    self.stdout.write(f'  - Created game: {game.name}')
                else:
                    self.stdout.write(f'  - Would create game with data: {game_data}')
                    migrated_count += 1
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'DRY RUN: Would migrate {migrated_count} stations to games')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully migrated {migrated_count} stations to games')
            )
        
        # Show next steps
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Review the migrated games in the admin panel')
        self.stdout.write('2. Update game settings (capacity, booking type, schedule) as needed')
        self.stdout.write('3. Test the new booking flow with hybrid options')
        self.stdout.write('4. Update existing bookings to use the new Game model')
        self.stdout.write('5. Remove the old GamingStation model after verification')