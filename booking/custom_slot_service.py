"""
Custom Slot Management Service
Provides a clean interface for managing custom slots in the gaming cafe booking system
"""
from datetime import datetime, date, time, timedelta
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Game, GameSlot, SlotAvailability
from .slot_generator import SlotGenerator
import logging

logger = logging.getLogger(__name__)


class CustomSlotService:
    """Service class for managing custom slots"""
    
    @staticmethod
    def create_custom_slot(game_id, target_date, start_time, end_time, created_by=None):
        """
        Create a custom slot for a game
        
        Args:
            game_id: Game ID
            target_date: Date for the custom slot
            start_time: Start time for the slot
            end_time: End time for the slot
            created_by: User who created the slot (optional)
            
        Returns:
            dict: Creation result
        """
        try:
            game = Game.objects.get(id=game_id, is_active=True)
        except Game.DoesNotExist:
            return {
                'success': False,
                'errors': ['Game not found or inactive']
            }
        
        result = SlotGenerator.create_custom_slot(
            game=game,
            target_date=target_date,
            start_time=start_time,
            end_time=end_time
        )
        
        if result['success'] and created_by:
            # Log the creation for audit purposes
            logger.info(f"Custom slot created by {created_by}: {result['slot']}")
        
        return result
    
    @staticmethod
    def get_custom_slots_for_game(game_id, start_date=None, end_date=None):
        """
        Get custom slots for a specific game
        
        Args:
            game_id: Game ID
            start_date: Start date filter (optional)
            end_date: End date filter (optional)
            
        Returns:
            dict: Query result with slots or error
        """
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return {
                'success': False,
                'errors': ['Game not found']
            }
        
        slots = SlotGenerator.get_custom_slots_for_game(game, start_date, end_date)
        
        # Convert to serializable format
        slot_data = []
        for slot in slots:
            availability = getattr(slot, 'availability', None)
            booking_count = slot.bookings.filter(
                status__in=['CONFIRMED', 'IN_PROGRESS', 'PENDING']
            ).count()
            
            slot_data.append({
                'id': str(slot.id),
                'date': slot.date.isoformat(),
                'start_time': slot.start_time.strftime('%H:%M'),
                'end_time': slot.end_time.strftime('%H:%M'),
                'duration_minutes': int((
                    datetime.combine(slot.date, slot.end_time) - 
                    datetime.combine(slot.date, slot.start_time)
                ).total_seconds() / 60),
                'is_active': slot.is_active,
                'booking_count': booking_count,
                'availability': {
                    'total_capacity': availability.total_capacity if availability else game.capacity,
                    'booked_spots': availability.booked_spots if availability else 0,
                    'available_spots': availability.available_spots if availability else game.capacity,
                    'is_private_booked': availability.is_private_booked if availability else False,
                    'can_book_private': availability.can_book_private if availability else True,
                    'can_book_shared': availability.can_book_shared if availability else True,
                } if availability else None,
                'created_at': slot.created_at.isoformat()
            })
        
        return {
            'success': True,
            'slots': slot_data,
            'count': len(slot_data)
        }
    
    @staticmethod
    def update_custom_slot(slot_id, new_date=None, new_start_time=None, new_end_time=None, updated_by=None):
        """
        Update a custom slot
        
        Args:
            slot_id: Slot ID to update
            new_date: New date (optional)
            new_start_time: New start time (optional)
            new_end_time: New end time (optional)
            updated_by: User who updated the slot (optional)
            
        Returns:
            dict: Update result
        """
        result = SlotGenerator.update_custom_slot(
            slot_id=slot_id,
            new_date=new_date,
            new_start_time=new_start_time,
            new_end_time=new_end_time
        )
        
        if result['success'] and updated_by:
            logger.info(f"Custom slot updated by {updated_by}: {result['slot']}")
        
        return result
    
    @staticmethod
    def delete_custom_slot(slot_id, force=False, deleted_by=None):
        """
        Delete a custom slot
        
        Args:
            slot_id: Slot ID to delete
            force: Whether to force deletion even with bookings
            deleted_by: User who deleted the slot (optional)
            
        Returns:
            dict: Deletion result
        """
        result = SlotGenerator.delete_custom_slot(slot_id, force=force)
        
        if result['success'] and deleted_by:
            logger.info(f"Custom slot deleted by {deleted_by}: {slot_id}")
        
        return result
    
    @staticmethod
    def bulk_create_custom_slots(game_id, slot_definitions, created_by=None):
        """
        Create multiple custom slots at once
        
        Args:
            game_id: Game ID
            slot_definitions: List of slot definitions
            created_by: User who created the slots (optional)
            
        Returns:
            dict: Bulk creation result
        """
        try:
            game = Game.objects.get(id=game_id, is_active=True)
        except Game.DoesNotExist:
            return {
                'success': False,
                'errors': ['Game not found or inactive']
            }
        
        result = SlotGenerator.bulk_create_custom_slots(game, slot_definitions)
        
        if result['success'] and created_by:
            logger.info(f"Bulk custom slots created by {created_by}: {result['created_count']} slots for {game.name}")
        
        return result
    
    @staticmethod
    def get_slot_conflicts(game_id, target_date, start_time, end_time, exclude_slot_id=None):
        """
        Check for conflicts when creating/updating a custom slot
        
        Args:
            game_id: Game ID
            target_date: Date for the slot
            start_time: Start time
            end_time: End time
            exclude_slot_id: Slot ID to exclude from conflict check (for updates)
            
        Returns:
            dict: Conflict check result
        """
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return {
                'success': False,
                'errors': ['Game not found']
            }
        
        conflict_result = SlotGenerator._check_slot_conflicts(
            game, target_date, start_time, end_time, exclude_slot_id
        )
        
        return {
            'success': True,
            'has_conflicts': not conflict_result['valid'],
            'conflicts': conflict_result.get('conflicting_slots', []),
            'errors': conflict_result.get('errors', [])
        }
    
    @staticmethod
    def get_available_time_ranges(game_id, target_date, min_duration_minutes=60):
        """
        Get available time ranges for creating custom slots
        
        Args:
            game_id: Game ID
            target_date: Date to check
            min_duration_minutes: Minimum duration for available ranges
            
        Returns:
            dict: Available time ranges
        """
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return {
                'success': False,
                'errors': ['Game not found']
            }
        
        # Get all existing slots for the date
        existing_slots = GameSlot.objects.filter(
            game=game,
            date=target_date,
            is_active=True
        ).order_by('start_time')
        
        available_ranges = []
        
        # Start from midnight
        current_time = time(0, 0)
        
        for slot in existing_slots:
            # If there's a gap before this slot
            if current_time < slot.start_time:
                gap_duration = (
                    datetime.combine(target_date, slot.start_time) - 
                    datetime.combine(target_date, current_time)
                ).total_seconds() / 60
                
                if gap_duration >= min_duration_minutes:
                    available_ranges.append({
                        'start_time': current_time.strftime('%H:%M'),
                        'end_time': slot.start_time.strftime('%H:%M'),
                        'duration_minutes': int(gap_duration)
                    })
            
            # Move current time to after this slot
            current_time = slot.end_time
        
        # Check for gap after the last slot until midnight
        end_of_day = time(23, 59)
        if current_time < end_of_day:
            gap_duration = (
                datetime.combine(target_date, end_of_day) - 
                datetime.combine(target_date, current_time)
            ).total_seconds() / 60
            
            if gap_duration >= min_duration_minutes:
                available_ranges.append({
                    'start_time': current_time.strftime('%H:%M'),
                    'end_time': end_of_day.strftime('%H:%M'),
                    'duration_minutes': int(gap_duration)
                })
        
        return {
            'success': True,
            'available_ranges': available_ranges,
            'date': target_date.isoformat(),
            'game_name': game.name
        }
    
    @staticmethod
    def validate_custom_slot_data(game_id, target_date, start_time, end_time):
        """
        Validate custom slot data before creation/update
        
        Args:
            game_id: Game ID
            target_date: Date for the slot
            start_time: Start time
            end_time: End time
            
        Returns:
            dict: Validation result
        """
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return {
                'valid': False,
                'errors': ['Game not found']
            }
        
        # Use the slot generator's validation
        validation_result = SlotGenerator._validate_custom_slot_params(
            game, target_date, start_time, end_time
        )
        
        # Add additional business logic validation
        additional_errors = []
        
        # Check if the slot is too far in the future (e.g., more than 6 months)
        max_future_date = date.today() + timedelta(days=180)
        if target_date > max_future_date:
            additional_errors.append("Cannot create slots more than 6 months in advance")
        
        # Check if it's a reasonable time (not too early or too late)
        if start_time < time(6, 0):
            additional_errors.append("Slots cannot start before 6:00 AM")
        
        if end_time > time(23, 59):
            additional_errors.append("Slots cannot end after 11:59 PM")
        
        all_errors = validation_result['errors'] + additional_errors
        
        return {
            'valid': len(all_errors) == 0,
            'errors': all_errors
        }
    
    @staticmethod
    def get_custom_slot_statistics(game_id=None, start_date=None, end_date=None):
        """
        Get statistics about custom slots
        
        Args:
            game_id: Game ID filter (optional)
            start_date: Start date filter (optional)
            end_date: End date filter (optional)
            
        Returns:
            dict: Statistics about custom slots
        """
        slots_query = GameSlot.objects.filter(is_custom=True, is_active=True)
        
        if game_id:
            slots_query = slots_query.filter(game_id=game_id)
        
        if start_date:
            slots_query = slots_query.filter(date__gte=start_date)
        
        if end_date:
            slots_query = slots_query.filter(date__lte=end_date)
        
        total_slots = slots_query.count()
        
        # Count slots with bookings
        slots_with_bookings = slots_query.filter(
            bookings__status__in=['CONFIRMED', 'IN_PROGRESS', 'COMPLETED']
        ).distinct().count()
        
        # Count upcoming slots
        upcoming_slots = slots_query.filter(date__gte=date.today()).count()
        
        # Count past slots
        past_slots = slots_query.filter(date__lt=date.today()).count()
        
        return {
            'total_custom_slots': total_slots,
            'slots_with_bookings': slots_with_bookings,
            'upcoming_slots': upcoming_slots,
            'past_slots': past_slots,
            'utilization_rate': (slots_with_bookings / total_slots * 100) if total_slots > 0 else 0
        }