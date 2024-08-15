from django.contrib import admin

from . import forms
from .models import HistoricalRecord


class HistoryRecordAdmin(admin.ModelAdmin):
    form = forms.HistoricalRecordForm
    list_display = ("content_type", "change_type", "owner")
    search_fields = ("content_type",)
    list_filter = ("content_type", "change_date")
    ordering = ("-change_date",)
    date_hierarchy = "change_date"
    readonly_fields = ("change_date", "content_type", "change_type", "object_id", "owner")
    fieldsets = (
        (None, {"fields": ("content_type", "object_id", "owner")}),
        (
            "Datas",
            {"fields": ("change_date",), "classes": ("collapse",)},
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.owner = request.user
        super().save_model(request, obj, form, change)


admin.site.register(HistoricalRecord, HistoryRecordAdmin)
