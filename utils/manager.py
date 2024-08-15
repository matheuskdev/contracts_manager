from django.db import models


class NonDeletedManager(models.Manager):
    """
    Manager that filters out deleted objects (is_deleted=True).
    """

    def get_queryset(self):
        """Return undeleted items."""
        return super().get_queryset().filter(is_deleted=False)
