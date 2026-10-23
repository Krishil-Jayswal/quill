from collections.abc import Callable
from .base import Logger
from .backends.KafkaLoggerImpl import KafkaLoggerImpl
from config import settings
from config.enums import LoggerBackendType, WorkerType
from infra.kafka import KafkaProducer

LoggerConstructor = Callable[
    [KafkaProducer, str, WorkerType], 
    Logger
]

_BACKEND_REGISTRY: dict[
    LoggerBackendType,
    LoggerConstructor
] = {
    LoggerBackendType.KAFKA: KafkaLoggerImpl
}

class LoggerFactory():
    @staticmethod
    def create(producer: KafkaProducer, job_id: str) -> Logger:
        logger_constructor = _BACKEND_REGISTRY.get(
            settings.LOGGER_BACKEND
        )

        if logger_constructor is None:
            raise ValueError(
                f"Unsupported logger backend: "
                f"{settings.LOGGER_BACKEND}"
            )

        return logger_constructor(producer, job_id, settings.WORKER_TYPE)