from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from historys.mixins import HistoricalRecordModelMixin
from django.contrib.contenttypes.models import ContentType


class HistoricalRecord(HistoricalRecordModelMixin):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.content_object} foi {self.change_type} em {self.change_date}, por: {self.owner}"


