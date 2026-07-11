from django.urls import path
from . import views

app_name = 'retailer_portal'

urlpatterns = [
    path('', views.retailer_dashboard, name='dashboard'),
    path('stock/', views.stock_verification, name='stock'),
    path('report/', views.report_issue, name='report'),
]
