import os
from datetime import datetime
from django.db import models
from django.core.validators import FileExtensionValidator
from contracts.models import Contract
from utils import mixins


def get_upload_path(instance, filename):
    folder_name = instance.contract.folders.name
    date = datetime.now().strftime("%Y/%m/%d")
    return os.path.join('addemdums/pdfs/', folder_name, date, filename)


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
    new_end_date = models.DateField(
        null=True, blank=True, help_text='Nova data final para o contrato'
    )
    document = models.FileField(
        upload_to=get_upload_path,
        validators=[FileExtensionValidator(["pdf", "DOCX", "DOC"])],
        help_text="Faça o upload do arquivo PDF do Aditivo.",
        default='addendums/default.pdf'
    )


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
