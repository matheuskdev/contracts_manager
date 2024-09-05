from abc import ABC

from django.db.models.signals import post_delete, post_save

from historys.models import HistoricalRecord


class HistoricalRecordSignal(ABC):

    @staticmethod
    def register_signals(model):
        """Registers signals for the given model."""
        post_save.connect(HistoricalRecordSignal._handle_save, sender=model)
        post_delete.connect(HistoricalRecordSignal._handle_delete, sender=model)

    @staticmethod
    def _handle_save(sender, instance, created, **kwargs):
        """Handles save (create or update) events."""
        change_type =  "Deletion" if instance.is_deleted else ("Creation" if created else "Update")
        HistoricalRecordSignal._create_historical_record(instance, change_type)

    @staticmethod
    def _handle_delete(sender, instance, **kwargs):
        """Handles delete events."""
        HistoricalRecordSignal._create_historical_record(instance, "Deletion Total")

    @staticmethod
    def _create_historical_record(instance, change_type):
        """Creates a historical record."""
        HistoricalRecord.objects.create(
            content_object=instance,
            change_type=change_type,
            owner=getattr(instance, "owner", None),
        )
