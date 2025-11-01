from django.contrib import admin
from .models import Customer, CafeOwner


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone')
    readonly_fields = ('created_at', 'google_id')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'google_id')
        }),
        ('Contact Information', {
            'fields': ('phone', 'avatar_url')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
    )


@admin.register(CafeOwner)
class CafeOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'cafe_name', 'contact_email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'cafe_name', 'contact_email')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Cafe Information', {
            'fields': ('cafe_name', 'contact_email', 'phone')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
