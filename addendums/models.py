from django.db import models

from contracts.models import Contract
from utils import mixins


class Addendum(
    mixins.SoftDeleteModelMixin, mixins.TimestampModelMixin, mixins.OwnerModelMixin
):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="addendums",
        help_text="Contrato associado ao aditivo",
    )
    title = models.CharField(max_length=255, help_text="Tiulo do Aditivo")
    description = models.TextField(
        null=True, blank=True, help_text="Descrição do Aditivo"
    )
    effective_date = models.DateField(help_text="Data Inicial do Aditivo")

    class Meta:
        ordering = ["title"]
        verbose_name = "Aditivo"
        verbose_name_plural = "Aditivos"
        indexes = [
            models.Index(fields=["title"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["title"], name="unique_addendums_title"),
        ]

    def __str__(self):
        return f"Aditivo para: {self.contract} - {self.title}"
