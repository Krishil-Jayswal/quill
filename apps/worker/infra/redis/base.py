from abc import ABC, abstractmethod

class RedisBackend(ABC):

    @abstractmethod
    def get(self, key: str) -> str | None:
        ...

    @abstractmethod
    def set(
        self,
        key: str,
        value: str,
        ttl_seconds: int | None = None,
    ) -> None:
        ...

    @abstractmethod
    def delete(self, key: str) -> None:
        ...

    @abstractmethod
    def acquire_lock(
        self,
        key: str,
        ttl_seconds: int,
    ) -> bool:
        ...

    @abstractmethod
    def release_lock(self, key: str) -> None:
        ...

    @abstractmethod
    def log(
        self,
        job_id: str,
        message: str,
        level: str,
    ) -> None:
        ...