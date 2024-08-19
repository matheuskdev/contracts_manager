# Generated by Django 5.1 on 2024-08-19 15:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contracts", "0003_rename_parties_contract_parts"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Evaluation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "rating",
                    models.PositiveIntegerField(
                        choices=[
                            (1, "Péssimo"),
                            (2, "Ruim"),
                            (3, "Aceitável"),
                            (4, "Bom"),
                            (5, "Ótimo"),
                        ],
                        help_text="Classificação da avaliação",
                    ),
                ),
                (
                    "comments",
                    models.TextField(
                        blank=True, help_text="Comentários adicionais sobre a avaliação"
                    ),
                ),
                (
                    "contract",
                    models.ForeignKey(
                        help_text="Contrato associado à avaliação",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evaluations",
                        to="contracts.contract",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Avaliação",
                "verbose_name_plural": "Avaliações",
                "ordering": ["rating"],
                "indexes": [
                    models.Index(fields=["rating"], name="evaluations_rating_660477_idx")
                ],
            },
        ),
    ]
