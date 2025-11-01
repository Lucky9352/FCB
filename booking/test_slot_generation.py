"""
Tests for enhanced slot generation functionality
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, time, timedelta
from decimal import Decimal

from .models import Game, GameSlot, SlotAvailability
from .slot_generator import SlotGenerator
from .custom_slot_service import CustomSlotService


class SlotGeneratorTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create(
            name="Test Pool Table",
            description="Test pool table for slot generation",
            capacity=4,
            booking_type='HYBRID',
            opening_time=time(10, 0),  # 10 AM
            closing_time=time(22, 0),  # 10 PM
            slot_duration_minutes=60,
            available_days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
            private_price=Decimal('400.00'),
            shared_price=Decimal('100.00'),
            is_active=True
        )
    
    def test_generate_slots_for_game(self):
        """Test basic slot generation"""
        # Use a specific Monday to ensure consistent test results
        start_date = date.today() + timedelta(days=1)
        # Find next Monday
        while start_date.strftime('%A').lower() != 'monday':
            start_date += timedelta(days=1)
        end_date = start_date + timedelta(days=2)  # Monday to Wednesday
        
        result = SlotGenerator.generate_slots_for_game(self.game, start_date, end_date)
        
        self.assertTrue(result['created'] > 0)
        self.assertEqual(len(result['errors']), 0)
        
        # Check that slots were actually created
        slots = GameSlot.objects.filter(game=self.game, is_custom=False)
        self.assertTrue(slots.exists())
        
        # Check that availability was created
        for slot in slots:
            self.assertTrue(hasattr(slot, 'availability'))
    
    def test_validate_slot_generation_settings(self):
        """Test game settings validation"""
        # Valid game should pass
        result = SlotGenerator.validate_slot_generation_settings(self.game)
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['errors']), 0)
        
        # Invalid game should fail
        invalid_game = Game.objects.create(
            name="Invalid Game",
            capacity=0,  # Invalid capacity
            opening_time=time(22, 0),  # Opening after closing
            closing_time=time(10, 0),
            slot_duration_minutes=0,  # Invalid duration
            private_price=Decimal('0.00'),  # Invalid price
            is_active=False
        )
        
        result = SlotGenerator.validate_slot_generation_settings(invalid_game)
        self.assertFalse(result['valid'])
        self.assertTrue(len(result['errors']) > 0)


class CustomSlotServiceTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create(
            name="Test Game",
            capacity=2,
            booking_type='SINGLE',
            opening_time=time(9, 0),
            closing_time=time(21, 0),
            slot_duration_minutes=120,
            available_days=['saturday', 'sunday'],
            private_price=Decimal('200.00'),
            is_active=True
        )
    
    def test_create_custom_slot(self):
        """Test custom slot creation"""
        target_date = date.today() + timedelta(days=7)
        start_time = time(23, 0)  # 11 PM
        end_time = time(23, 59)   # 11:59 PM
        
        result = CustomSlotService.create_custom_slot(
            game_id=str(self.game.id),
            target_date=target_date,
            start_time=start_time,
            end_time=end_time
        )
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result.get('slot'))
        
        # Verify slot was created
        slot = GameSlot.objects.get(id=result['slot'].id)
        self.assertTrue(slot.is_custom)
        self.assertEqual(slot.date, target_date)
        self.assertEqual(slot.start_time, start_time)
        self.assertEqual(slot.end_time, end_time)
    
    def test_get_available_time_ranges(self):
        """Test available time range calculation"""
        target_date = date.today() + timedelta(days=1)
        
        # Create some existing slots
        GameSlot.objects.create(
            game=self.game,
            date=target_date,
            start_time=time(10, 0),
            end_time=time(12, 0),
            is_custom=False
        )
        
        result = CustomSlotService.get_available_time_ranges(
            game_id=str(self.game.id),
            target_date=target_date,
            min_duration_minutes=60
        )
        
        self.assertTrue(result['success'])
        self.assertTrue(len(result['available_ranges']) > 0)