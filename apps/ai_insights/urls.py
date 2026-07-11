from django.urls import path
from . import views

app_name = 'ai_insights'

urlpatterns = [
    path('', views.insights_list, name='list'),
    path('query/', views.query_insights, name='query'),
]
