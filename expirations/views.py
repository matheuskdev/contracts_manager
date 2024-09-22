from typing import Any, Optional, Union
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from contracts.models import Contract
from utils import mixins

class BaseContractExpiredView(
    mixins.DepartmentListFilterMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView,
):
    template_name: str = ""
    data_filter: Optional[Q] = None
    permission_required: str = "expirations.view_expiration"

    def get_queryset(self) -> QuerySet[Contract]:
        """
        Return a queryset of contracts that match the specified date filter.
        Excludes deleted contracts and includes contracts with 'approved' or 'renewed' statuses.

        :return: QuerySet of filtered contracts.
        """
        return Contract.objects.filter(
            self.data_filter, is_deleted=False, status__in=["approved", "renewed"]
        )

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Handle GET requests by passing filtered contracts and their total count to the template.

        :param request: HttpRequest object.
        :return: Rendered HTML response with the context containing contracts and total count.
        """
        contracts: QuerySet[Contract] = self.get_queryset()
        total: int = contracts.count()
        context: dict[str, Union[QuerySet[Contract], int]] = {"contracts": contracts, "total": total}
        return render(request, self.template_name, context)


class ExpiredContracts(BaseContractExpiredView):
    """
    View to display expired contracts.
    """
    data_filter: Q = Q(end_date__lt=timezone.now().date())
    template_name: str = "expired_contracts.html"


class ContractsDueIn45Days(BaseContractExpiredView):
    """
    View to display contracts expiring in the next 45 days and marked for automatic renewal.
    """
    data_filter: Q = (
        Q(end_date__gte=timezone.now().date())
        & Q(end_date__lte=timezone.now().date() + timezone.timedelta(days=45))
        & Q(automatic_renewal=True)
    )
    template_name: str = "contracts_due_in_45_days.html"


class ContractsDueIn30Days(BaseContractExpiredView):
    """
    View to display contracts expiring in the next 30 days without automatic renewal.
    """
    data_filter: Q = (
        Q(end_date__gte=timezone.now().date())
        & Q(end_date__lte=timezone.now().date() + timezone.timedelta(days=30))
        & Q(automatic_renewal=False)
    )
    template_name: str = "contracts_due_in_30_days.html"


class Expired(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """
    View to handle the expired contracts page with appropriate user permissions.
    Displays an error message if the user does not have permission or is not authenticated.
    """
    permission_required: str = "expirations.view_expiration"
    template_name: str = "expired.html"

    def handle_no_permission(self) -> HttpResponse:
        """
        Redirect the user to the home page if they lack the required permission.
        Displays an error message if the user is authenticated but lacks permission.

        :return: Redirect to home page or invoke default permission handling.
        """
        if self.request.user.is_authenticated:
            messages.error(
                self.request,
                "Você não tem permissão para acessar a página anterior.",
            )
            return redirect(reverse_lazy("home"))
        else:
            return super().handle_no_permission()
