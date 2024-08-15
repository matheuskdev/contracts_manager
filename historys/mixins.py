from utils import mixins 
from django.db import models


class HistoricalRecordModelMixin(mixins.OwnerModelMixin):
    change_date = models.DateTimeField(auto_now_add=True)
    change_type = models.CharField(max_length=20)

    class Meta:
        abstract = True
