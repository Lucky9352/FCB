from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from decimal import Decimal

from authentication.models import Customer
from .models import GamingStation, Booking, BookingHistory
from .utils import TimeSlotManager, BookingValidator, BookingManager


class GamingStationModelTest(TestCase):
    def setUp(self):
        self.station = GamingStation.objects.create(
            name="PC-001",
            station_type="PC",
            description="High-end gaming PC",
            hourly_rate=Decimal('15.00'),
            specifications={
                "cpu": "Intel i7-12700K",
                "gpu": "RTX 3080",
                "ram": "32GB DDR4"
            }
        )
    
    def test_station_creation(self):
        self.assertEqual(self.station.name, "PC-001")
        self.assertEqual(self.station.station_type, "PC")
        self.assertEqual(self.station.hourly_rate, Decimal('15.00'))
        self.assertTrue(self.station.is_available)
    
    def test_station_availability(self):
        # Test active station
        self.assertTrue(self.station.is_available)
        
        # Test inactive station
        self.station.is_active = False
        self.station.save()
        self.assertFalse(self.station.is_available)
        
        # Test maintenance station
        self.station.is_active = True
        self.station.is_maintenance = True
        self.station.save()
        self.assertFalse(self.station.is_available)


class BookingModelTest(TestCase):
    def setUp(self):
        # Create test user and customer
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            phone='+1234567890'
        )
        
        # Create test gaming station
        self.station = GamingStation.objects.create(
            name="PC-001",
            station_type="PC",
            hourly_rate=Decimal('15.00')
        )
        
        # Create test booking times
        self.start_time = timezone.now() + timedelta(hours=1)
        self.end_time = self.start_time + timedelta(hours=2)
    
    def test_booking_creation(self):
        booking = Booking.objects.create(
            customer=self.customer,
            gaming_station=self.station,
            start_time=self.start_time,
            end_time=self.end_time,
            hourly_rate=self.station.hourly_rate
        )
        
        self.assertEqual(booking.customer, self.customer)
        self.assertEqual(booking.gaming_station, self.station)
        self.assertEqual(booking.status, 'PENDING')
        self.assertEqual(booking.duration_hours, 2.0)
        self.assertEqual(booking.total_amount, Decimal('30.00'))
    
    def test_booking_validation(self):
        # Test end time before start time
        with self.assertRaises(ValidationError):
            booking = Booking(
                customer=self.customer,
                gaming_station=self.station,
                start_time=self.end_time,
                end_time=self.start_time,
                hourly_rate=self.station.hourly_rate
            )
            booking.full_clean()
        
        # Test booking in the past
        past_time = timezone.now() - timedelta(hours=1)
        with self.assertRaises(ValidationError):
            booking = Booking(
                customer=self.customer,
                gaming_station=self.station,
                start_time=past_time,
                end_time=past_time + timedelta(hours=1),
                hourly_rate=self.station.hourly_rate
            )
            booking.full_clean()


class TimeSlotManagerTest(TestCase):
    def setUp(self):
        self.station = GamingStation.objects.create(
            name="PC-001",
            station_type="PC",
            hourly_rate=Decimal('15.00')
        )
        self.time_manager = TimeSlotManager(self.station)
    
    def test_get_available_slots(self):
        tomorrow = (timezone.now() + timedelta(days=1)).date()
        slots = self.time_manager.get_available_slots(tomorrow)
        
        # Should have slots from 9 AM to 11 PM (14 hours)
        self.assertEqual(len(slots), 14)
        
        # First slot should start at 9 AM
        first_slot = slots[0]
        self.assertEqual(first_slot['start_time'].hour, 9)
        self.assertEqual(first_slot['duration_hours'], 1)
        self.assertEqual(first_slot['price'], 15.0)
    
    def test_unavailable_station_slots(self):
        # Make station unavailable
        self.station.is_active = False
        self.station.save()
        
        tomorrow = (timezone.now() + timedelta(days=1)).date()
        slots = self.time_manager.get_available_slots(tomorrow)
        
        # Should have no available slots
        self.assertEqual(len(slots), 0)


class BookingValidatorTest(TestCase):
    def setUp(self):
        self.start_time = timezone.now() + timedelta(hours=1)
        self.end_time = self.start_time + timedelta(hours=2)
    
    def test_validate_booking_time(self):
        # Valid booking time should not raise exception
        BookingValidator.validate_booking_time(self.start_time, self.end_time)
        
        # Invalid: end before start
        with self.assertRaises(ValidationError):
            BookingValidator.validate_booking_time(self.end_time, self.start_time)
        
        # Invalid: booking in the past
        past_time = timezone.now() - timedelta(hours=1)
        with self.assertRaises(ValidationError):
            BookingValidator.validate_booking_time(past_time, past_time + timedelta(hours=1))
        
        # Invalid: too short duration
        short_end = self.start_time + timedelta(minutes=10)
        with self.assertRaises(ValidationError):
            BookingValidator.validate_booking_time(self.start_time, short_end)
        
        # Invalid: too long duration
        long_end = self.start_time + timedelta(hours=10)
        with self.assertRaises(ValidationError):
            BookingValidator.validate_booking_time(self.start_time, long_end)


class BookingManagerTest(TestCase):
    def setUp(self):
        # Create test user and customer
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            phone='+1234567890'
        )
        
        # Create test gaming station
        self.station = GamingStation.objects.create(
            name="PC-001",
            station_type="PC",
            hourly_rate=Decimal('15.00')
        )
        
        self.start_time = timezone.now() + timedelta(hours=1)
        self.end_time = self.start_time + timedelta(hours=2)
    
    def test_create_booking(self):
        booking = BookingManager.create_booking(
            customer=self.customer,
            station=self.station,
            start_time=self.start_time,
            end_time=self.end_time,
            notes="Test booking"
        )
        
        self.assertEqual(booking.customer, self.customer)
        self.assertEqual(booking.gaming_station, self.station)
        self.assertEqual(booking.status, 'PENDING')
        self.assertEqual(booking.notes, "Test booking")
        self.assertEqual(booking.total_amount, Decimal('30.00'))
    
    def test_create_walk_in_booking(self):
        booking = BookingManager.create_booking(
            customer=self.customer,
            station=self.station,
            start_time=self.start_time,
            end_time=self.end_time,
            is_walk_in=True
        )
        
        self.assertTrue(booking.is_walk_in)
        self.assertEqual(booking.status, 'CONFIRMED')  # Walk-ins are auto-confirmed
