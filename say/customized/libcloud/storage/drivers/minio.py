from datetime import timedelta
import io
import os

from libcloud.storage.drivers.minio import MinIOStorageDriver as OrMinIOStorageDriver
from libcloud.storage.types import ContainerDoesNotExistError
from minio.api import Minio


Minio_CDN_URL_EXPIRY_HOURS = float(
    os.getenv("LIBCLOUD_Minio_CDN_URL_EXPIRY_HOURS", "24")
)


class MinIOStorageDriver(OrMinIOStorageDriver):
    supports_s3_multipart_upload = False

    def upload_object_via_stream(
        self,
        iterator,
        container,
        object_name,
        extra=None,
        headers=None,
        ex_storage_class=None,
    ):
        extra = extra or {}
        headers = headers or {}
        headers = {**extra, **headers}
        content_type = headers.get("content_type", {})
        meta_data = headers.get("meta_data", None)

        object_name = object_name.replace("\\", "/")

        the_bytes = bytes()
        for i in iterator:
            the_bytes += i

        length = len(the_bytes)
        data = io.BytesIO(the_bytes)
        return self.client.put_object(
            container.name, object_name, data, length, content_type, meta_data
        )

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
