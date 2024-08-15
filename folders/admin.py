from django.contrib import admin

from . import forms
from .models import Folder


class FolderAdmin(admin.ModelAdmin):
    form = forms.FolderForm
    list_display = (
        "name",
        "created_at",
        "updated_at",
        "owner",
    )
    search_fields = ("name",)
    list_filter = ("name", "created_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name",)}),
        (
            "Datas",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.owner = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Folder, FolderAdmin)
