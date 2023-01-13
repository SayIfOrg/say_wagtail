from typing import TYPE_CHECKING, Type, Union

from libcloud.common.providers import get_driver as _get_provider_driver
from libcloud.storage.providers import DRIVERS as OR_DRIVERS
from libcloud.storage.types import OLD_CONSTANT_TO_NEW_MAPPING, Provider

if TYPE_CHECKING:
    from libcloud.storage.base import StorageDriver

DRIVERS = {
    **OR_DRIVERS,
    Provider.MINIO: ("say.customized.libcloud.storage.drivers.minio", "MinIOStorageDriver"),
}


def get_driver(provider):
    # type: (Union[Provider, str]) -> Type[StorageDriver]
    """
    This customization is in order to pass the new "DRIVERS"
    """
    deprecated_constants = OLD_CONSTANT_TO_NEW_MAPPING
    return _get_provider_driver(
        drivers=DRIVERS, provider=provider, deprecated_constants=deprecated_constants
    )
