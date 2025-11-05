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
    
    def form_valid(self, form):
        """Add success message on successful login"""
        response = super().form_valid(form)
        user = self.request.user
        username = user.username
        # Get cafe owner name if available
        if hasattr(user, 'cafe_owner_profile'):
            cafe_name = user.cafe_owner_profile.cafe_name
            messages.success(self.request, f'Welcome back, {cafe_name}!')
        else:
            messages.success(self.request, f'Welcome back, {username}!')
        return response

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
    """Custom logout view with custom template"""
    template_name = 'authentication/logout.html'
    http_method_names = ['get', 'post']  # Allow both GET and POST
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' or request.method == 'GET':
            # Perform logout
            logout(request)
            # Redirect to logout template
            return render(request, self.template_name)
        return super().dispatch(request, *args, **kwargs)


def customer_login_view(request):
    """Customer login view - redirects to Google OAuth or shows customer login options"""
    if request.user.is_authenticated:
        if hasattr(request.user, 'customer_profile'):
            return redirect('/customer/dashboard/')
        else:
            messages.error(request, 'Please use the appropriate login method.')
            logout(request)
    
    return render(request, 'authentication/customer_login.html')


def customer_email_login_view(request):
    """Handle traditional email/password login for customers (for testing purposes)"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user has customer profile
            if hasattr(user, 'customer_profile'):
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('authentication:customer_dashboard')
            else:
                # Create customer profile if doesn't exist
                Customer.objects.get_or_create(user=user)
                login(request, user)
                messages.success(request, f'Welcome, {user.get_full_name() or user.username}!')
                return redirect('authentication:customer_dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('authentication:customer_login')
    
    # If GET request, redirect to login page
    return redirect('authentication:customer_login')


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
    """Home page view with all available games (public access)"""
    from booking.models import Game
    
    # Get all active games
    games = Game.objects.filter(is_active=True).order_by('name')
    
    context = {
        'games': games,
    }
    return render(request, 'home.html', context)


def debug_user_view(request):
    """Debug view to check user authentication status"""
    if request.user.is_authenticated:
        return render(request, 'authentication/debug_user.html', {
            'user': request.user,
            'has_customer_profile': hasattr(request.user, 'customer_profile'),
            'has_cafe_owner_profile': hasattr(request.user, 'cafe_owner_profile'),
            'is_superuser': request.user.is_superuser,
        })
    else:
        return redirect('authentication:customer_login')


@login_required
def update_phone_number(request):
    """Update customer phone number"""
    from django.http import JsonResponse
    import json
    
    if request.method == 'POST':
        try:
            # Check if user has customer profile
            if not hasattr(request.user, 'customer_profile'):
                return JsonResponse({
                    'success': False,
                    'error': 'Customer profile not found'
                }, status=403)
            
            data = json.loads(request.body)
            phone = data.get('phone', '').strip()
            
            # Validate phone number
            if not phone:
                return JsonResponse({
                    'success': False,
                    'error': 'Phone number is required'
                }, status=400)
            
            # Update customer phone
            customer = request.user.customer_profile
            customer.phone = phone
            customer.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Phone number updated successfully',
                'phone': phone
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)
