from django.urls import path

from . import views

app_name = "addendums"

urlpatterns = [
    path("addendums/", views.AddendumListView.as_view(), name="addendum_list"),
    path(
        "addendums/<int:pk>/", views.AddendumDetailView.as_view(), name="addendum_detail"
    ),
    path(
        "addendums/create/<int:contract_id>/",
        views.AddendumCreateView.as_view(),
        name="addendum_create",
    ),
    path(
        "addendums/<int:pk>/update/",
        views.AddendumUpdateView.as_view(),
        name="addendum_update",
    ),
    path(
        "addendums/<int:pk>/delete/",
        views.AddendumDeleteView.as_view(),
        name="addendum_delete",
    ),
]
