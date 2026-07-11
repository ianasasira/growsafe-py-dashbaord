from django.urls import path
from . import views

app_name = 'recalls'

urlpatterns = [
    path('', views.recall_list, name='list'),
    path('create/', views.recall_create, name='create'),
    path('<uuid:pk>/', views.recall_detail, name='detail'),
]
