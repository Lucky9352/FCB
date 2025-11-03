"""
API Serializers for Booking System
Provides efficient JSON serialization for REST API endpoints
"""
from rest_framework import serializers
from .models import Game, GameSlot, SlotAvailability, Booking
from django.utils import timezone


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Game model - basic info for fast loading"""
    
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = [
            'id', 'name', 'description', 'capacity', 
            'slot_duration_minutes', 'booking_type',
            'private_price', 'shared_price', 'shared_price_per_person',
            'image_url', 'is_active'
        ]
    
    def get_image_url(self, obj):
        """Get absolute URL for game image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class SlotAvailabilitySerializer(serializers.ModelSerializer):
    """Serializer for slot availability information"""
    
    available_spots = serializers.IntegerField(read_only=True)
    can_book_private = serializers.BooleanField(read_only=True)
    can_book_shared = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = SlotAvailability
        fields = [
            'total_capacity', 'booked_spots', 'is_private_booked',
            'available_spots', 'can_book_private', 'can_book_shared'
        ]


class BookingOptionSerializer(serializers.Serializer):
    """Serializer for booking options (private/shared)"""
    
    type = serializers.CharField()
    price = serializers.FloatField()
    capacity = serializers.IntegerField(required=False)
    spots_included = serializers.IntegerField(required=False)
    description = serializers.CharField()
    available = serializers.BooleanField()
    icon = serializers.CharField()
    benefits = serializers.ListField(child=serializers.CharField())
    restriction_reason = serializers.CharField(required=False)
    disabled_message = serializers.CharField(required=False)
    available_spots = serializers.IntegerField(required=False)
    max_spots_per_booking = serializers.IntegerField(required=False)
    price_per_spot = serializers.FloatField(required=False)


class GameSlotSerializer(serializers.ModelSerializer):
    """Serializer for GameSlot with availability and booking options"""
    
    availability = SlotAvailabilitySerializer(read_only=True)
    booking_options = serializers.SerializerMethodField()
    is_past = serializers.SerializerMethodField()
    time_display = serializers.SerializerMethodField()
    
    class Meta:
        model = GameSlot
        fields = [
            'id', 'date', 'start_time', 'end_time', 
            'is_active', 'availability', 'booking_options',
            'is_past', 'time_display'
        ]
    
    def get_booking_options(self, obj):
        """Get booking options for this slot"""
        from .booking_service import BookingService
        
        try:
            options = BookingService.get_booking_options(obj)
            return BookingOptionSerializer(options, many=True).data
        except Exception as e:
            return []
    
    def get_is_past(self, obj):
        """Check if slot is in the past"""
        now = timezone.now()
        slot_datetime = timezone.make_aware(
            timezone.datetime.combine(obj.date, obj.start_time)
        )
        return slot_datetime < now
    
    def get_time_display(self, obj):
        """Format time range for display"""
        return f"{obj.start_time.strftime('%I:%M %p')} - {obj.end_time.strftime('%I:%M %p')}"


class SlotsByDateSerializer(serializers.Serializer):
    """Serializer for slots grouped by date"""
    
    date = serializers.DateField()
    slots = GameSlotSerializer(many=True)
    total_slots = serializers.IntegerField()
    available_slots = serializers.IntegerField()
