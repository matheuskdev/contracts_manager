# Generated by Django 5.1 on 2024-09-30 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("folders", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="folder",
            options={
                "ordering": ["name"],
                "verbose_name": "Pasta",
                "verbose_name_plural": "Pastas",
            },
        ),
    ]
