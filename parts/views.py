from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from utils import mixins

from . import forms, models


class PartListView(
    mixins.DepartmentListFilterMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = models.Part
    template_name = "part_list.html"
    context_object_name = "parts"
    paginate_by = 10
    permission_required = "parts.view_part"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class PartCreateView(
    LoginRequiredMixin,
    mixins.OwnerUserMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = models.Part
    template_name = "part_form.html"
    form_class = forms.PartForm
    success_url = reverse_lazy("parts:part_list")
    permission_required = "parts.add_part"


class PartDetailView(
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = models.Part
    template_name = "part_detail.html"
    context_object_name = "part"
    permission_required = "parts.view_part"


class PartUpdateView(
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = models.Part
    template_name = "part_form.html"
    form_class = forms.PartForm
    success_url = reverse_lazy("parts:part_list")
    permission_required = "parts.change_part"


class PartDeleteView(
    mixins.SoftDeleteViewMixin,
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = models.Part
    template_name = "part_confirm_delete.html"
    success_url = reverse_lazy("parts:part_list")
    permission_required = "parts.delete_part"
