from django.urls import path

from . import views

app_name = "parts"

urlpatterns = [
    path("parts/", views.PartListView.as_view(), name="part_list"),
    path(
        "parts/<int:pk>/", views.PartDetailView.as_view(), name="part_detail"
    ),
    path("parts/create/", views.PartCreateView.as_view(), name="part_create"),
    path(
        "parts/<int:pk>/update/",
        views.PartUpdateView.as_view(),
        name="part_update",
    ),
    path(
        "parts/<int:pk>/delete/",
        views.PartDeleteView.as_view(),
        name="part_delete",
    ),
]
