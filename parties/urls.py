from django.urls import path
from . import views 

urlpatterns = [
    path('', views.PartyListView.as_view(), name='party-list'),
    path('<int:pk>/', views.PartyDetailView.as_view(), name='party-detail'),
    path('create/', views.PartyCreateView.as_view(), name='party-create'),
    path('<int:pk>/update/', views.PartyUpdateView.as_view(), name='party-update'),
    path('<int:pk>/delete/', views.PartyDeleteView.as_view(), name='party-delete'),
]
