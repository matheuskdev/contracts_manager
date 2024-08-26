import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db import models
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
logger = logging.getLogger(__name__)
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
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class SoftDeleteViewMixin:
    """
    Mixin that overrides the delete method to perform a soft delete.
    """

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


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

        if hasattr(self.model, 'department'):
            return queryset.filter(
                Q(owner=user) | 
                Q(owner__departments__in=user.departments.all()) | 
                Q(department__in=user.departments.all())
            ).distinct()

        return queryset.filter(
            Q(owner=user) | 
            Q(owner__departments__in=user.departments.all()) 
        ).distinct()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(
                self.request,
                "Você não tem permissão para acessar a página anterior. Faça seu login!",
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
            return HttpResponseRedirect(reverse("home"))

        is_owner = request.user == obj.owner
        is_department_admin =  "Administração" in user_profile.departments.values_list("name", flat=True)
        is_in_department = hasattr(self.model, 'department') and \
                        str(obj.department) in request.user.departments.values_list("name", flat=True)
        is_department_in_owner_dep = request.user.departments.values_list in obj.owner.departments.values_list("name", flat=True)

        if not ( is_owner or is_department_admin or is_in_department or is_department_in_owner_dep):
            messages.error(request, "Você não tem nível de permissão para acessar este recurso.")
            return HttpResponseRedirect(reverse("home"))

        return super().dispatch(request, *args, **kwargs)
