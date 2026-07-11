from django.urls import path
from . import settings_views as views

app_name = 'settings'

urlpatterns = [
    path('', views.settings_view, name='index'),
    path('company/', views.company_settings, name='company'),
    path('users/', views.user_management, name='users'),
    path('verification/', views.verification_settings, name='verification'),
]
