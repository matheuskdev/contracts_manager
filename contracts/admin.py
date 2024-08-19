from django.contrib import admin
from .models import Contract
from .forms import ContractForm

class ContractAdmin(admin.ModelAdmin):
    form = ContractForm
    list_display = (
        "number",
        "subject",
        "amount",
        "start_date",
        "end_date",
        "active",
        "folder",
        "department",
        "created_at",
        "updated_at",
    )
    search_fields = ("number", "subject", "description")
    list_filter = (
        "active",
        "lgpd",
        "automatic_renewal",
        "contains_addendum",
        "folder",
        "department",
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
                    "active",
                    "lgpd",
                    "automatic_renewal",
                    "contains_addendum",
                    "parts",
                    "folder",
                    "department",
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
