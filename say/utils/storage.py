from django.utils.deconstruct import deconstructible

from storages.backends.apache_libcloud import LibCloudFile as BaseLibCloudFile

from say.customized.storages.backends.apache_libcloud import (
    LibCloudStorage as BaseLibCloudStorage,
)
from say.dynamic_storage.storage import DynamicStorageMixin


@deconstructible
class LibCloudStorage(BaseLibCloudStorage):
    def _open(self, name, mode="rb"):
        remote_file = LibCloudFile(name, self, mode=mode)
        return remote_file


class LibCloudFile(BaseLibCloudFile):
    def open(self, mode=None):
        """Reopenable LibCloudFile"""
        if self.closed:
            self.file = self._storage.open(self.name, mode=mode)
        else:
            super(LibCloudFile, self).open(mode=mode)
        return self


@deconstructible
class DynamicLibCloudStorage(DynamicStorageMixin, LibCloudStorage):
    def __init__(self, provider_name=None, option=None):
        super(DynamicLibCloudStorage, self).__init__(
            provider_name=provider_name, option=option
        )
        self.provider_name = provider_name

    def init_params(self) -> dict:
        return {"provider_name": self.provider_name}
