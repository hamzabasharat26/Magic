from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OperatorSession

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'full_name', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['username', 'full_name', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'full_name')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'full_name')}),
    )

@admin.register(OperatorSession)
class OperatorSessionAdmin(admin.ModelAdmin):
    list_display = ['operator', 'product', 'started_at', 'measurements_count', 'status']
    list_filter = ['status', 'started_at', 'operator']
    search_fields = ['operator__username', 'product__purchase_order__po_number']
    date_hierarchy = 'started_at'
