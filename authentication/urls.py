from django.urls import path
from . import views
from . import dashboard_views
from . import tapnex_views

app_name = 'authentication'

urlpatterns = [
    # Customer authentication (Google OAuth handled by allauth)
    path('login/', views.customer_login_view, name='customer_login'),
    
    # Cafe owner authentication
    path('cafe-owner/login/', views.CafeOwnerLoginView.as_view(), name='cafe_owner_login'),
    path('cafe-owner/register/', views.CafeOwnerRegistrationView.as_view(), name='cafe_owner_register'),
    
    # Common authentication
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile_redirect_view, name='profile_redirect'),
    
    # Dashboards
    path('customer/dashboard/', dashboard_views.customer_dashboard, name='customer_dashboard'),
    path('owner/dashboard/', dashboard_views.cafe_owner_dashboard, name='cafe_owner_dashboard'),
    
    # TapNex Superuser Dashboard and Management
    path('tapnex/dashboard/', tapnex_views.tapnex_dashboard, name='tapnex_dashboard'),
    path('tapnex/commission-settings/', tapnex_views.commission_settings, name='commission_settings'),
    path('tapnex/revenue-reports/', tapnex_views.revenue_reports, name='revenue_reports'),
    path('tapnex/cafe-owner-management/', tapnex_views.cafe_owner_management, name='cafe_owner_management'),
    path('tapnex/reset-cafe-owner-password/', tapnex_views.reset_cafe_owner_password, name='reset_cafe_owner_password'),
    path('tapnex/system-analytics/', tapnex_views.system_analytics, name='system_analytics'),
    path('tapnex/ajax/revenue-data/', tapnex_views.ajax_revenue_data, name='ajax_revenue_data'),
]