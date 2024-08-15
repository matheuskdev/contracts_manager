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
        name = self.request.GET.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)
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


class ContractDeleteView(
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = models.Contract
    template_name = "contract_confirm_delete.html"
    success_url = reverse_lazy("contracts:contract_list")
    permission_required = "contracts.delete_contract"
