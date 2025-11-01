from django.core.management.base import BaseCommand
from django.utils import timezone
from booking.models import Booking


class Command(BaseCommand):
    help = 'Update booking statuses based on current time'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )
    
    def handle(self, *args, **options):
        now = timezone.now()
        dry_run = options['dry_run']
        
        # Find bookings that should be started
        bookings_to_start = Booking.objects.filter(
            status='CONFIRMED',
            start_time__lte=now,
            end_time__gt=now
        )
        
        # Find bookings that should be completed
        bookings_to_complete = Booking.objects.filter(
            status='IN_PROGRESS',
            end_time__lte=now
        )
        
        # Find bookings that are no-shows (confirmed but past start time + 15 minutes)
        no_show_threshold = now - timezone.timedelta(minutes=15)
        bookings_no_show = Booking.objects.filter(
            status='CONFIRMED',
            start_time__lte=no_show_threshold
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN - No changes will be made')
            )
        
        # Update bookings to IN_PROGRESS
        if bookings_to_start.exists():
            count = bookings_to_start.count()
            if not dry_run:
                bookings_to_start.update(status='IN_PROGRESS')
            self.stdout.write(
                self.style.SUCCESS(
                    f'{"Would update" if dry_run else "Updated"} {count} booking(s) to IN_PROGRESS'
                )
            )
            for booking in bookings_to_start:
                self.stdout.write(f'  - {booking.id}: {booking.customer} at {booking.gaming_station.name}')
        
        # Update bookings to COMPLETED
        if bookings_to_complete.exists():
            count = bookings_to_complete.count()
            if not dry_run:
                bookings_to_complete.update(status='COMPLETED')
            self.stdout.write(
                self.style.SUCCESS(
                    f'{"Would update" if dry_run else "Updated"} {count} booking(s) to COMPLETED'
                )
            )
            for booking in bookings_to_complete:
                self.stdout.write(f'  - {booking.id}: {booking.customer} at {booking.gaming_station.name}')
        
        # Update bookings to NO_SHOW
        if bookings_no_show.exists():
            count = bookings_no_show.count()
            if not dry_run:
                bookings_no_show.update(status='NO_SHOW')
            self.stdout.write(
                self.style.WARNING(
                    f'{"Would update" if dry_run else "Updated"} {count} booking(s) to NO_SHOW'
                )
            )
            for booking in bookings_no_show:
                self.stdout.write(f'  - {booking.id}: {booking.customer} at {booking.gaming_station.name}')
        
        if not (bookings_to_start.exists() or bookings_to_complete.exists() or bookings_no_show.exists()):
            self.stdout.write(
                self.style.SUCCESS('No bookings need status updates')
            )