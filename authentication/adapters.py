from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from .models import Customer


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter for handling Google OAuth authentication"""
    
    def pre_social_login(self, request, sociallogin):
        """Handle pre-login logic for social accounts"""
        if sociallogin.account.provider == 'google':
            # Check if user already exists with this email
            email = sociallogin.account.extra_data.get('email')
            if email:
                try:
                    from django.contrib.auth.models import User
                    existing_user = User.objects.get(email=email)
                    
                    # If user exists but doesn't have a social account, connect them
                    if not sociallogin.is_existing:
                        sociallogin.connect(request, existing_user)
                        
                except User.DoesNotExist:
                    pass
    
    def save_user(self, request, sociallogin, form=None):
        """Save user data from Google OAuth"""
        user = super().save_user(request, sociallogin, form)
        
        # Update user information from Google data
        extra_data = sociallogin.account.extra_data
        
        if not user.first_name and extra_data.get('given_name'):
            user.first_name = extra_data.get('given_name')
        
        if not user.last_name and extra_data.get('family_name'):
            user.last_name = extra_data.get('family_name')
            
        user.save()
        
        # Create customer profile for Google OAuth users
        Customer.objects.get_or_create(user=user)
        
        return user
    
    def get_login_redirect_url(self, request):
        """Redirect users to appropriate dashboard after Google login"""
        if request.user.is_authenticated:
            # Ensure customer profile exists for Google OAuth users
            if not hasattr(request.user, 'customer_profile') and not hasattr(request.user, 'cafe_owner_profile'):
                Customer.objects.get_or_create(user=request.user)
            
            if hasattr(request.user, 'customer_profile'):
                return '/accounts/customer/dashboard/'
            elif hasattr(request.user, 'cafe_owner_profile'):
                return '/accounts/owner/dashboard/'
            elif request.user.is_superuser:
                return '/accounts/tapnex/dashboard/'
            else:
                # Fallback - create customer profile
                Customer.objects.get_or_create(user=request.user)
                return '/accounts/customer/dashboard/'
        return '/accounts/login/'
    
    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        """Handle authentication errors with user-friendly messages"""
        if provider_id == 'google':
            if 'access_denied' in str(error):
                messages.error(request, 'Google authentication was cancelled. Please try again.')
            elif 'invalid_request' in str(error):
                messages.error(request, 'Invalid authentication request. Please try again.')
            else:
                messages.error(request, 'Authentication failed. Please try again or contact support.')
        
        return redirect(reverse('authentication:customer_login'))


class CustomAccountAdapter(DefaultAccountAdapter):
    """Custom adapter for account management"""
    
    def get_login_redirect_url(self, request):
        """Redirect users based on their role after manual login"""
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return '/admin/'
            elif hasattr(request.user, 'cafe_owner_profile'):
                return '/owner/dashboard/'
            elif hasattr(request.user, 'customer_profile'):
                return '/customer/dashboard/'
        return '/'
    
    def add_message(self, request, level, message_tag, message, extra_tags=''):
        """Customize message display - ensure message is a string"""
        # Don't add login success messages from allauth - we'll handle them ourselves
        if message_tag == 'account/messages/logged_in.txt':
            return
        
        # Convert message to string if it's not already
        if not isinstance(message, str):
            # If it's a dict, skip it (likely a context dict from allauth)
            if isinstance(message, dict):
                return
            message = str(message)
        
        messages.add_message(request, level, message, extra_tags=extra_tags)