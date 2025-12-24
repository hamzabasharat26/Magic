from django.urls import path
from . import views

urlpatterns = [
    path('', views.measurement_dashboard, name='measurement_dashboard'),
    path('upload-and-analyze/', views.upload_and_analyze, name='upload_analyze'),
    path('save-qc-result/', views.save_qc_result, name='save_qc_result'),
    path('get-available-sizes/', views.get_available_sizes, name='get_available_sizes'),
    path('get-size-chart/', views.get_size_chart, name='get_size_chart'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('generate-daily-report/', views.generate_daily_report, name='generate_daily_report'),
]