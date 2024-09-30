from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from utils import mixins

from . import forms, models


class FolderListView(
    mixins.DepartmentListFilterMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = models.Folder
    template_name = "folder_list.html"
    context_object_name = "folders"
    paginate_by = 5
    permission_required = "folders.view_folder"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class FolderCreateView(
    LoginRequiredMixin,
    mixins.OwnerUserMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = models.Folder
    template_name = "folder_form.html"
    form_class = forms.FolderForm
    success_url = reverse_lazy("folders:folder_list")
    permission_required = "folders.add_folder"


class FolderDetailView(
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = models.Folder
    template_name = "folder_detail.html"
    context_object_name = "folder"
    permission_required = "folders.view_folder"


class FolderUpdateView(
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = models.Folder
    template_name = "folder_form.html"
    form_class = forms.FolderForm
    success_url = reverse_lazy("folders:folder_list")
    permission_required = "folders.change_folder"


class FolderDeleteView(
    mixins.SoftDeleteViewMixin,
    mixins.DepartmentPermissionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = models.Folder
    template_name = "folder_confirm_delete.html"
    success_url = reverse_lazy("folders:folder_list")
    permission_required = "folders.delete_folder"
