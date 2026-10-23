from abc import ABC, abstractmethod
from schemas.kafka import KafkaMessage

class KafkaProducer(ABC):

    @abstractmethod
    def publish(
        self,
        topic: str,
        value: dict,
        key: str | None = None,
    ) -> None:
        ...

class KafkaConsumer(ABC):

    @abstractmethod
    def subscribe(
        self,
        topics: list[str],
    ) -> None:
        ...

    @abstractmethod
    def consume(self) -> KafkaMessage | None:
        ...

    @abstractmethod
    def commit(self, message: KafkaMessage) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

class KafkaBackend(ABC):

    @abstractmethod
    def producer(self) -> KafkaProducer:
        ...

    @abstractmethod
    def consumer(
        self,
        group_id: str,
    ) -> KafkaConsumer:
        ...