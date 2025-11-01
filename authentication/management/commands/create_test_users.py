from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authentication.models import CafeOwner, TapNexSuperuser


class Command(BaseCommand):
    help = 'Create test users for the system (owner and superuser)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test users...\n')

        # Create Cafe Owner
        try:
            # Check if owner user already exists
            if User.objects.filter(username='owner').exists():
                self.stdout.write(self.style.WARNING('User "owner" already exists. Skipping...'))
                owner_user = User.objects.get(username='owner')
            else:
                owner_user = User.objects.create_user(
                    username='owner',
                    password='aadijain',
                    email='owner@gamingcafe.com',
                    first_name='Cafe',
                    last_name='Owner'
                )
                self.stdout.write(self.style.SUCCESS('✓ Created user: owner'))

            # Check if cafe owner profile exists
            if hasattr(owner_user, 'cafe_owner_profile'):
                self.stdout.write(self.style.WARNING('Cafe Owner profile already exists. Skipping...'))
            else:
                cafe_owner = CafeOwner.objects.create(
                    user=owner_user,
                    cafe_name='TapNex Gaming Cafe',
                    contact_email='owner@gamingcafe.com',
                    phone='+919876543210'
                )
                self.stdout.write(self.style.SUCCESS('✓ Created Cafe Owner profile'))
                self.stdout.write(f'  - Cafe Name: {cafe_owner.cafe_name}')
                self.stdout.write(f'  - Email: {cafe_owner.contact_email}')
                self.stdout.write(f'  - Phone: {cafe_owner.phone}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating Cafe Owner: {str(e)}'))

        self.stdout.write('')

        # Create TapNex Superuser
        try:
            # Check if superuser user already exists
            if User.objects.filter(username='prabhav').exists():
                self.stdout.write(self.style.WARNING('User "prabhav" already exists. Skipping...'))
                superuser_user = User.objects.get(username='prabhav')
                # Update to make sure they're a superuser
                if not superuser_user.is_superuser:
                    superuser_user.is_superuser = True
                    superuser_user.is_staff = True
                    superuser_user.save()
                    self.stdout.write(self.style.SUCCESS('✓ Updated user to superuser status'))
            else:
                superuser_user = User.objects.create_superuser(
                    username='prabhav',
                    password='aadijain',
                    email='prabhav@tapnex.com',
                    first_name='Prabhav',
                    last_name='Admin'
                )
                self.stdout.write(self.style.SUCCESS('✓ Created superuser: prabhav'))

            # Check if TapNex Superuser profile exists
            if hasattr(superuser_user, 'tapnex_superuser_profile'):
                self.stdout.write(self.style.WARNING('TapNex Superuser profile already exists. Skipping...'))
            else:
                tapnex_superuser = TapNexSuperuser.objects.create(
                    user=superuser_user,
                    commission_rate=10.00,  # 10% commission
                    platform_fee=50.00,     # ₹50 platform fee per booking
                    contact_email='prabhav@tapnex.com',
                    phone='+919876543211'
                )
                self.stdout.write(self.style.SUCCESS('✓ Created TapNex Superuser profile'))
                self.stdout.write(f'  - Commission Rate: {tapnex_superuser.commission_rate}%')
                self.stdout.write(f'  - Platform Fee: ₹{tapnex_superuser.platform_fee}')
                self.stdout.write(f'  - Email: {tapnex_superuser.contact_email}')
                self.stdout.write(f'  - Phone: {tapnex_superuser.phone}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating TapNex Superuser: {str(e)}'))

        # Summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('Test Users Created Successfully!'))
        self.stdout.write('=' * 60)
        self.stdout.write('\nLogin Credentials:')
        self.stdout.write('\n1. CAFE OWNER:')
        self.stdout.write('   Username: owner')
        self.stdout.write('   Password: aadijain')
        self.stdout.write('   Login URL: /accounts/cafe-owner/login/')
        self.stdout.write('\n2. TAPNEX SUPERUSER:')
        self.stdout.write('   Username: prabhav')
        self.stdout.write('   Password: aadijain')
        self.stdout.write('   Login URL: /accounts/cafe-owner/login/ (or /admin/)')
        self.stdout.write('\n' + '=' * 60 + '\n')
