from django.apps import AppConfig


class BookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking'
    verbose_name = 'Gaming Cafe Booking System'
    
    def ready(self):
        import booking.signals
