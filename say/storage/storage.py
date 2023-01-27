from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from django.core.exceptions import ImproperlyConfigured, ValidationError as DJValidationError

from pydantic import BaseModel, conint, constr, ValidationError

from say.customized.libcloud.storage.drivers.minio import MinIOStorageDriver
from say.dynamic_storage.storage import Storage as DynamicStorage
from say.utils.storage import LibCloudStorage


class StorageDoesNotExists(Exception):
    pass


class AbstractBaseStorage(DynamicStorage):
    IDENTITY: str

    @abstractmethod
    def __init__(
        self, /, storage_account_id: Optional[int] = None, args: Optional[dict] = None
    ):
        ...

    def init_params(self) -> dict:
        return {"storage_account_id": self.storage_account_id}

    @classmethod
    @abstractmethod
    def title(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def validate_to_obj_args(cls, args: dict) -> object:
        ...

    @property
    def storage_account_id(self):
        return self._storage_account_id

    def get_storage_account(self):
        if not self._storage_account:
            self._storage_account = StorageAccount.objects.get(
                pk=self.storage_account_id
            )
        return self._storage_account


class MinioStorage(AbstractBaseStorage, LibCloudStorage):
    IDENTITY = "libcloud_minio"

    class Schema(BaseModel):
        key: str
        secret: str
        host: str
        port: conint(gt=79, lt=99999)
        secure: bool
        bucket: constr(min_length=1, max_length=127)
        auto_create_container: bool

    def __init__(
        self, /, storage_account_id: Optional[int] = None, storage_account=None
    ):
        self.provider = dict()
        self.provider["type"] = "libcloud.storage.types.Provider.MINIO"

        assert (storage_account_id or storage_account) and not (storage_account_id and storage_account)
        from .models import StorageAccount

        args = (
            storage_account.args
            if storage_account
            else StorageAccount.objects.only("args").get(pk=storage_account_id).args
        )
        args = self.validate_to_obj_args(args)

        self.driver = MinIOStorageDriver(
            args.key,
            secret=args.secret,
            host=args.host,
            port=args.port,
            secure=args.secure,
            auto_create_container=args.auto_create_container,
        )
        self._bucket = args.bucket
        self._storage_account_id = storage_account_id or storage_account.pk
        self._storage_account = None

    @property
    def bucket(self):
        return self._bucket

    @classmethod
    def title(cls) -> str:
        return "First LibCloud Minio"

    @classmethod
    def validate_to_obj_args(cls, args: dict) -> Schema:
        try:
            return cls.Schema(**args)
        except ValidationError as e:
            raise DJValidationError(str(e))

class Minio2Storage(MinioStorage):
    IDENTITY = "libcloud_minio2"

    @classmethod
    def title(cls):
        return "fdsf"


def get_storage_by_identity(identity: str) -> type(AbstractBaseStorage):
    from say.storage.models import AVAILABLE_STORAGES

    filtered = [i for i in AVAILABLE_STORAGES if i.IDENTITY == identity]
    if len(filtered) == 0:
        raise StorageDoesNotExists
    elif len(filtered) == 1:
        return filtered[0]

    raise ImproperlyConfigured(f'"identity" for {str(filtered)} clashes')
