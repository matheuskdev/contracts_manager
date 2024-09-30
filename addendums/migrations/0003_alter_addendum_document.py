# Generated by Django 5.1 on 2024-09-30 19:28

import addendums.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("addendums", "0002_alter_addendum_options_addendum_document_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="addendum",
            name="document",
            field=models.FileField(
                default="addendums/default.pdf",
                help_text="Faça o upload do arquivo PDF do Aditivo.",
                upload_to=addendums.models.get_upload_path,
                validators=[
                    django.core.validators.FileExtensionValidator(["pdf", "DOCX", "DOC"])
                ],
            ),
        ),
    ]
