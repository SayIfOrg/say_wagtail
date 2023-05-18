from django.core.checks import Critical, register
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Site

import pydantic

from .storage import (
    AccountStorage,
    Minio2AccountStorage,
    MinioAccountStorage,
    get_storage_by_identity,
)
from .utils import pydantic_validation_err_to_djs


AVAILABLE_STORAGES = [
    MinioAccountStorage,
    Minio2AccountStorage,
]


@register()
def no_duplicate_identity_check(app_configs, **kwargs):
    errors = []

    for i in AVAILABLE_STORAGES:
        try:
            _ = get_storage_by_identity(i.IDENTITY)
        except ImproperlyConfigured as e:
            errors.append(
                Critical(
                    str(e),
                    obj=i,
                    id=f"{__package__}.E001",
                )
            )
    return errors


def available_storage_validator(value: str):
    if value not in [i.IDENTITY for i in AVAILABLE_STORAGES]:
        raise ValidationError(_("This storage is not available."))


class StorageAccountQuerySet(models.QuerySet):
    def for_site(self, site: Site):
        return self.filter(site=site)


class StorageAccount(models.Model):
    IN_SITE_METHOD = "for_site"
    PROVIDE_SITE_METHOD = "set_site"
    objects = StorageAccountQuerySet.as_manager()

    site = models.ForeignKey("wagtailcore.Site", on_delete=models.CASCADE)
    type = models.CharField(max_length=63, validators=[available_storage_validator])
    title = models.CharField(max_length=127)
    args = models.JSONField(default=dict)

    def __init__(self, *args, **kwargs):
        super(StorageAccount, self).__init__(*args, **kwargs)
        self.validate_schema_before_saving = True

    def set_site(self, site):
        self.site_id = site.id

    def get_storage_class(self) -> AccountStorage.__class__:
        return get_storage_by_identity(self.type)

    def get_storage(self) -> AccountStorage:
        return self.get_storage_class()(storage_account=self)

    @classmethod
    def validate_schema(cls, storage: AccountStorage.__class__, args: dict):
        """
        returns the final dict ready to be passed to Storage
        raises ValidationError if not valid
        """
        try:
            return storage.validate_to_obj_args(args).dict()
        except pydantic.ValidationError as e:
            raise pydantic_validation_err_to_djs(e)

    def save(self, *args, **kwargs):
        if self.validate_schema_before_saving:
            self.args = self.validate_schema(
                storage=self.get_storage_class(), args=self.args
            )
        return super(StorageAccount, self).save(*args, **kwargs)
