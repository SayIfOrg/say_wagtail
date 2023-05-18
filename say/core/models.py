from contextlib import contextmanager

from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.documents import models as wagtail_document_models
from wagtail.images import models as wagtail_image_models
from wagtail.images.models import (
    SourceImageIOError,
    WagtailImageField,
    WagtailImageFieldFile,
    get_rendition_storage,
    get_rendition_upload_to,
)

from grapple.models import GraphQLImage, GraphQLInt, GraphQLString

from say.dynamic_storage.models import (
    DynamicFileField,
    DynamicImageField,
    DynamicImageFieldFile,
)


class Monkey:
    @contextmanager
    def open_file(self):
        """
        This is #monkey patch due to https://github.com/wagtail/wagtail/issues/9904
        and should transfer to the package itself
        """

        # Open file if it is closed
        close_file = False
        try:
            image_file = self.file

            if self.file.closed:
                # Reopen the file
                if self.is_stored_locally():
                    self.file.open("rb")
                else:
                    # Some external storage backends don't allow reopening
                    # the file. Get a fresh file instance. #1397

                    #       #       #       #       #       #       #       #
                    # storage = self._meta.get_field("file").storage wronggg
                    storage = self.file.storage  # right
                    #       #       #       #       #       #       #

                    image_file = storage.open(self.file.name, "rb")

                close_file = True
        except IOError as e:
            # re-throw this as a SourceImageIOError so that calling code can distinguish
            # these from IOErrors elsewhere in the process
            raise SourceImageIOError(str(e))

        # Seek to beginning
        image_file.seek(0)

        try:
            yield image_file
        finally:
            if close_file:
                image_file.close()


class DynamicWagtailImageFieldFile(WagtailImageFieldFile, DynamicImageFieldFile):
    pass


class DynamicWagtailImageField(WagtailImageField, DynamicImageField):
    attr_class = DynamicWagtailImageFieldFile


class DSWAbstractImage(Monkey, wagtail_image_models.AbstractImage):
    """Dynamic Storage Wagtail Abstract Image"""

    file = DynamicWagtailImageField(
        verbose_name=_("file"),
        upload_to=wagtail_image_models.get_upload_to,
        width_field="width",
        height_field="height",
    )

    class Meta(wagtail_image_models.AbstractImage.Meta):
        abstract = True


class DSWImage(DSWAbstractImage):
    """Dynamic Storage Wagtail Image"""

    admin_form_fields = wagtail_image_models.Image.admin_form_fields + ("storage",)

    class Meta(DSWAbstractImage.Meta):
        verbose_name = _("image")
        verbose_name_plural = _("images")
        permissions = [
            ("choose_image", "Can choose image"),
        ]


class DSWRendition(Monkey, wagtail_image_models.AbstractRendition):
    """Dynamic Storage Wagtail Rendition"""

    file = DynamicWagtailImageField(
        upload_to=get_rendition_upload_to,
        storage=get_rendition_storage,
        width_field="width",
        height_field="height",
    )

    image = models.ForeignKey(
        DSWImage, related_name="renditions", on_delete=models.CASCADE
    )

    class Meta(wagtail_image_models.AbstractImage.Meta):
        unique_together = (("image", "filter_spec", "focal_point_key"),)

    graphql_fields = (
        GraphQLString("custom_rendition_property", required=True),
        GraphQLInt("id", required=True),
        GraphQLString("url", required=True),
        GraphQLString("width", required=True),
        GraphQLString("height", required=True),
        GraphQLImage("image", required=True),
        GraphQLString("file", required=True),
    )


class DSWAbstractDocument(wagtail_document_models.AbstractDocument):
    """Dynamic Storage Wagtail Abstract Document"""

    file = DynamicFileField(upload_to="documents", verbose_name=_("file"))

    class Meta(wagtail_document_models.AbstractDocument.Meta):
        abstract = True


class DSWDocument(DSWAbstractDocument):
    """Dynamic Storage Wagtail Document"""

    admin_form_fields = wagtail_document_models.Document.admin_form_fields + (
        "storage",
    )

    class Meta(DSWAbstractDocument.Meta):
        permissions = [
            ("choose_document", "Can choose document"),
        ]
