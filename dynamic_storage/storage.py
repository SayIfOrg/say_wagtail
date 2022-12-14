from __future__ import annotations

from abc import abstractmethod, ABC
import importlib
from typing import Dict, Any, Callable

from django.core.files.storage import Storage as BaseStorage

# {"import_path": str, "constructor": dict}
prob = Dict[str, Any]


class Storage(ABC, BaseStorage):
    @abstractmethod
    def init_params(self) -> dict:
        """parameters for calling __init__ on storage class"""
        ...

    def uninit(self) -> prob:
        """get the required properties for future initialization"""
        return {
            "import_path": f"{self.__class__.__module__}.{self.__class__.__qualname__}",
            "constructor": self.init_params(),
        }

    @classmethod
    def init(cls, probs: prob) -> Storage:
        """initialize storage"""
        module_name = ".".join(probs["import_path"].split(".")[:-1])
        class_name = probs["import_path"].split(".")[-1]
        StorageClass: Callable = getattr(
            importlib.import_module(module_name), class_name
        )
        return StorageClass(**probs["constructor"])
