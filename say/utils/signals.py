from django.dispatch import receiver

from say.dynamic_storage.models import DynamicFieldFile
from say.dynamic_storage.signals import pre_dynamic_file_save
from say.dynamic_storage.storage import Storage

from . import models


@receiver(pre_dynamic_file_save, sender=models.DSWRendition)
def image_rendition_same_storage(
    instance: models.DSWRendition,
    field_file: DynamicFieldFile,
    to_storage: Storage,
    *args,
    **kwargs
):
    """
    Save rendition to the same storage as it's related image
    except a storage is specified for it explicitly
    """
    if not to_storage:
        field_file.destination_storage = instance.image.file.storage
