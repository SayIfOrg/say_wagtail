from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.images import models as wagtail_models

from dynamic_storage.models import DynamicImageField


class DSWAbstractImage(wagtail_models.AbstractImage):
    """Dynamic Storage Wagtail Abstract Image"""

    file = DynamicImageField(
        verbose_name=_("file"),
        upload_to=wagtail_models.get_upload_to,
        width_field="width",
        height_field="height",
    )

    class Meta:
        abstract = True


class DSWImage(DSWAbstractImage):
    """Dynamic Storage Wagtail Image"""

    admin_form_fields = wagtail_models.Image.admin_form_fields

    class Meta(DSWAbstractImage.Meta):
        verbose_name = _("image")
        verbose_name_plural = _("images")
        permissions = [
            ("choose_image", "Can choose image"),
        ]


class DSWRendition(wagtail_models.AbstractRendition):
    """Dynamic Storage Wagtail Rendition"""
    image = models.ForeignKey(
        DSWImage, related_name="renditions", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
