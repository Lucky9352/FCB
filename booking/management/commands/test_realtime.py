from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from booking.supabase_client import supabase_realtime
from booking.realtime_service import realtime_service
from booking.models import GamingStation, Booking
from authentication.models import Customer
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Test real-time functionality and Supabase integration'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--test-type',
            type=str,
            choices=['connection', 'booking', 'availability', 'conflict'],
            default='connection',
            help='Type of test to run'
        )
        
        parser.add_argument(
            '--duration',
            type=int,
            default=30,
            help='Test duration in seconds'
        )
    
    def handle(self, *args, **options):
        test_type = options['test_type']
        duration = options['duration']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting {test_type} test for {duration} seconds...')
        )
        
        if test_type == 'connection':
            self.test_connection()
        elif test_type == 'booking':
            self.test_booking_updates()
        elif test_type == 'availability':
            self.test_availability_updates()
        elif test_type == 'conflict':
            self.test_conflict_resolution()
    
    def test_connection(self):
        """Test Supabase connection"""
        if supabase_realtime.is_connected():
            self.stdout.write(
                self.style.SUCCESS('✅ Supabase client connected successfully')
            )
            
            # Test subscription
            def test_callback(payload):
                self.stdout.write(f'📡 Received real-time update: {payload}')
            
            subscription_id = supabase_realtime.subscribe_to_booking_changes(test_callback)
            
            if subscription_id:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Subscription created: {subscription_id}')
                )
                
                # Clean up
                supabase_realtime.unsubscribe(subscription_id)
                self.stdout.write('🧹 Subscription cleaned up')
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Failed to create subscription')
                )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Supabase client not connected')
            )
    
    def test_booking_updates(self):
        """Test booking update broadcasting"""
        # Get or create test data
        station = self.get_or_create_test_station()
        customer = self.get_or_create_test_customer()
        
        # Create a test booking
        start_time = timezone.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        self.stdout.write('📝 Creating test booking...')
        
        booking = Booking.objects.create(
            customer=customer,
            gaming_station=station,
            start_time=start_time,
            end_time=end_time,
            hourly_rate=station.hourly_rate
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Created booking: {booking.id}')
        )
        
        # Update booking status
        self.stdout.write('🔄 Updating booking status...')
        booking.status = 'CONFIRMED'
        booking.save()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Booking status updated - check real-time updates')
        )
        
        # Clean up
        booking.delete()
        self.stdout.write('🧹 Test booking cleaned up')
    
    def test_availability_updates(self):
        """Test availability update broadcasting"""
        station = self.get_or_create_test_station()
        
        self.stdout.write('🔄 Updating station availability...')
        
        # Toggle maintenance mode
        original_maintenance = station.is_maintenance
        station.is_maintenance = not original_maintenance
        station.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Station maintenance toggled to: {station.is_maintenance}')
        )
        
        # Get real-time availability
        availability = realtime_service.get_real_time_availability()
        station_data = availability['stations'].get(str(station.id))
        
        if station_data:
            self.stdout.write(
                f'📊 Available slots: {len(station_data["available_slots"])}'
            )
        
        # Restore original state
        station.is_maintenance = original_maintenance
        station.save()
        
        self.stdout.write('🧹 Station state restored')
    
    def test_conflict_resolution(self):
        """Test booking conflict resolution"""
        station = self.get_or_create_test_station()
        customer1 = self.get_or_create_test_customer()
        customer2 = self.get_or_create_test_customer('testuser2')
        
        # Use a time further in the future to avoid validation issues
        start_time = timezone.now() + timedelta(hours=2)
        end_time = start_time + timedelta(hours=2)
        
        # Simulate simultaneous booking requests
        booking_request1 = {
            'station_id': str(station.id),
            'customer_id': str(customer1.id),
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'timestamp': timezone.now().timestamp()
        }
        
        booking_request2 = {
            'station_id': str(station.id),
            'customer_id': str(customer2.id),
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'timestamp': timezone.now().timestamp() + 0.1  # Slightly later
        }
        
        self.stdout.write('⚡ Testing conflict resolution...')
        
        # Process first request
        result1 = realtime_service.handle_booking_attempt(booking_request1)
        self.stdout.write(f'📝 Request 1 result: {result1["success"]}')
        
        # Process second request (should conflict)
        result2 = realtime_service.handle_booking_attempt(booking_request2)
        self.stdout.write(f'📝 Request 2 result: {result2["success"]}')
        
        if result1['success'] and not result2['success']:
            self.stdout.write(
                self.style.SUCCESS('✅ Conflict resolution working correctly')
            )
            
            # Clean up successful booking
            if 'booking_id' in result1:
                try:
                    booking = Booking.objects.get(id=result1['booking_id'])
                    booking.delete()
                    self.stdout.write('🧹 Test booking cleaned up')
                except Booking.DoesNotExist:
                    pass
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Unexpected conflict resolution result')
            )
    
    def get_or_create_test_station(self):
        """Get or create a test gaming station"""
        station, created = GamingStation.objects.get_or_create(
            name='TEST-PC-001',
            defaults={
                'station_type': 'PC',
                'hourly_rate': 15.00,
                'description': 'Test gaming station for real-time testing'
            }
        )
        
        if created:
            self.stdout.write('🎮 Created test gaming station')
        
        return station
    
    def get_or_create_test_customer(self, username='testuser'):
        """Get or create a test customer"""
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        customer, created = Customer.objects.get_or_create(
            user=user,
            defaults={
                'phone': '+1234567890'
            }
        )
        
        if created:
            self.stdout.write(f'👤 Created test customer: {username}')
        
        return customer