from django.db import models

class TimestampMixin(models.Model):
    """
    Providing at models self-managed 'created_at' and 'updated_at data fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True