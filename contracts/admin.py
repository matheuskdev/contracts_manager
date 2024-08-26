from django.contrib import admin

from .forms import ContractForm
from .models import Contract


class ContractAdmin(admin.ModelAdmin):
    form = ContractForm
    list_display = (
        "number",
        "subject",
        "amount",
        "start_date",
        "end_date",
        "status",
        "contract_type",
        "folder",
        "department",
        "owner",
        "created_at",
        "updated_at",
    )
    search_fields = ("number", "subject", "description")
    list_filter = (
        "lgpd",
        "owner",
        "automatic_renewal",
        "contains_addendum",
        "folder",
        "department",
        "status",
        "contract_type",
        "created_at",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at", "slug")
    fieldsets = (
        (None, {"fields": ("number", "subject", "description", "amount", "pdf")}),
        (
            "Datas do Contrato",
            {"fields": ("start_date", "end_date"), "classes": ("",)},
        ),
        (
            "Detalhes do Contrato",
            {
                "fields": (
                    "lgpd",
                    "owner",
                    "automatic_renewal",
                    "contains_addendum",
                    "parts",
                    "folder",
                    "department",
                    "status",
                    "contract_type",
                )
            },
        ),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at", "slug"), "classes": ("collapse",)},
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.owner = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Contract, ContractAdmin)
