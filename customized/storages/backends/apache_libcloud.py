from django.conf import settings
from django.contrib.staticfiles.storage import ManifestFilesMixin
from django.core.exceptions import ImproperlyConfigured
from django.utils.deconstruct import deconstructible

from libcloud.storage.types import Provider
from storages.backends.apache_libcloud import LibCloudStorage
from whitenoise.media_types import MediaTypes

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

    def _read(self, name):
        obj = self._get_object(name)
        # https://github.com/jschneier/django-storages/issues/1190 #
        if obj is None:
            raise FileNotFoundError(f"{name} does not exist.")
        #    #    #    #    #    #    #    #    #    #    #    #
        # I have no idea what is that about #
        # TOFIX : we should be able to read chunk by chunk
        # return next(self.driver.download_object_as_stream(obj, obj.size))
        #   #   #   #   #   #   #   #   #  #
        bs = bytes()
        for i in self.driver.download_object_as_stream(obj, obj.size):
            bs += i
        return bs


class LibCloudStaticStorage(LibCloudStorage):
    """Querystring auth must be disabled so that url() returns a consistent output."""

    querystring_auth = False

    def __init__(self, *args, provider_name=None, **kwargs):
        if provider_name is None:
            provider_name = getattr(
                settings, "DEFAULT_LIBCLOUD_STATIC_PROVIDER", "default"
            )
        super(LibCloudStaticStorage, self).__init__(
            *args, provider_name=provider_name, **kwargs
        )

    def _save(self, name, file):
        # It's essential for static assets to be type known by browsers #
        content_type = MediaTypes().get_type(name)
        extra = {"content_type": content_type}
        #    #    #    #    #    #    #    #    #    #    #    #    #
        self.driver.upload_object_via_stream(
            iter(file), self._get_bucket(), name, extra
        )
        return name

    def url(self, name):
        """
        It should not cause any request in order to get static assets,
        and also it comes handy for "LibCloudManifestStaticStorage" because "ManifestFilesMixin"
        tries to get the url of hashed file before copping it to storage
        """
        object_path = "{}/{}".format(self.bucket, name)
        conn = self.driver.connection
        base_url = (
            "https://" if conn.secure else "http://"
        ) + f"{conn.host}:{conn.port}"
        return f"{base_url}/{object_path}"


class LibCloudManifestStaticStorage(ManifestFilesMixin, LibCloudStaticStorage):
    # It might not work properly
    """Copy the file before saving for compatibility with ManifestFilesMixin
    which does not play nicely with boto3 automatically closing the file.

    See: https://github.com/boto/s3transfer/issues/80#issuecomment-562356142
    """

    def __init__(self, *args, **kwargs):
        manifest_storage = LibCloudStaticStorage()
        super(LibCloudManifestStaticStorage, self).__init__(
            *args, manifest_storage=manifest_storage, **kwargs
        )

    def hashed_name(self, *args, **kwargs):
        result = super(LibCloudManifestStaticStorage, self).hashed_name(*args, **kwargs)
        # Don't know why but result contains both "/" and "\"
        return result.replace("\\", "/")
