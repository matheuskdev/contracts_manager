from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from . import manager


class TimestampModelMixin(models.Model):
    """
    Providing self-managed 'created_at' and 'updated_at' data fields for models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModelMixin(models.Model):
    """
    Adding 'is_deleted' field and providing soft delete functionality for models.
    """

    is_deleted = models.BooleanField(default=False)
    objects = manager.NonDeletedManager()
    all_objects = models.Manager()

    def soft_delete(self):
        """Marks the item as deleted without removing it from the database."""
        self.is_deleted = True
        self.save()

    def restore(self):
        """Restores an item that has been marked as deleted."""
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class OwnerModelMixin(models.Model):
    """
    Providing self-managed 'owner' data field for models.
    """

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class OwnerUserMixin:
    """Add  a new owner based on the current user"""

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DepartmentListFilterMixin:
    """
    Filter the queryset based on the user's department.
    If the user's department is 'Administração', return all objects.
    Otherwise, only return objects related to the user's department.
    """

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if queryset is None:
            queryset = self.model.objects.none()

        queryset = queryset.filter(is_deleted=False)

        if user.departments.filter(name="Administração").exists():
            return queryset

        return queryset.filter(owner__departments__in=user.departments.all()).distinct()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(
                self.request,
                "Você não tem permissão para acessar a página anterior.",
            )
            return redirect(reverse_lazy("home"))
        else:
            return super().handle_no_permission()


class DepartmentPermissionMixin:
    """
    Get the object and checks access permission.
    Allows access if the user is the owner of the object or if the sector is 'Administração'.
    """

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        User = get_user_model()
        try:
            user_profile = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            messages.error(request, "Perfil do usuário não encontrado.")
            return HttpResponseRedirect(reverse("parties:party_list"))

        if not (
            request.user == obj.owner
            or "Administração" in user_profile.departments.values_list("name", flat=True)
        ):
            messages.error(request, "Você não tem permissão para acessar este recurso.")
            return HttpResponseRedirect(reverse("parties:party_list"))

        return super().dispatch(request, *args, **kwargs)
