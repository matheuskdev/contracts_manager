# Generated by Django 5.1 on 2024-09-30 18:17

import contracts.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="contract",
            options={
                "ordering": ["subject"],
                "verbose_name": "Contrato",
                "verbose_name_plural": "Contratos",
            },
        ),
        migrations.AlterField(
            model_name="contract",
            name="pdf",
            field=models.FileField(
                help_text="Faça o upload do arquivo PDF do contrato.",
                upload_to=contracts.models.get_upload_path,
                validators=[
                    django.core.validators.FileExtensionValidator(["pdf", "DOCX", "DOC"])
                ],
            ),
        ),
    ]
