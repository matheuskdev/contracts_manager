from django.db import models

from contracts.models import Contract
from utils import mixins

RATING_CHOICES = [
    (1, "Péssimo"),
    (2, "Ruim"),
    (3, "Aceitável"),
    (4, "Bom"),
    (5, "Ótimo"),
]


class Evaluation(
    mixins.TimestampModelMixin, mixins.OwnerModelMixin, mixins.SoftDeleteModelMixin
):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="evaluations",
        help_text="Contrato associado à avaliação",
    )
    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES, help_text="Classificação da avaliação"
    )
    comments = models.TextField(
        blank=True, help_text="Comentários adicionais sobre a avaliação"
    )

    class Meta:
        ordering = ["rating"]
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        indexes = [
            models.Index(fields=["rating"]),
        ]

    def __str__(self):
        return f"Avaliação {self.get_rating_display()} para o Contrato {self.contract}"
