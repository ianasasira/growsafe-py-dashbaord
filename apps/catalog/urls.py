from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('create/', views.product_create, name='create'),
    path('<uuid:pk>/', views.product_detail, name='detail'),
    path('<uuid:pk>/edit/', views.product_edit, name='edit'),
    path('<uuid:pk>/delete/', views.product_delete, name='delete'),
]
