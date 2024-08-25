from django.contrib import admin

from . import forms
from .models import Evaluation


class EvaluationAdmin(admin.ModelAdmin):
    form = forms.EvaluationForm
    list_display = ("contract", "rating", "comments", "created_at", "updated_at")
    list_filter = ("rating", "contract")
    search_fields = ("comments",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("rating", "comments")}),
        (
            "Datas",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.owner = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Evaluation, EvaluationAdmin)
