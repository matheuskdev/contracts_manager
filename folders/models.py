from django.db import models

from utils import mixins


class Folder(
    mixins.TimestampModelMixin,
    mixins.OwnerModelMixin,
    mixins.SoftDeleteModelMixin,
):
    """
    Model representing a Folder
    """

    name = models.CharField(
        unique=True, max_length=255, help_text="Nome da pasta. Deve ser único."
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Pasta"
        verbose_name_plural = "Pastas"
        indexes = [
            models.Index(fields=["name"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_folder_name"),
        ]

    def __str__(self):
        return self.name
