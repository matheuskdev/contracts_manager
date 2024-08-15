from django.db import models

from utils import mixins, regex


class Part(
    mixins.SoftDeleteModelMixin,
    mixins.TimestampModelMixin,
    mixins.OwnerModelMixin
):
    """
    Model representing a Part.
    """

    name = models.CharField(
        unique=True, max_length=255, help_text="Nome da parte. Deve ser único."
    )
    address = models.CharField(max_length=255, help_text="Endereço da parte.")
    email = models.EmailField(null=True, blank=True, help_text="Email da parte.")
    phone = models.CharField(
        max_length=20,
        validators=[regex.phone_regex],
        help_text="Número de telefone da parte.",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Parte"
        verbose_name_plural = "Partes"
        indexes = [
            models.Index(fields=["name"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_part_name"),
        ]

    def __str__(self):
        return self.name