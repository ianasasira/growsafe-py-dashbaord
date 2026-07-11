from django.urls import path
from . import views

app_name = 'batches'

urlpatterns = [
    path('', views.batch_list, name='list'),
    path('create/', views.batch_create, name='create'),
    path('<uuid:pk>/', views.batch_detail, name='detail'),
    path('<uuid:pk>/generate-codes/', views.generate_codes, name='generate_codes'),
    path('<uuid:pk>/export/', views.export_codes, name='export'),
]
