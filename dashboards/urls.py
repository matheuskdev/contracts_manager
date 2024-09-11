from django.urls import  path
from .  import views

app_name ='dashboards'

urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
]
