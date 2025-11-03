"""
Test the booking endpoint to debug the issue
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaming_cafe.settings')
django.setup()

from django.test import Client
from booking.models import GameSlot, Game
from authentication.models import User, Customer
import json

# Create a test client
client = Client()

# Get a game slot
slot = GameSlot.objects.filter(is_active=True).first()
if not slot:
    print("No active slots found!")
    exit(1)

print(f"Testing with slot: {slot.id}")
print(f"Game: {slot.game.name}")
print(f"Time: {slot.start_time} - {slot.end_time}")
print()

# Test without authentication
print("=" * 60)
print("TEST 1: Booking without authentication")
print("=" * 60)

response = client.post(
    '/booking/games/book/',
    data=json.dumps({
        'game_slot_id': str(slot.id),
        'booking_type': 'PRIVATE',
        'spots_requested': 1
    }),
    content_type='application/json'
)

print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")

try:
    data = response.json()
    print(f"Response JSON: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"Failed to parse JSON: {e}")
    print(f"Raw content: {response.content[:500]}")

print()

# Test with authentication
print("=" * 60)
print("TEST 2: Booking with authentication")
print("=" * 60)

# Get or create a test user
user, created = User.objects.get_or_create(
    username='testcustomer',
    defaults={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'Customer'
    }
)

# Get or create customer profile
customer, created = Customer.objects.get_or_create(
    user=user,
    defaults={
        'phone_number': '1234567890'
    }
)

# Login
client.force_login(user)

response = client.post(
    '/booking/games/book/',
    data=json.dumps({
        'game_slot_id': str(slot.id),
        'booking_type': 'PRIVATE',
        'spots_requested': 1
    }),
    content_type='application/json'
)

print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")

try:
    data = response.json()
    print(f"Response JSON: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"Failed to parse JSON: {e}")
    print(f"Raw content: {response.content[:500]}")

print()
print("=" * 60)
print("Tests completed!")
print("=" * 60)
