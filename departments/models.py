from django.db import models

from utils import mixins


class Department(
    mixins.TimestampModelMixin,
    mixins.OwnerModelMixin,
    mixins.SoftDeleteModelMixin,
):
    """
    Model representing a Department
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Nome do departamento. Deve ser único.",
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Descrição do departamento. Opcional.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        indexes = [
            models.Index(fields=["name"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_department_name"),
        ]

    def __str__(self) -> str:
        return self.name
