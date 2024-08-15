from django.apps import AppConfig


class HistoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'historys'

    def ready(self):
        from historys.signals import HistoricalRecordSignal
        from django.apps import apps
        models_to_track = [
            'contracts.Contract',
            'folders.Folder',
            'parts.Part',
         ]
        

        for model_name in models_to_track:
            model = apps.get_model(model_name)
            HistoricalRecordSignal.register_signals(model)
