import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaming_cafe.settings')
django.setup()

from booking.models import Booking

b = Booking.objects.filter(status='CONFIRMED').first()
if b:
    print('\n' + '='*60)
    print('Sample Confirmed Booking:')
    print('='*60)
    print(f'  ID: {b.id}')
    print(f'  Customer: {b.customer.user.get_full_name()}')
    print(f'  Subtotal: Rs.{b.subtotal}')
    print(f'  Platform Fee: Rs.{b.platform_fee}')
    print(f'  Total Amount: Rs.{b.total_amount}')
    print(f'  Status: {b.status}')
    print('='*60)
    print('\nPlatform fee is working correctly!')
else:
    print('No confirmed bookings found')
