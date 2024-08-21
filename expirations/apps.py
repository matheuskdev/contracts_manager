from django.apps import AppConfig


class ExpirationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "expirations"

    def ready(self):
        from .signals import ContractExpirationNotification45, ContractExpirationNotification30
        ContractExpirationNotification45.register_signal()
        ContractExpirationNotification30.register_signal()