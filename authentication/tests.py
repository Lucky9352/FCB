from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Customer, CafeOwner


class AuthenticationTestCase(TestCase):
    """Test cases for authentication system"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test users
        self.customer_user = User.objects.create_user(
            username='testcustomer',
            email='customer@test.com',
            password='TestPass123!'
        )
        self.customer_profile = Customer.objects.create(user=self.customer_user)
        
        self.owner_user = User.objects.create_user(
            username='testowner',
            email='owner@test.com',
            password='TestPass123!'
        )
        self.owner_profile = CafeOwner.objects.create(
            user=self.owner_user,
            cafe_name='Test Cafe',
            contact_email='owner@test.com',
            phone='+1234567890'
        )
        
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='AdminPass123!'
        )
    
    def test_customer_login_view(self):
        """Test customer login page loads correctly"""
        response = self.client.get(reverse('authentication:customer_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome Back, Gamer!')
    
    def test_cafe_owner_login_view(self):
        """Test cafe owner login page loads correctly"""
        response = self.client.get(reverse('authentication:cafe_owner_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cafe Owner Portal')
    
    def test_customer_dashboard_access(self):
        """Test customer can access customer dashboard"""
        self.client.login(username='testcustomer', password='TestPass123!')
        response = self.client.get(reverse('authentication:customer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back')
    
    def test_cafe_owner_dashboard_access(self):
        """Test cafe owner can access owner dashboard"""
        self.client.login(username='testowner', password='TestPass123!')
        response = self.client.get(reverse('authentication:cafe_owner_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Owner Portal')
    
    def test_role_based_access_control(self):
        """Test that users can only access appropriate dashboards"""
        # Customer trying to access owner dashboard
        self.client.login(username='testcustomer', password='TestPass123!')
        response = self.client.get(reverse('authentication:cafe_owner_dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Owner trying to access customer dashboard  
        self.client.login(username='testowner', password='TestPass123!')
        response = self.client.get(reverse('authentication:customer_dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect
