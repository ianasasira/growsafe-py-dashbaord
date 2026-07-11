from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list, name='list'),
    path('verification/', views.verification_report, name='verification'),
    path('fraud/', views.fraud_report, name='fraud'),
    path('export/<str:report_type>/', views.export_report, name='export'),
]
