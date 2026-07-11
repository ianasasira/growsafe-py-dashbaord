from django.urls import path
from . import views

app_name = 'supply_chain'

urlpatterns = [
    path('', views.partner_list, name='list'),
    path('create/', views.partner_create, name='create'),
    path('<uuid:pk>/', views.partner_detail, name='detail'),
    path('journey/<uuid:code_id>/', views.product_journey, name='journey'),
]
