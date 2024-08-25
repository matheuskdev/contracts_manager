from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from contracts.models import Contract
from utils import mixins

from . import forms, models


class EvaluationListView(
    mixins.DepartmentListFilterMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = models.Evaluation
    template_name = "evaluation_list.html"
    context_object_name = "evaluations"
    paginate_by = 10
    permission_required = "evaluations.view_folder"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("rating")

        if name:
            queryset = queryset.filter(rating__icontains=name)
        return queryset


class EvaluationCreateView(
    LoginRequiredMixin,
    mixins.OwnerUserMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = models.Evaluation
    template_name = "evaluation_form.html"
    form_class = forms.EvaluationForm
    success_url = reverse_lazy("evaluations:evaluation_list")
    permission_required = "evaluations.add_evaluation"

    def form_valid(self, form):
        contract_id = self.kwargs.get("contract_id")
        form.instance.contract = get_object_or_404(Contract, pk=contract_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("evaluations:evaluation_list")


class EvaluationDetailView(
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = models.Evaluation
    template_name = "evaluation_detail.html"
    context_object_name = "evaluation"
    permission_required = "evaluations.view_evaluation"


class EvaluationUpdateView(
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = models.Evaluation
    template_name = "evaluation_form.html"
    form_class = forms.EvaluationForm
    success_url = reverse_lazy("evaluations:evaluation_list")
    permission_required = "evaluations.change_evaluation"


class EvaluationDeleteView(
    mixins.SoftDeleteViewMixin,
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = models.Evaluation
    template_name = "evaluation_confirm_delete.html"
    success_url = reverse_lazy("evaluations:evaluation_list")
    permission_required = "evaluations.delete_evaluation"
