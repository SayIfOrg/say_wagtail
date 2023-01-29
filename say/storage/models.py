from django.core.checks import register, Critical
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.db import models
from django.utils.translation import gettext_lazy as _

from .storage import (
    MinioAccountStorage,
    Minio2AccountStorage,
    get_storage_by_identity,
    AccountStorage,
)

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


class StorageAccount(models.Model):
    site = models.ForeignKey("wagtailcore.Site", on_delete=models.CASCADE)
    type = models.CharField(max_length=63, validators=[available_storage_validator])
    title = models.CharField(max_length=127)
    args = models.JSONField(default=dict)

    def get_storage_class(self) -> AccountStorage.__class__:
        return get_storage_by_identity(self.type)

    def get_storage(self) -> AccountStorage:
        return self.get_storage_class()(storage_account=self)

    def check_args(self):
        SelectedStorage = get_storage_by_identity(self.type)
        self.args = SelectedStorage.validate_to_obj_args(self.args).dict()

    def save(self, *args, **kwargs):
        try:
            self.check_args()
        except ValidationError:
            raise
        return super(StorageAccount, self).save(*args, **kwargs)
