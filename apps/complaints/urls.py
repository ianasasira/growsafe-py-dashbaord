from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('', views.complaint_list, name='list'),
    path('<uuid:pk>/', views.complaint_detail, name='detail'),
    path('<uuid:pk>/update/', views.update_complaint, name='update'),
]
