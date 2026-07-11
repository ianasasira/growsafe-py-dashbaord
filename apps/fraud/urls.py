from django.urls import path
from . import views

app_name = 'fraud'

urlpatterns = [
    path('', views.fraud_list, name='list'),
    path('<uuid:pk>/', views.fraud_detail, name='detail'),
    path('<uuid:pk>/resolve/', views.resolve_alert, name='resolve'),
    path('<uuid:pk>/dismiss/', views.dismiss_alert, name='dismiss'),
]
