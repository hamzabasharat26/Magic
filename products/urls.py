from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create-po/', views.create_purchase_order, name='create_po'),
    path('add-product/<int:po_id>/', views.add_product, name='add_product'),
    path('po-detail/<int:po_id>/', views.purchase_order_detail, name='purchase_order_detail'),
    path('get-standard-measurements/', views.get_standard_measurements, name='get_standard_measurements'),
]
