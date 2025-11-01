from django.urls import path, include
from . import views

app_name = 'booking'

urlpatterns = [
    # OLD BOOKING SYSTEM (Backward Compatibility)
    path('select/', views.booking_selection, name='selection'),
    path('create/', views.booking_create, name='create'),
    path('confirm/<uuid:booking_id>/', views.booking_confirm, name='confirm'),
    path('success/<uuid:booking_id>/', views.booking_success, name='success'),
    
    # NEW HYBRID BOOKING SYSTEM
    path('games/', views.game_selection, name='game_selection'),
    path('games/book/', views.hybrid_booking_create, name='hybrid_booking_create'),
    path('games/confirm/<uuid:booking_id>/', views.hybrid_booking_confirm, name='hybrid_booking_confirm'),
    path('games/cancel/<uuid:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
    # Customer booking management
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
    # Booking actions (OLD)
    path('simulate-payment/<uuid:booking_id>/', views.simulate_payment, name='simulate_payment'),
    
    # Notifications
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # AJAX endpoints
    path('api/availability/', views.get_availability, name='get_availability'),
    path('api/slot-availability/<uuid:game_slot_id>/', views.get_slot_availability, name='get_slot_availability'),
    
    # Game Management URLs
    path('games/manage/', include('booking.game_management_urls', namespace='game_management')),
]