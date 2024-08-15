from django.urls import path

from . import views

app_name = "contracts"

urlpatterns = [
    path("contracts/", views.ContractListView.as_view(), name="contract_list"),
    path(
        "contracts/<int:pk>/", views.ContractDetailView.as_view(), name="contract_detail"
    ),
    path("contracts/create/", views.ContractCreateView.as_view(), name="contract_create"),
    path(
        "contracts/<int:pk>/update/",
        views.ContractUpdateView.as_view(),
        name="contract_update",
    ),
    path(
        "contracts/<int:pk>/delete/",
        views.ContractDeleteView.as_view(),
        name="contract_delete",
    ),
]
