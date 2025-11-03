from django.urls import path, include
from . import views
from . import payment_views
from . import verification_views

app_name = 'booking'

urlpatterns = [
    # OLD BOOKING SYSTEM (Backward Compatibility)
    path('select/', views.booking_selection, name='selection'),
    path('create/', views.booking_create, name='create'),
    path('confirm/<uuid:booking_id>/', views.booking_confirm, name='confirm'),
    path('success/<uuid:booking_id>/', views.booking_success, name='success'),
    
    # NEW HYBRID BOOKING SYSTEM
    path('games/', views.game_selection, name='game_selection'),
    path('games/<uuid:game_id>/', views.game_detail, name='game_detail'),
    path('games/book/', views.hybrid_booking_create, name='hybrid_booking_create'),
    path('games/confirm/<uuid:booking_id>/', views.hybrid_booking_confirm, name='hybrid_booking_confirm'),
    path('games/update-spots/<uuid:booking_id>/', views.update_booking_spots, name='update_booking_spots'),
    path('games/cancel/<uuid:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
    # Customer booking management
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
    # Booking actions (OLD)
    path('simulate-payment/<uuid:booking_id>/', views.simulate_payment, name='simulate_payment'),
    
    # RAZORPAY PAYMENT INTEGRATION
    path('payment/create-order/<uuid:booking_id>/', payment_views.create_razorpay_order, name='create_razorpay_order'),
    path('payment/verify/', payment_views.verify_razorpay_payment, name='verify_razorpay_payment'),
    path('payment/webhook/', payment_views.razorpay_webhook, name='razorpay_webhook'),
    path('payment/cancelled/<uuid:booking_id>/', payment_views.payment_cancelled, name='payment_cancelled'),
    path('payment/success/<uuid:booking_id>/', payment_views.payment_success, name='payment_success'),
    path('payment/status/<uuid:booking_id>/', payment_views.check_payment_status, name='check_payment_status'),
    
    # QR CODE VERIFICATION (Owner/Staff)
    path('qr-scanner/', verification_views.qr_scanner_view, name='qr_scanner'),
    path('verify-qr/', verification_views.verify_booking_qr, name='verify_booking_qr'),
    path('complete/<uuid:booking_id>/', verification_views.complete_booking, name='complete_booking'),
    path('active-bookings/', verification_views.active_bookings_view, name='active_bookings'),
    
    # Notifications
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # AJAX endpoints
    path('api/availability/', views.get_availability, name='get_availability'),
    path('api/slot-availability/<int:game_slot_id>/', views.get_slot_availability, name='get_slot_availability'),
    
    # Game Management URLs
    path('games/manage/', include('booking.game_management_urls', namespace='game_management')),
]