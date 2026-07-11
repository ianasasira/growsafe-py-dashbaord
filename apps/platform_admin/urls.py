from django.urls import path
from . import views

app_name = 'platform_admin'

urlpatterns = [
    path('', views.platform_overview, name='overview'),
    path('companies/', views.company_list, name='companies'),
    path('companies/<uuid:pk>/', views.company_detail, name='company_detail'),
    path('companies/<uuid:pk>/suspend/', views.suspend_company, name='suspend'),
    path('analytics/', views.platform_analytics, name='analytics'),
]
