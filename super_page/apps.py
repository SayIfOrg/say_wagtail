from django.apps import AppConfig


class SuperPageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "super_page"

    def ready(self):
        from . import signals
