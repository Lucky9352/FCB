from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import GamingStation, Booking
from typing import List, Tuple, Dict, Optional


class TimeSlotManager:
    """Utility class for managing time slots and availability"""
    
    def __init__(self, station: GamingStation):
        self.station = station
    
    def get_available_slots(self, date: datetime.date, slot_duration: int = 1) -> List[Dict]:
        """
        Get available time slots for a specific date
        
        Args:
            date: The date to check availability for
            slot_duration: Duration of each slot in hours (default: 1 hour)
        
        Returns:
            List of available time slots with start and end times
        """
        if not self.station.is_available:
            return []
        
        # Define operating hours (can be made configurable later)
        start_hour = 9  # 9 AM
        end_hour = 23   # 11 PM
        
        # Generate all possible slots for the day
        start_datetime = timezone.make_aware(
            datetime.combine(date, datetime.min.time().replace(hour=start_hour))
        )
        end_datetime = timezone.make_aware(
            datetime.combine(date, datetime.min.time().replace(hour=end_hour))
        )
        
        available_slots = []
        current_time = start_datetime
        
        while current_time + timedelta(hours=slot_duration) <= end_datetime:
            slot_end = current_time + timedelta(hours=slot_duration)
            
            # Check if this slot is available
            if self.station.is_available_at_time(current_time, slot_end):
                available_slots.append({
                    'start_time': current_time,
                    'end_time': slot_end,
                    'duration_hours': slot_duration,
                    'price': float(self.station.hourly_rate * slot_duration)
                })
            
            current_time += timedelta(hours=slot_duration)
        
        return available_slots
    
    def get_booking_conflicts(self, start_time: datetime, end_time: datetime, 
                            exclude_booking_id: Optional[str] = None) -> List[Booking]:
        """
        Get bookings that conflict with the given time range
        
        Args:
            start_time: Start time of the proposed booking
            end_time: End time of the proposed booking
            exclude_booking_id: Booking ID to exclude from conflict check (for updates)
        
        Returns:
            List of conflicting bookings
        """
        conflicts = self.station.bookings.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            status__in=['CONFIRMED', 'IN_PROGRESS', 'PENDING']
        )
        
        if exclude_booking_id:
            conflicts = conflicts.exclude(id=exclude_booking_id)
        
        return list(conflicts)
    
    def find_next_available_slot(self, preferred_start: datetime, 
                               duration_hours: int = 1) -> Optional[Dict]:
        """
        Find the next available slot after the preferred start time
        
        Args:
            preferred_start: Preferred start time
            duration_hours: Duration of the booking in hours
        
        Returns:
            Next available slot or None if no slot available
        """
        if not self.station.is_available:
            return None
        
        # Start checking from the preferred time
        current_time = preferred_start
        max_search_time = preferred_start + timedelta(days=7)  # Search up to 7 days ahead
        
        while current_time < max_search_time:
            slot_end = current_time + timedelta(hours=duration_hours)
            
            if self.station.is_available_at_time(current_time, slot_end):
                return {
                    'start_time': current_time,
                    'end_time': slot_end,
                    'duration_hours': duration_hours,
                    'price': float(self.station.hourly_rate * duration_hours)
                }
            
            # Move to next hour
            current_time += timedelta(hours=1)
        
        return None


class BookingValidator:
    """Utility class for validating booking requests"""
    
    @staticmethod
    def validate_booking_time(start_time: datetime, end_time: datetime) -> None:
        """
        Validate booking time constraints
        
        Args:
            start_time: Booking start time
            end_time: Booking end time
        
        Raises:
            ValidationError: If validation fails
        """
        now = timezone.now()
        
        # Check if end time is after start time
        if end_time <= start_time:
            raise ValidationError("End time must be after start time")
        
        # Check if booking is in the future
        if start_time <= now:
            raise ValidationError("Booking start time must be in the future")
        
        # Check minimum booking duration (15 minutes)
        min_duration = timedelta(minutes=15)
        if end_time - start_time < min_duration:
            raise ValidationError("Minimum booking duration is 15 minutes")
        
        # Check maximum booking duration (8 hours)
        max_duration = timedelta(hours=8)
        if end_time - start_time > max_duration:
            raise ValidationError("Maximum booking duration is 8 hours")
        
        # Check if booking is too far in the future (30 days)
        max_advance_booking = now + timedelta(days=30)
        if start_time > max_advance_booking:
            raise ValidationError("Bookings can only be made up to 30 days in advance")
    
    @staticmethod
    def validate_station_availability(station: GamingStation, start_time: datetime, 
                                    end_time: datetime, exclude_booking_id: Optional[str] = None) -> None:
        """
        Validate that a station is available for the given time period
        
        Args:
            station: Gaming station to check
            start_time: Booking start time
            end_time: Booking end time
            exclude_booking_id: Booking ID to exclude from conflict check
        
        Raises:
            ValidationError: If station is not available
        """
        if not station.is_available:
            if station.is_maintenance:
                raise ValidationError("Station is currently under maintenance")
            else:
                raise ValidationError("Station is not available for booking")
        
        # Check for conflicts
        time_manager = TimeSlotManager(station)
        conflicts = time_manager.get_booking_conflicts(start_time, end_time, exclude_booking_id)
        
        if conflicts:
            conflict_times = [
                f"{conflict.start_time.strftime('%H:%M')} - {conflict.end_time.strftime('%H:%M')}"
                for conflict in conflicts
            ]
            raise ValidationError(
                f"Time slot conflicts with existing bookings: {', '.join(conflict_times)}"
            )
    
    @staticmethod
    def validate_customer_booking_limit(customer, start_time: datetime) -> None:
        """
        Validate customer booking limits
        
        Args:
            customer: Customer making the booking
            start_time: Booking start time
        
        Raises:
            ValidationError: If customer exceeds booking limits
        """
        # Check for maximum concurrent bookings (3 active bookings)
        active_bookings = customer.bookings.filter(
            status__in=['CONFIRMED', 'IN_PROGRESS', 'PENDING']
        ).count()
        
        if active_bookings >= 3:
            raise ValidationError("Maximum of 3 active bookings allowed per customer")
        
        # Check for duplicate bookings on the same day
        booking_date = start_time.date()
        same_day_bookings = customer.bookings.filter(
            start_time__date=booking_date,
            status__in=['CONFIRMED', 'IN_PROGRESS', 'PENDING']
        ).count()
        
        if same_day_bookings >= 2:
            raise ValidationError("Maximum of 2 bookings per day allowed")


class BookingManager:
    """High-level booking management utility"""
    
    @staticmethod
    def create_booking(customer, station: GamingStation, start_time: datetime, 
                      end_time: datetime, is_walk_in: bool = False, 
                      notes: str = "") -> Booking:
        """
        Create a new booking with full validation
        
        Args:
            customer: Customer making the booking
            station: Gaming station to book
            start_time: Booking start time
            end_time: Booking end time
            is_walk_in: Whether this is a walk-in booking
            notes: Additional notes
        
        Returns:
            Created booking instance
        
        Raises:
            ValidationError: If validation fails
        """
        # Validate booking parameters
        BookingValidator.validate_booking_time(start_time, end_time)
        BookingValidator.validate_station_availability(station, start_time, end_time)
        BookingValidator.validate_customer_booking_limit(customer, start_time)
        
        # Create the booking
        booking = Booking(
            customer=customer,
            gaming_station=station,
            start_time=start_time,
            end_time=end_time,
            hourly_rate=station.hourly_rate,
            is_walk_in=is_walk_in,
            notes=notes
        )
        
        # Calculate total amount
        booking.total_amount = booking.calculate_total_amount()
        
        # Set initial status
        booking.status = 'CONFIRMED' if is_walk_in else 'PENDING'
        
        # Save the booking
        booking.full_clean()  # Run model validation
        booking.save()
        
        return booking
    
    @staticmethod
    def get_station_availability_summary(date: datetime.date) -> Dict[str, Dict]:
        """
        Get availability summary for all stations on a given date
        
        Args:
            date: Date to check availability for
        
        Returns:
            Dictionary with station availability information
        """
        stations = GamingStation.objects.filter(is_active=True)
        availability_summary = {}
        
        for station in stations:
            time_manager = TimeSlotManager(station)
            available_slots = time_manager.get_available_slots(date)
            
            availability_summary[str(station.id)] = {
                'station': {
                    'id': str(station.id),
                    'name': station.name,
                    'type': station.station_type,
                    'hourly_rate': float(station.hourly_rate),
                    'is_available': station.is_available
                },
                'available_slots': len(available_slots),
                'slots': available_slots
            }
        
        return availability_summary