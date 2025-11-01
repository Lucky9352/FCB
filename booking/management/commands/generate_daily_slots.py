"""
Django management command for daily slot generation
Run this as a scheduled task (e.g., cron job) to generate slots for all active games
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from booking.models import Game
from booking.slot_generator import SlotGenerator


class Command(BaseCommand):
    help = 'Generate time slots for all active games for upcoming dates'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days-ahead',
            type=int,
            default=30,
            help='Number of days ahead to generate slots for (default: 30)'
        )
        
        parser.add_argument(
            '--game-id',
            type=str,
            help='Generate slots for specific game ID only'
        )
        
        parser.add_argument(
            '--regenerate',
            action='store_true',
            help='Regenerate all slots (preserving existing bookings)'
        )
    
    def handle(self, *args, **options):
        days_ahead = options['days_ahead']
        game_id = options.get('game_id')
        regenerate = options['regenerate']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting slot generation for {days_ahead} days ahead...')
        )
        
        # Get games to process
        if game_id:
            try:
                games = [Game.objects.get(id=game_id)]
                self.stdout.write(f'Processing specific game: {games[0].name}')
            except Game.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Game with ID {game_id} not found')
                )
                return
        else:
            games = Game.objects.filter(is_active=True)
            self.stdout.write(f'Processing {games.count()} active games')
        
        total_created = 0
        total_deleted = 0
        total_errors = []
        
        for game in games:
            self.stdout.write(f'Processing game: {game.name}')
            
            try:
                if regenerate:
                    # Regenerate all slots
                    result = SlotGenerator.regenerate_slots_for_game(game, preserve_bookings=True, days_ahead=days_ahead)
                    created = result['created']
                    deleted = result['deleted']
                    preserved = result.get('preserved', 0)
                    errors = result.get('errors', [])
                    
                    self.stdout.write(
                        f'  - Regenerated: {deleted} deleted, {created} created, {preserved} preserved'
                    )
                    
                    if errors:
                        for error in errors:
                            self.stdout.write(self.style.WARNING(f'    Warning: {error}'))
                        total_errors.extend(errors)
                    
                    total_created += created
                    total_deleted += deleted
                    
                else:
                    # Generate new slots for upcoming dates
                    start_date = date.today()
                    end_date = start_date + timedelta(days=days_ahead)
                    
                    result = SlotGenerator.generate_slots_for_game(game, start_date, end_date)
                    created = result['created']
                    skipped = result['skipped']
                    errors = result.get('errors', [])
                    
                    self.stdout.write(f'  - Created {created} new slots, {skipped} days skipped')
                    
                    if errors:
                        for error in errors:
                            self.stdout.write(self.style.WARNING(f'    Warning: {error}'))
                        total_errors.extend(errors)
                    
                    total_created += created
                
            except Exception as e:
                error_msg = f'Error processing {game.name}: {e}'
                self.stdout.write(self.style.ERROR(f'  - {error_msg}'))
                total_errors.append(error_msg)
        
        # Summary
        if regenerate:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Slot regeneration completed: {total_deleted} deleted, {total_created} created'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Slot generation completed: {total_created} slots created')
            )
        
        # Show errors summary
        if total_errors:
            self.stdout.write(
                self.style.WARNING(f'\nTotal errors/warnings: {len(total_errors)}')
            )
            for error in total_errors[:5]:  # Show first 5 errors
                self.stdout.write(f'  - {error}')
            if len(total_errors) > 5:
                self.stdout.write(f'  ... and {len(total_errors) - 5} more')
        
        # Show next steps
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Set up a daily cron job to run this command')
        self.stdout.write('2. Monitor slot availability in the admin dashboard')
        self.stdout.write('3. Add custom slots as needed for special events')
        self.stdout.write('4. Use "manage_custom_slots.py" command for custom slot management')