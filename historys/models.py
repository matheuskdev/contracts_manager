from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from historys.mixins import HistoricalRecordModelMixin


class HistoricalRecord(HistoricalRecordModelMixin):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["content_type"]
        verbose_name = "Histórico"
        verbose_name_plural = "Históricos"
        indexes = [
            models.Index(fields=["content_type"]),
        ]

    def __str__(self):
        return f"{self.content_object} foi {self.change_type} em {self.change_date}, por: {self.owner}"
