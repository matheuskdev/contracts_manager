from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from utils import mixins

from . import forms, models


class ContractListView(
    mixins.DepartmentListFilterMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = models.Contract
    template_name = "contract_list.html"
    context_object_name = "contracts"
    paginate_by = 10
    permission_required = "contracts.view_contract"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("subject")

        if name:
            queryset = queryset.filter(subject__icontains=name)
        return queryset


class ContractCreateView(
    LoginRequiredMixin,
    mixins.OwnerUserMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = models.Contract
    template_name = "contract_form.html"
    form_class = forms.ContractForm
    success_url = reverse_lazy("contracts:contract_list")
    permission_required = "contracts.add_contract"


class ContractDetailView(
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = models.Contract
    template_name = "contract_detail.html"
    context_object_name = "contract"
    permission_required = "contracts.view_contract"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract = self.get_object()
        # Includes the amendments associated with the contract in the context
        context["addendums"] = contract.addendums.filter(contract=contract)
        context["evaluations"] = contract.evaluations.filter(contract=contract)
        return context


class ContractUpdateView(
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = models.Contract
    template_name = "contract_form.html"
    form_class = forms.ContractForm
    success_url = reverse_lazy("contracts:contract_list")
    permission_required = "contracts.change_contract"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        contract = self.get_object()

        kwargs["initial"] = {
            "start_date": (
                contract.start_date.strftime("%Y-%m-%d") if contract.start_date else ""
            ),
            "end_date": (
                contract.end_date.strftime("%Y-%m-%d") if contract.end_date else ""
            ),
        }
        return kwargs


class ContractDeleteView(
    mixins.SoftDeleteViewMixin,
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = models.Contract
    template_name = "contract_confirm_delete.html"
    success_url = reverse_lazy("contracts:contract_list")
    permission_required = "contracts.delete_contract"
