from django.contrib import admin

from . import forms
from .models import Addendum


class AddendumAdmin(admin.ModelAdmin):
    form = forms.AddendumForm
    list_display = (
        "title",
        "created_at",
        "updated_at",
        "owner",
    )
    search_fields = ("title",)
    list_filter = ("title", "created_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title",)}),
        (
            "Datas",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.owner = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Addendum, AddendumAdmin)
