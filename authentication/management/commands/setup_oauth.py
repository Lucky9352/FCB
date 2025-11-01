from django.core.management.base import BaseCommand
from django.conf import settings
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Set up Google OAuth application'

    def handle(self, *args, **options):
        site = Site.objects.get(pk=settings.SITE_ID)
        
        # Set up Google OAuth
        if settings.GOOGLE_OAUTH_CLIENT_ID and settings.GOOGLE_OAUTH_CLIENT_SECRET:
            google_app, created = SocialApp.objects.get_or_create(
                provider='google',
                defaults={
                    'name': 'Google OAuth',
                    'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
                    'secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
                }
            )
            if not created:
                google_app.client_id = settings.GOOGLE_OAUTH_CLIENT_ID
                google_app.secret = settings.GOOGLE_OAUTH_CLIENT_SECRET
                google_app.save()
            
            google_app.sites.add(site)
            self.stdout.write(
                self.style.SUCCESS(f'Google OAuth app {"created" if created else "updated"} successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Google OAuth credentials not found in environment variables')
            )

        self.stdout.write(
            self.style.SUCCESS('Google OAuth setup completed!')
        )