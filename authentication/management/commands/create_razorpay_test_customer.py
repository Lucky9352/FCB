from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication.models import Customer


class Command(BaseCommand):
    help = 'Create a test customer account for Razorpay domain verification'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating Razorpay test customer account...\n')

        # Test account credentials
        username = 'razorpay_test'
        email = 'razorpay.test@tapnex.tech'
        password = 'Razorpay@Test2024'
        
        try:
            # Check if test user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
                user = User.objects.get(username=username)
                # Update password in case it was changed
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS('✓ Updated password for existing user'))
            else:
                # Create new user
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name='Razorpay',
                    last_name='Test'
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Created user: {username}'))

            # Check if customer profile exists
            if hasattr(user, 'customer_profile'):
                self.stdout.write(self.style.WARNING('Customer profile already exists.'))
                customer = user.customer_profile
            else:
                # Create customer profile
                customer = Customer.objects.create(
                    user=user,
                    phone='+919999999999',
                    is_active=True
                )
                self.stdout.write(self.style.SUCCESS('✓ Created Customer profile'))

            # Display credentials
            self.stdout.write('\n' + '=' * 70)
            self.stdout.write(self.style.SUCCESS('RAZORPAY TEST CUSTOMER ACCOUNT CREATED!'))
            self.stdout.write('=' * 70)
            self.stdout.write('\n📋 CREDENTIALS FOR RAZORPAY VERIFICATION:')
            self.stdout.write('\n' + '-' * 70)
            self.stdout.write(f'\n  Test Account Email:    {email}')
            self.stdout.write(f'  Test Account Password: {password}')
            self.stdout.write(f'\n  Username:              {username}')
            self.stdout.write(f'  Phone:                 {customer.phone}')
            self.stdout.write('\n' + '-' * 70)
            self.stdout.write('\n🔗 LOGIN URLS:')
            self.stdout.write('  Customer Login: https://forge.tapnex.tech/accounts/customer/login/')
            self.stdout.write('  Or direct:      https://forge.tapnex.tech/accounts/login/')
            self.stdout.write('\n' + '-' * 70)
            self.stdout.write('\n📝 INSTRUCTIONS FOR RAZORPAY FORM:')
            self.stdout.write('\n  1. Website Link: https://forge.tapnex.tech')
            self.stdout.write(f'  2. Test Username: {email}')
            self.stdout.write(f'  3. Test Password: {password}')
            self.stdout.write('\n' + '=' * 70)
            self.stdout.write('\n✅ This account can be used to test the complete booking flow.')
            self.stdout.write('✅ Razorpay will use these credentials to verify payment integration.')
            self.stdout.write('\n')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating test customer: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
