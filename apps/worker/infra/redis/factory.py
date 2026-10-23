from collections.abc import Callable
from config import settings
from config.enums import RedisBackendType
from .backends.RedisBackendImpl import RedisBackendImpl
from .base import RedisBackend

RedisBackendConstructor = Callable[[], RedisBackend]

_BACKEND_REGISTRY: dict[
    RedisBackendType,
    RedisBackendConstructor,
] = {
    RedisBackendType.REDIS: RedisBackendImpl,
}

class RedisFactory:

    @staticmethod
    def create() -> RedisBackend:
        backend_constructor = _BACKEND_REGISTRY.get(
            settings.REDIS_BACKEND
        )

        if backend_constructor is None:
            raise ValueError(
                f"Unsupported Redis backend: {settings.REDIS_BACKEND}"
            )

        return backend_constructor()