"""
Django management command for custom slot management
Provides interface for cafe owners to add, update, and delete custom slots
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime, date, time
from booking.models import Game, GameSlot
from booking.slot_generator import SlotGenerator
import json


class Command(BaseCommand):
    help = 'Manage custom slots for games'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['create', 'update', 'delete', 'list', 'preview'],
            help='Action to perform'
        )
        
        parser.add_argument(
            '--game-id',
            type=str,
            help='Game ID (required for most actions)'
        )
        
        parser.add_argument(
            '--slot-id',
            type=str,
            help='Slot ID (required for update/delete actions)'
        )
        
        parser.add_argument(
            '--date',
            type=str,
            help='Date for the slot (YYYY-MM-DD format)'
        )
        
        parser.add_argument(
            '--start-time',
            type=str,
            help='Start time (HH:MM format)'
        )
        
        parser.add_argument(
            '--end-time',
            type=str,
            help='End time (HH:MM format)'
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force action even with conflicts/bookings'
        )
        
        parser.add_argument(
            '--bulk-file',
            type=str,
            help='JSON file with bulk slot definitions'
        )
    
    def handle(self, *args, **options):
        action = options['action']
        
        try:
            if action == 'create':
                self.handle_create(options)
            elif action == 'update':
                self.handle_update(options)
            elif action == 'delete':
                self.handle_delete(options)
            elif action == 'list':
                self.handle_list(options)
            elif action == 'preview':
                self.handle_preview(options)
                
        except Exception as e:
            raise CommandError(f'Command failed: {str(e)}')
    
    def handle_create(self, options):
        """Handle custom slot creation"""
        game_id = options.get('game_id')
        if not game_id:
            raise CommandError('--game-id is required for create action')
        
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            raise CommandError(f'Game with ID {game_id} not found')
        
        # Check for bulk creation
        bulk_file = options.get('bulk_file')
        if bulk_file:
            self.handle_bulk_create(game, bulk_file)
            return
        
        # Single slot creation
        date_str = options.get('date')
        start_time_str = options.get('start_time')
        end_time_str = options.get('end_time')
        
        if not all([date_str, start_time_str, end_time_str]):
            raise CommandError('--date, --start-time, and --end-time are required for single slot creation')
        
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
        except ValueError as e:
            raise CommandError(f'Invalid date/time format: {e}')
        
        result = SlotGenerator.create_custom_slot(
            game=game,
            target_date=target_date,
            start_time=start_time,
            end_time=end_time
        )
        
        if result['success']:
            self.stdout.write(
                self.style.SUCCESS(f'Created custom slot: {result["slot"]}')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'Failed to create slot: {", ".join(result["errors"])}')
            )
    
    def handle_bulk_create(self, game, bulk_file):
        """Handle bulk custom slot creation from JSON file"""
        try:
            with open(bulk_file, 'r') as f:
                slot_definitions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise CommandError(f'Error reading bulk file: {e}')
        
        # Convert string dates/times to proper objects
        processed_definitions = []
        for slot_def in slot_definitions:
            try:
                processed_definitions.append({
                    'date': datetime.strptime(slot_def['date'], '%Y-%m-%d').date(),
                    'start_time': datetime.strptime(slot_def['start_time'], '%H:%M').time(),
                    'end_time': datetime.strptime(slot_def['end_time'], '%H:%M').time()
                })
            except (KeyError, ValueError) as e:
                raise CommandError(f'Invalid slot definition: {e}')
        
        result = SlotGenerator.bulk_create_custom_slots(game, processed_definitions)
        
        if result['success']:
            self.stdout.write(
                self.style.SUCCESS(f'Created {result["created_count"]} custom slots')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'Bulk creation failed: {", ".join(result["errors"])}')
            )
    
    def handle_update(self, options):
        """Handle custom slot update"""
        slot_id = options.get('slot_id')
        if not slot_id:
            raise CommandError('--slot-id is required for update action')
        
        # Parse optional new values
        new_date = None
        new_start_time = None
        new_end_time = None
        
        if options.get('date'):
            try:
                new_date = datetime.strptime(options['date'], '%Y-%m-%d').date()
            except ValueError:
                raise CommandError('Invalid date format (use YYYY-MM-DD)')
        
        if options.get('start_time'):
            try:
                new_start_time = datetime.strptime(options['start_time'], '%H:%M').time()
            except ValueError:
                raise CommandError('Invalid start time format (use HH:MM)')
        
        if options.get('end_time'):
            try:
                new_end_time = datetime.strptime(options['end_time'], '%H:%M').time()
            except ValueError:
                raise CommandError('Invalid end time format (use HH:MM)')
        
        result = SlotGenerator.update_custom_slot(
            slot_id=slot_id,
            new_date=new_date,
            new_start_time=new_start_time,
            new_end_time=new_end_time
        )
        
        if result['success']:
            self.stdout.write(
                self.style.SUCCESS(f'Updated custom slot: {result["slot"]}')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'Failed to update slot: {", ".join(result["errors"])}')
            )
    
    def handle_delete(self, options):
        """Handle custom slot deletion"""
        slot_id = options.get('slot_id')
        if not slot_id:
            raise CommandError('--slot-id is required for delete action')
        
        force = options.get('force', False)
        
        result = SlotGenerator.delete_custom_slot(slot_id, force=force)
        
        if result['success']:
            self.stdout.write(
                self.style.SUCCESS(f'Deleted custom slot {slot_id}')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'Failed to delete slot: {", ".join(result["errors"])}')
            )
    
    def handle_list(self, options):
        """Handle listing custom slots"""
        game_id = options.get('game_id')
        
        if game_id:
            try:
                game = Game.objects.get(id=game_id)
                slots = SlotGenerator.get_custom_slots_for_game(game)
                self.stdout.write(f'Custom slots for {game.name}:')
            except Game.DoesNotExist:
                raise CommandError(f'Game with ID {game_id} not found')
        else:
            slots = GameSlot.objects.filter(is_custom=True, is_active=True).select_related('game')
            self.stdout.write('All custom slots:')
        
        if not slots.exists():
            self.stdout.write('No custom slots found.')
            return
        
        for slot in slots:
            booking_count = slot.bookings.filter(status__in=['CONFIRMED', 'IN_PROGRESS']).count()
            availability = getattr(slot, 'availability', None)
            
            status_info = []
            if booking_count > 0:
                status_info.append(f'{booking_count} bookings')
            
            if availability:
                status_info.append(f'{availability.available_spots}/{availability.total_capacity} available')
            
            status_str = f' ({", ".join(status_info)})' if status_info else ''
            
            self.stdout.write(
                f'  {slot.id}: {slot.game.name} - {slot.date} {slot.start_time}-{slot.end_time}{status_str}'
            )
    
    def handle_preview(self, options):
        """Handle slot generation preview"""
        game_id = options.get('game_id')
        date_str = options.get('date')
        
        if not game_id:
            raise CommandError('--game-id is required for preview action')
        
        if not date_str:
            raise CommandError('--date is required for preview action')
        
        try:
            game = Game.objects.get(id=game_id)
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except Game.DoesNotExist:
            raise CommandError(f'Game with ID {game_id} not found')
        except ValueError:
            raise CommandError('Invalid date format (use YYYY-MM-DD)')
        
        preview = SlotGenerator.get_slot_generation_preview(game, target_date)
        
        if preview['errors']:
            self.stdout.write(
                self.style.ERROR(f'Preview errors: {", ".join(preview["errors"])}')
            )
            return
        
        if preview['warnings']:
            self.stdout.write(
                self.style.WARNING(f'Warnings: {", ".join(preview["warnings"])}')
            )
        
        self.stdout.write(f'Slot preview for {game.name} on {target_date}:')
        
        if not preview['slots']:
            self.stdout.write('No slots would be generated.')
            return
        
        for slot in preview['slots']:
            self.stdout.write(
                f'  {slot["start_time"]}-{slot["end_time"]} '
                f'({slot["duration_minutes"]} min, '
                f'capacity: {slot["capacity"]}, '
                f'private: ₹{slot["private_price"]}'
                f'{f", shared: ₹{slot["shared_price"]}" if slot["shared_price"] else ""})'
            )
        
        self.stdout.write(f'Total slots: {len(preview["slots"])}')