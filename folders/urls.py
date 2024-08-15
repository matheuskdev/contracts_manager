from django.urls import path

from . import views

app_name = "folders"

urlpatterns = [
    path("folders/", views.FolderListView.as_view(), name="folder_list"),
    path("folders/<int:pk>/", views.FolderDetailView.as_view(), name="folder_detail"),
    path("folders/create/", views.FolderCreateView.as_view(), name="folder_create"),
    path("folders/<int:pk>/update/", views.FolderUpdateView.as_view(), name="folder_update"),
    path("folders/<int:pk>/delete/", views.FolderDeleteView.as_view(), name="folder_delete"),
]
