# Generated by Django 5.1 on 2024-08-15 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0002_alter_contract_pdf"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contract",
            old_name="parties",
            new_name="parts",
        ),
    ]
