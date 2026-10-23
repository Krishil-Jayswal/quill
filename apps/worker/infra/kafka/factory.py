from collections.abc import Callable
from config import settings
from config.enums import KafkaBackendType
from .backends.KafkaBackendImpl import KafkaBackendImpl
from .base import KafkaBackend

KafkaBackendConstructor = Callable[[], KafkaBackend]

_BACKEND_REGISTRY: dict[
    KafkaBackendType,
    KafkaBackendConstructor,
] = {
    KafkaBackendType.KAFKA: KafkaBackendImpl,
}

class KafkaFactory:
    
    @staticmethod
    def create() -> KafkaBackend:
        backend_constructor = _BACKEND_REGISTRY.get(
            settings.KAFKA_BACKEND
        )

        if backend_constructor is None:
            raise ValueError(
                f"Unsupported Kafka backend: {settings.KAFKA_BACKEND}"
            )

        return backend_constructor()