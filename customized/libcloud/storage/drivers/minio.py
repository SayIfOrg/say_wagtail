import os

from libcloud.storage.drivers.minio import MinIOStorageDriver as OrMinIOStorageDriver
from libcloud.storage.types import ContainerDoesNotExistError
from minio.api import Minio


from datetime import datetime, timedelta


Minio_CDN_URL_EXPIRY_HOURS = float(
    os.getenv("LIBCLOUD_Minio_CDN_URL_EXPIRY_HOURS", "24")
)


class MinIOStorageDriver(OrMinIOStorageDriver):
    def __init__(self, *args, auto_create_container=False, **kwargs):
        super(MinIOStorageDriver, self).__init__(*args, **kwargs)
        self.auto_create_container = auto_create_container
        self.client = Minio(
            f"{self.connection.host}:{self.connection.port}",
            access_key=self.key,
            secret_key=self.secret,
            secure=False,
        )

    # def get_container_cdn_url(self, container):
    #     pass
    #
    # def enable_container_cdn(self, container):
    #     pass
    #
    # def enable_object_cdn(self, obj):
    #     pass

    def get_object_cdn_url(self, obj, ex_expiry=Minio_CDN_URL_EXPIRY_HOURS):

        """
        Return a "presigned URL"

        :param obj: Object instance.
        :type  obj: :class:`Object`

        :param ex_expiry: The number of hours after which the URL expires.
                          Defaults to 24 hours or the value of the environment
                          variable "LIBCLOUD_S3_STORAGE_CDN_URL_EXPIRY_HOURS",
                          if set.
        :type  ex_expiry: ``float``

        :return: Presigned URL for the object.
        :rtype: ``str``
        """

        # assemble data for the request we want to pre-sign
        # see: https://min.io/docs/minio/linux/developers/python
        #       /API.html#get-presigned-url-method-bucket-name-object-name-
        #       expires-timedelta-days-7-response-headers-none-request-date-none-
        #       version-id-none-extra-query-params-none
        return self.client.get_presigned_url(
            "GET",
            obj.container.name,
            obj.name,
            expires=timedelta(hours=ex_expiry),
        )

    def get_container(self, container_name):
        try:
            return super(MinIOStorageDriver, self).get_container(container_name)
        except ContainerDoesNotExistError:
            if not self.auto_create_container:
                raise
            return self.create_container(container_name)
