from django.db import models


class NonDeletedManager(models.Manager):
    def get_queryset(self):
        """Return undeleted items."""
        return super().get_queryset().filter(is_deleted=False)
