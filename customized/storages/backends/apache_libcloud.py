from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.deconstruct import deconstructible

from libcloud.storage.types import Provider
from storages.backends.apache_libcloud import LibCloudStorage

from customized.libcloud.storage.providers import get_driver


@deconstructible
class LibCloudStorage(LibCloudStorage):
    """
    This overriding is just for passing "extra" kwargs to drivers
    """

    def __init__(self, provider_name=None, option=None):
        if provider_name is None:
            provider_name = getattr(settings, "DEFAULT_LIBCLOUD_PROVIDER", "default")

        self.provider = settings.LIBCLOUD_PROVIDERS.get(provider_name)
        if not self.provider:
            raise ImproperlyConfigured(
                "LIBCLOUD_PROVIDERS %s not defined or invalid" % provider_name
            )
        extra_kwargs = {}
        if "region" in self.provider:
            extra_kwargs["region"] = self.provider["region"]
        # Used by the GoogleStorageDriver
        if "project" in self.provider:
            extra_kwargs["project"] = self.provider["project"]
        # All this is becuase of this two line #
        if "extra" in self.provider:
            extra_kwargs.update(**self.provider["extra"])
        # # # # # # # # # # # # # # # # # # # # #
        try:
            provider_type = self.provider["type"]
            if isinstance(provider_type, str):
                module_path, tag = provider_type.rsplit(".", 1)
                if module_path != "libcloud.storage.types.Provider":
                    raise ValueError("Invalid module path")
                provider_type = getattr(Provider, tag)

            Driver = get_driver(provider_type)
            self.driver = Driver(
                self.provider["user"], self.provider["key"], **extra_kwargs
            )
        except Exception as e:
            raise ImproperlyConfigured(
                "Unable to create libcloud driver type %s: %s"
                % (self.provider.get("type"), e)
            )
        self.bucket = self.provider["bucket"]  # Limit to one container
