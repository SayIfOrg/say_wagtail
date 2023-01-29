from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from django.core.exceptions import (
    ImproperlyConfigured,
    ValidationError as DJValidationError,
)
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

from pydantic import BaseModel, conint, constr, ValidationError

from say.dynamic_storage.storage import DynamicStorageMixin
from say.utils.storage import MinioStorage


class StorageDoesNotExists(Exception):
    pass


class AccountStorageMixin(DynamicStorageMixin, ABC):
    IDENTITY: str
    Schema: BaseModel

    def __init__(
        self, /, storage_account_id: Optional[int] = None, storage_account=None
    ):
        assert (storage_account_id or storage_account) and not (
            storage_account_id and storage_account
        )
        from .models import StorageAccount

        args = (
            storage_account.args
            if storage_account
            else StorageAccount.objects.only("args").get(pk=storage_account_id).args
        )
        args = self.validate_to_obj_args(args)

        self.get_the_storage_class().__init__(self, **args.dict())
        self._storage_account_id = storage_account_id or storage_account.pk
        self._storage_account: Optional[StorageAccount] = None

    @classmethod
    def get_the_storage_class(cls) -> type(Storage):
        try:
            return [i for i in cls.__bases__ if issubclass(i, Storage)][-1]
        except IndexError:
            raise Exception("Last base of this class is not a DjStorage")

    def init_params(self) -> dict:
        return {"storage_account_id": self.storage_account_id}

    @classmethod
    def validate_to_obj_args(cls, args: dict) -> BaseModel:
        try:
            return cls.Schema(**args)
        except ValidationError as e:
            raise DJValidationError(str(e))

    @property
    def storage_account_id(self):
        return self._storage_account_id

    def get_storage_account(self):
        if not self._storage_account:
            from say.storage.models import StorageAccount

            self._storage_account = StorageAccount.objects.get(
                pk=self.storage_account_id
            )
        return self._storage_account

    @classmethod
    @abstractmethod
    def title(cls) -> str:
        ...


class AccountStorage(AccountStorageMixin, Storage):
    ...


@deconstructible
class MinioAccountStorage(AccountStorageMixin, MinioStorage):
    IDENTITY = "libcloud_minio"

    class Schema(BaseModel):
        key: str
        secret: str
        host: str
        port: conint(gt=79, lt=99999)
        secure: bool
        bucket: constr(min_length=3, max_length=127)
        auto_create_container: bool

    @classmethod
    def title(cls) -> str:
        return "First LibCloud Minio"


class Minio2AccountStorage(MinioAccountStorage):
    IDENTITY = "libcloud_minio2"

    @classmethod
    def title(cls):
        return "fdsf"


def get_storage_by_identity(identity: str) -> type(AccountStorage):
    from say.storage.models import AVAILABLE_STORAGES

    filtered = [i for i in AVAILABLE_STORAGES if i.IDENTITY == identity]
    if len(filtered) == 0:
        raise StorageDoesNotExists
    elif len(filtered) == 1:
        return filtered[0]

    raise ImproperlyConfigured(f'"identity" for {str(filtered)} clashes')
