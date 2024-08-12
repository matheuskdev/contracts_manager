from django.db import models

from utils.mixins import TimestampMixin


class Party(TimestampMixin):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name