from django.urls import path

from . import views

app_name = "dashboards"

urlpatterns = [
    path("dashboard/", views.Dashboard.as_view(), name="dashboard"),
    path(
        "dashboard/data/",
        views.DashboardFilteredData.as_view(),
        name="filtered_contract_data",
    ),
    path('contract-query/', views.ContractQueryView.as_view(), name='contract_query'),
]
