from django.urls import path
from . import views

app_name: str = "expirations"

urlpatterns: list = [
    path(
        "has/",
        views.ExpiredContracts.as_view(),
        name="has_expired_contracts",
    ),
    path(
        "due-30-days/",
        views.ContractsDueIn30Days.as_view(),
        name="contracts_due_in_30_days",
    ),
    path(
        "due-45-days/",
        views.ContractsDueIn45Days.as_view(),
        name="contracts_due_in_45_days",
    ),
    path(
        "expirations/",
        views.Expired.as_view(),
        name="expired_contracts",
    ),
]
