from django.dispatch import receiver

from dynamic_storage.models import DynamicFieldFile
from dynamic_storage.signals import pre_dynamic_file_save
from dynamic_storage.storage import DynamicStorage

from . import models


@receiver(pre_dynamic_file_save, sender=models.DSWRendition)
def image_rendition_same_storage(
    instance: models.DSWRendition,
    field_file: DynamicFieldFile,
    to_storage: DynamicStorage,
    *args,
    **kwargs
):
    """
    Save rendition to the same storage as it's related image
    except a storage is specified for it explicitly
    """
    if not to_storage:
        field_file.destination_storage = instance.image.file.storage
