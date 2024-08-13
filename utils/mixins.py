from django.db import models
from django.conf import settings
from . import manager


class TimestampMixin(models.Model):
    """
    Providing self-managed 'created_at' and 'updated_at' data fields for models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OwnerMixin(models.Model):
    """
    Providing self-managed 'owner' data field for models.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.owner_id and hasattr(self, '_current_user'):
            self.owner = self._current_user
        super().save(*args, **kwargs)


class SoftDeleteMixin(models.Model):
    """
    Adding 'is_deleted' field and providing soft delete functionality for models.
    """
    is_deleted = models.BooleanField(default=False)
    objects = manager.NonDeletedManager()  
    all_objects = models.Manager()  

    def soft_delete(self):
        """Marks the item as deleted without removing it from the database."""
        self.is_deleted = True
        self.save()

    def restore(self):
        """Restores an item that has been marked as deleted."""
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


