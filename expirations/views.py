from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from contracts.models import Contract
from utils import mixins


class BaseContractExpiredView(
    mixins.DepartmentListFilterMixin, LoginRequiredMixin, TemplateView
):
    template_name = ""
    data_filter = None

    def get_queryset(self):
        return Contract.objects.filter(self.data_filter, active=True, is_deleted=False)

    def get(self, request, *args, **kwargs):
        contracts = self.get_queryset()
        total = contracts.count()
        context = {"contracts": contracts, "total": total}
        return render(request, self.template_name, context)


class ExpiredContracts(BaseContractExpiredView):
    data_filter = Q(end_date__lt=timezone.now().date())
    template_name = "expired_contracts.html"


class ContractsDueIn45Days(BaseContractExpiredView):
    data_filter = (
        Q(end_date__gte=timezone.now().date())
        & Q(end_date__lte=timezone.now().date() + timezone.timedelta(days=45))
        & Q(automatic_renewal=True)
        & Q(is_deleted=False)
    )
    template_name = "contracts_due_in_45_days.html"


class ContractsDueIn30Days(BaseContractExpiredView):
    data_filter = (
        Q(end_date__gte=timezone.now().date())
        & Q(end_date__lte=timezone.now().date() + timezone.timedelta(days=30))
        & Q(automatic_renewal=False)
        & Q(is_deleted=False)
    )
    template_name = "contracts_due_in_30_days.html"


class Expired(LoginRequiredMixin, TemplateView):
    template_name = "expired.html"
