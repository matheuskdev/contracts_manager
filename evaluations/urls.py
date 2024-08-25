from django.urls import path

from . import views

app_name = "evaluations"

urlpatterns = [
    path("evaluations/", views.EvaluationListView.as_view(), name="evaluation_list"),
    path(
        "evaluations/<int:pk>/",
        views.EvaluationDetailView.as_view(),
        name="evaluation_detail",
    ),
    path(
        "evaluations/create/<int:contract_id>/",
        views.EvaluationCreateView.as_view(),
        name="evaluation_create",
    ),
    path(
        "evaluations/<int:pk>/edit/",
        views.EvaluationUpdateView.as_view(),
        name="evaluation_update",
    ),
    path(
        "evaluations/<int:pk>/delete/",
        views.EvaluationDeleteView.as_view(),
        name="evaluation_delete",
    ),
]
