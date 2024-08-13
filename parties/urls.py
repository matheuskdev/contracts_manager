from django.urls import path
from . import views 

app_name = 'parties'

urlpatterns = [
    path('parties/', views.PartyListView.as_view(), name='party_list'),
    path('parties/<int:pk>/', views.PartyDetailView.as_view(), name='party_detail'),
    path('parties/create/', views.PartyCreateView.as_view(), name='party_create'),
    path('parties/<int:pk>/update/', views.PartyUpdateView.as_view(), name='party_update'),
    path('parties/<int:pk>/delete/', views.PartyDeleteView.as_view(), name='party_delete'),
]
