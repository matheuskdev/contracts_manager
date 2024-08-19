from django.apps import AppConfig


class ExpirationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "expirations"

    def ready(self):
        from .signals import ExpiryNotifications
        ExpiryNotifications.setup_notifications()