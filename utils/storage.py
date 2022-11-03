from django.utils.deconstruct import deconstructible

from customized.storages.backends.apache_libcloud import LibCloudStorage
from dynamic_storage.storage import Storage as DynamicStorage


@deconstructible
class DynamicLibCloudStorage(DynamicStorage, LibCloudStorage):
    def __init__(self, provider_name=None, option=None):
        super(DynamicLibCloudStorage, self).__init__(
            provider_name=provider_name, option=option
        )
        self.provider_name = provider_name

    def init_params(self) -> dict:
        return {"provider_name": self.provider_name}
