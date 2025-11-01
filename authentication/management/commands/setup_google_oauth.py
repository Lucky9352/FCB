from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup Google OAuth Social Application'

    def handle(self, *args, **options):
        # Get or create the site
        site, created = Site.objects.get_or_create(
            pk=settings.SITE_ID,
            defaults={
                'domain': 'forge.tapnex.tech',
                'name': 'TapNex Gaming Cafe'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created site: {site.domain}')
            )
        else:
            # Update existing site
            site.domain = 'forge.tapnex.tech'
            site.name = 'TapNex Gaming Cafe'
            site.save()
            self.stdout.write(
                self.style.SUCCESS(f'Updated site: {site.domain}')
            )

        # Get Google OAuth credentials from environment
        client_id = settings.GOOGLE_OAUTH_CLIENT_ID
        client_secret = settings.GOOGLE_OAUTH_CLIENT_SECRET

        if not client_id or not client_secret:
            self.stdout.write(
                self.style.ERROR('Google OAuth credentials not found in environment variables')
            )
            return

        # Create or update Google OAuth app
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': client_id,
                'secret': client_secret,
            }
        )

        if not created:
            # Update existing app
            google_app.client_id = client_id
            google_app.secret = client_secret
            google_app.save()

        # Add site to the app
        google_app.sites.add(site)

        if created:
            self.stdout.write(
                self.style.SUCCESS('Created Google OAuth Social Application')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Updated Google OAuth Social Application')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Google OAuth configured for site: {site.domain}')
        )