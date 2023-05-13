from django.apps import AppConfig


class UtilsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "say.core"

    def ready(self):
        # Register django signals
        from . import signals


        # Register custom image model and its rendition model to "wagtail_grapple"
        from grapple.actions import register_image_model, register_image_rendition_model
        from wagtail.images import get_image_model

        ImageModel = get_image_model()
        register_image_model(ImageModel, "")
        register_image_rendition_model(ImageModel.get_rendition_model(), "") #wagtail-grapple Issue #311
