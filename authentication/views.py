from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .forms import CafeOwnerLoginForm, CafeOwnerRegistrationForm
from .models import Customer, CafeOwner


class CafeOwnerLoginView(LoginView):
    """Custom login view for cafe owners"""
    form_class = CafeOwnerLoginForm
    template_name = 'authentication/cafe_owner_login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        # Check if user is a cafe owner
        if hasattr(self.request.user, 'cafe_owner_profile'):
            return '/owner/dashboard/'
        elif self.request.user.is_superuser:
            return '/admin/'
        else:
            messages.error(self.request, 'Access denied. This login is for cafe owners only.')
            return '/accounts/login/'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class CafeOwnerRegistrationView(CreateView):
    """Registration view for cafe owners"""
    form_class = CafeOwnerRegistrationForm
    template_name = 'authentication/cafe_owner_register.html'
    success_url = reverse_lazy('cafe_owner_login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! You can now log in.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view with redirect logic"""
    next_page = '/'
    http_method_names = ['get', 'post']  # Allow both GET and POST
    
    def dispatch(self, request, *args, **kwargs):
        # Perform logout first
        response = super().dispatch(request, *args, **kwargs)
        
        # Add success message after logout
        messages.success(request, 'You have been successfully logged out.')
        
        return response


def customer_login_view(request):
    """Customer login view - redirects to Google OAuth or shows customer login options"""
    if request.user.is_authenticated:
        if hasattr(request.user, 'customer_profile'):
            return redirect('/customer/dashboard/')
        else:
            messages.error(request, 'Please use the appropriate login method.')
            logout(request)
    
    return render(request, 'authentication/customer_login.html')


@login_required
def profile_redirect_view(request):
    """Redirect users to appropriate dashboard based on their role"""
    user = request.user
    
    # Check for TapNex superuser first
    if hasattr(user, 'tapnex_superuser_profile') or user.is_superuser:
        return redirect('authentication:tapnex_dashboard')
    elif hasattr(user, 'cafe_owner_profile'):
        return redirect('/owner/dashboard/')
    elif hasattr(user, 'customer_profile'):
        return redirect('/customer/dashboard/')
    else:
        # User doesn't have a profile, create customer profile for Google OAuth users
        if user.socialaccount_set.exists():
            Customer.objects.get_or_create(user=user)
            return redirect('/customer/dashboard/')
        else:
            messages.error(request, 'Unable to determine user role. Please contact support.')
            logout(request)
            return redirect('/')


def home_view(request):
    """Home page view with role-based navigation"""
    return render(request, 'home.html')
