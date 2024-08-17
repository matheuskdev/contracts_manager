from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from contracts.models import Contract
from utils import mixins

from . import forms, models


class AddendumListView(
    mixins.DepartmentListFilterMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = models.Addendum
    template_name = "addendum_list.html"
    context_object_name = "addendums"
    paginate_by = 2
    permission_required = "addendums.view_folder"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("title")

        if name:
            queryset = queryset.filter(title__icontains=name)
        return queryset


class AddendumCreateView(
    LoginRequiredMixin,
    mixins.OwnerUserMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = models.Addendum
    template_name = "addendum_form.html"
    form_class = forms.AddendumForm
    success_url = reverse_lazy("addendums:addendum_list")
    permission_required = "addendums.add_addendum"

    def form_valid(self, form):
        contract_id = self.kwargs.get("contract_id")
        contract = get_object_or_404(Contract, id=contract_id)
        form.instance.contract = contract
        response = super().form_valid(form)
        contract.contains_addendum = True
        contract.save()
        return response

    def get_success_url(self):
        return reverse_lazy(
            "contracts:contract_detail", kwargs={"pk": self.kwargs["contract_id"]}
        )


class AddendumDetailView(
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = models.Addendum
    template_name = "addendum_detail.html"
    context_object_name = "addendum"
    permission_required = "addendums.view_addendum"


class AddendumUpdateView(
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = models.Addendum
    template_name = "addendum_form.html"
    form_class = forms.AddendumForm
    success_url = reverse_lazy("addendums:addendum_list")
    permission_required = "addendum.change_addendum"


class AddendumDeleteView(
    mixins.SoftDeleteViewMixin,
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = models.Addendum
    template_name = "addendum_confirm_delete.html"
    success_url = reverse_lazy("addendums:addendum_list")
    permission_required = "addendums.delete_addendum"
