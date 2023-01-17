from django.apps import AppConfig


class UtilsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "say.utils"

    def ready(self):
        from . import signals
