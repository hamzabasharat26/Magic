from django.urls import path
from . import views

urlpatterns = [
    # Unified front login (hexagonal keypad) - ONLY login method
    path('login/', views.unified_login_view, name='unified_login'),
    
    # Shared logout
    path('logout/', views.logout_view, name='logout'),
    
    # Admin user management
    path('admin/users/', views.user_management_view, name='user_management'),
    path('admin/users/create/', views.user_create_view, name='user_create'),
    path('admin/users/edit/<int:user_id>/', views.user_edit_view, name='user_edit'),
    path('admin/users/delete/<int:user_id>/', views.user_delete_view, name='user_delete'),
    
    # Operator panel
    path('operator/panel/', views.operator_panel_view, name='operator_panel'),
    path('operator/products-by-brand/', views.get_products_by_brand, name='products_by_brand'),
    path('operator/available-sizes/', views.get_available_sizes, name='available_sizes'),
    path('operator/start-session/', views.start_measurement_session, name='start_session'),
    path('operator/end-session/<int:session_id>/', views.end_measurement_session, name='end_session'),
]
