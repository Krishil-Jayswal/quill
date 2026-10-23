from collections.abc import Callable
from config import settings
from config.enums import (StorageBackendType)
from .backends.MinIOBackendImpl import MinIOStorageBackendImpl
from .base import StorageBackend

StorageBackendConstructor = Callable[[], StorageBackend]

_BACKEND_REGISTRY: dict[
    StorageBackendType,
    StorageBackendConstructor
] = {
    StorageBackendType.MINIO: MinIOStorageBackendImpl
}

class StorageFactory:

    @staticmethod
    def create() -> StorageBackend:
        backend_constructor = _BACKEND_REGISTRY.get(
            settings.STORAGE_BACKEND
        )

        if backend_constructor is None:
            raise ValueError(
                f"Unsupported Storage backend: {settings.STORAGE_BACKEND}"
            )

        return backend_constructor()