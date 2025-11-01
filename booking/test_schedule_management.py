"""
Tests for enhanced schedule management functionality
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, time, timedelta
from decimal import Decimal

from authentication.models import Customer, CafeOwner
from .models import Game, GameSlot, Booking, SlotAvailability


class ScheduleManagementTest(TestCase):
    """Test schedule management views and functionality"""
    
    def setUp(self):
        # Create test users
        self.owner_user = User.objects.create_user(
            username='cafeowner',
            email='owner@test.com',
            password='testpass123'
        )
        
        self.customer_user = User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='testpass123'
        )
        
        # Create cafe owner profile
        self.cafe_owner = CafeOwner.objects.create(
            user=self.owner_user,
            cafe_name="Test Gaming Cafe",
            contact_email="owner@test.com",
            phone="1234567890"
        )
        
        # Create customer profile
        self.customer = Customer.objects.create(
            user=self.customer_user,
            google_id="test_google_id",
            phone="0987654321"
        )
        
        # Create test game
        self.game = Game.objects.create(
            name="Test Pool Table",
            description="Test pool table for schedule management",
            capacity=4,
            booking_type='HYBRID',
            opening_time=time(11, 0),
            closing_time=time(23, 0),
            slot_duration_minutes=60,
            available_days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
            private_price=Decimal('400.00'),
            shared_price=Decimal('100.00')
        )
        
        # Create some test slots (without bookings for now)
        self.create_test_slots()
        
        self.client = Client()
    
    def create_test_slots(self):
        """Create test slots for testing (without bookings to avoid save issues)"""
        # Create slots for the next 7 days
        start_date = date.today()
        for i in range(7):
            current_date = start_date + timedelta(days=i)
            
            # Create a few slots per day
            for hour in [14, 16, 18, 20]:  # 2 PM, 4 PM, 6 PM, 8 PM
                slot = GameSlot.objects.create(
                    game=self.game,
                    date=current_date,
                    start_time=time(hour, 0),
                    end_time=time(hour + 1, 0),
                    is_custom=False,
                    is_active=True
                )
                
                # Create availability tracking
                SlotAvailability.objects.create(
                    game_slot=slot,
                    total_capacity=self.game.capacity,
                    booked_spots=0,
                    is_private_booked=False
                )
    
    def test_advanced_schedule_management_view(self):
        """Test advanced schedule management view access and rendering"""
        # Login as cafe owner
        self.client.login(username='cafeowner', password='testpass123')
        
        # Access advanced schedule management
        url = reverse('booking:game_management:advanced_schedule_management', 
                     kwargs={'game_id': self.game.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Advanced Schedule Management')
        self.assertContains(response, self.game.name)
        self.assertContains(response, 'Schedule Optimization Suggestions')
    
    def test_schedule_optimization_suggestions_api(self):
        """Test schedule optimization suggestions API endpoint"""
        # Login as cafe owner
        self.client.login(username='cafeowner', password='testpass123')
        
        # Call optimization suggestions API
        url = reverse('booking:game_management:schedule_optimization_suggestions', 
                     kwargs={'game_id': self.game.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON response
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('suggestions', data)
        self.assertIn('analytics', data)
        
        # Check analytics data structure
        analytics = data['analytics']
        self.assertIn('total_bookings', analytics)
        self.assertIn('total_revenue', analytics)
        self.assertIn('utilization_rate', analytics)
        self.assertIn('analysis_period', analytics)
    
    def test_schedule_optimization_unauthorized_access(self):
        """Test that customers cannot access schedule management"""
        # Login as customer
        self.client.login(username='customer', password='testpass123')
        
        # Try to access advanced schedule management
        url = reverse('booking:game_management:advanced_schedule_management', 
                     kwargs={'game_id': self.game.id})
        response = self.client.get(url)
        
        # Should redirect to login or show permission denied
        self.assertNotEqual(response.status_code, 200)
    
    def test_schedule_optimization_with_no_data(self):
        """Test optimization suggestions when there's no booking data"""
        # Create a new game with no bookings
        new_game = Game.objects.create(
            name="New Game",
            description="New game with no bookings",
            capacity=2,
            booking_type='SINGLE',
            opening_time=time(10, 0),
            closing_time=time(22, 0),
            slot_duration_minutes=90,
            available_days=['monday', 'wednesday', 'friday'],
            private_price=Decimal('200.00')
        )
        
        # Login as cafe owner
        self.client.login(username='cafeowner', password='testpass123')
        
        # Call optimization suggestions API
        url = reverse('booking:game_management:schedule_optimization_suggestions', 
                     kwargs={'game_id': new_game.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        
        # Should have empty or minimal suggestions for new game
        analytics = data['analytics']
        self.assertEqual(analytics['total_bookings'], 0)
        self.assertEqual(analytics['total_revenue'], 0.0)
    
    def test_schedule_preview_enhanced_functionality(self):
        """Test enhanced schedule preview functionality"""
        # Login as cafe owner
        self.client.login(username='cafeowner', password='testpass123')
        
        # Test schedule preview with game_id for revenue analysis
        url = reverse('booking:game_management:schedule_preview')
        params = {
            'opening_time': '10:00',
            'closing_time': '22:00',
            'slot_duration_minutes': '60',
            'available_days[]': ['monday', 'tuesday', 'wednesday'],
            'game_id': str(self.game.id)
        }
        
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('preview_slots', data)
        self.assertIn('statistics', data)
        self.assertIn('revenue_analysis', data)
        self.assertIn('booking_impact', data)
        
        # Check revenue analysis for hybrid game
        if data['revenue_analysis']:
            revenue_analysis = data['revenue_analysis']
            self.assertIn('private_only', revenue_analysis)
            if self.game.booking_type == 'HYBRID':
                self.assertIn('shared_only', revenue_analysis)
                self.assertIn('mixed_50_50', revenue_analysis)


class ScheduleOptimizationLogicTest(TestCase):
    """Test the schedule optimization logic"""
    
    def setUp(self):
        # Create test user and game
        self.owner_user = User.objects.create_user(
            username='owner',
            password='testpass123'
        )
        
        self.cafe_owner = CafeOwner.objects.create(
            user=self.owner_user,
            cafe_name="Test Cafe"
        )
        
        self.customer_user = User.objects.create_user(
            username='customer',
            password='testpass123'
        )
        
        self.customer = Customer.objects.create(
            user=self.customer_user,
            google_id="test_id"
        )
        
        self.game = Game.objects.create(
            name="Analytics Test Game",
            description="Game for testing analytics",
            capacity=4,
            booking_type='HYBRID',
            opening_time=time(9, 0),
            closing_time=time(21, 0),
            slot_duration_minutes=60,
            available_days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
            private_price=Decimal('300.00'),
            shared_price=Decimal('80.00')
        )
    
    def test_peak_hours_detection(self):
        """Test that peak hours are correctly identified"""
        # Create bookings concentrated in certain hours
        peak_hours = [14, 15, 16]  # 2-4 PM peak
        low_hours = [9, 10, 20]    # 9-10 AM and 8 PM low
        
        # Create slots and bookings
        test_date = date.today()
        
        for hour in peak_hours + low_hours:
            slot = GameSlot.objects.create(
                game=self.game,
                date=test_date,
                start_time=time(hour, 0),
                end_time=time(hour + 1, 0)
            )
            
            SlotAvailability.objects.create(
                game_slot=slot,
                total_capacity=self.game.capacity
            )
            
            # Create more bookings for peak hours
            if hour in peak_hours:
                for i in range(3):  # 3 bookings per peak hour
                    booking = Booking(
                        customer=self.customer,
                        game=self.game,
                        game_slot=slot,
                        booking_type='SHARED',
                        spots_booked=1,
                        price_per_spot=self.game.shared_price,
                        total_amount=self.game.shared_price,
                        status='PENDING'
                    )
                    booking.save()
                    booking.status = 'CONFIRMED'
                    booking.save()
            elif hour in low_hours:
                # Only 1 booking for low hours
                booking = Booking(
                    customer=self.customer,
                    game=self.game,
                    game_slot=slot,
                    booking_type='SHARED',
                    spots_booked=1,
                    price_per_spot=self.game.shared_price,
                    total_amount=self.game.shared_price,
                    status='PENDING'
                )
                booking.save()
                booking.status = 'CONFIRMED'
                booking.save()
        
        # Test the optimization suggestions
        client = Client()
        client.login(username='owner', password='testpass123')
        
        url = reverse('booking:game_management:schedule_optimization_suggestions', 
                     kwargs={'game_id': self.game.id})
        response = client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should detect peak hours
        suggestions = data['suggestions']
        peak_suggestion = next((s for s in suggestions if s['type'] == 'peak_hours'), None)
        self.assertIsNotNone(peak_suggestion, "Peak hours should be detected")
    
    def test_utilization_rate_analysis(self):
        """Test utilization rate analysis and suggestions"""
        # Create many slots with few bookings (low utilization)
        test_date = date.today()
        
        slots_created = 0
        bookings_created = 0
        
        for hour in range(9, 21):  # 12 slots
            slot = GameSlot.objects.create(
                game=self.game,
                date=test_date,
                start_time=time(hour, 0),
                end_time=time(hour + 1, 0)
            )
            
            SlotAvailability.objects.create(
                game_slot=slot,
                total_capacity=self.game.capacity
            )
            slots_created += 1
            
            # Only book every 4th slot (25% utilization)
            if hour % 4 == 0:
                booking = Booking(
                    customer=self.customer,
                    game=self.game,
                    game_slot=slot,
                    booking_type='PRIVATE',
                    spots_booked=self.game.capacity,
                    price_per_spot=self.game.private_price / self.game.capacity,
                    total_amount=self.game.private_price,
                    status='PENDING'
                )
                booking.save()
                booking.status = 'CONFIRMED'
                booking.save()
                bookings_created += 1
        
        # Test optimization suggestions
        client = Client()
        client.login(username='owner', password='testpass123')
        
        url = reverse('booking:game_management:schedule_optimization_suggestions', 
                     kwargs={'game_id': self.game.id})
        response = client.get(url)
        
        data = response.json()
        
        # Should detect low utilization
        suggestions = data['suggestions']
        utilization_suggestion = next((s for s in suggestions if s['type'] == 'low_utilization'), None)
        self.assertIsNotNone(utilization_suggestion, "Low utilization should be detected")
        
        # Check analytics
        analytics = data['analytics']
        expected_utilization = bookings_created / slots_created
        self.assertAlmostEqual(analytics['utilization_rate'], expected_utilization, places=2)