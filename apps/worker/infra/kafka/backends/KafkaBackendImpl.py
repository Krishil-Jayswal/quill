import json
from typing import Any, cast
from kafka import KafkaConsumer as KafkaPythonConsumer
from kafka import KafkaProducer as KafkaPythonProducer
from config import settings
from schemas import KafkaMessage
from ..base import (
    KafkaBackend,
    KafkaConsumer,
    KafkaProducer,
)

def serialize_key(key: str | None) -> bytes | None:
    if key is None:
        return None

    return key.encode("utf-8")

def deserialize_value(value: bytes | None) -> dict[str, Any]:
    if value is None:
        return {}

    return json.loads(value.decode("utf-8"))

def deserialize_key(key: bytes | None) -> str | None:
    if key is None:
        return None

    return key.decode("utf-8")

class KafkaProducerImpl(KafkaProducer):
    def __init__(self) -> None:
        self._producer = KafkaPythonProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            client_id=settings.KAFKA_CLIENT_ID,
            security_protocol=cast(Any, settings.KAFKA_SECURITY_PROTOCOL),
            sasl_mechanism=cast(Any, settings.KAFKA_SASL_MECHANISM),
            sasl_plain_username=settings.KAFKA_SASL_USERNAME or None,
            sasl_plain_password=settings.KAFKA_SASL_PASSWORD or None,
            key_serializer=cast(Any, serialize_key),
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        )

    def publish(
        self,
        topic: str,
        value: dict[str, Any],
        key: str | None = None,
    ) -> None:
        future = self._producer.send(
            topic,
            key=key,
            value=value,
        )

        future.get(timeout=10)

    def close(self) -> None:
        self._producer.flush()
        self._producer.close()

class KafkaConsumerImpl(KafkaConsumer):
    def __init__(self, group_id: str) -> None:
        self._consumer = KafkaPythonConsumer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=group_id,
            client_id=settings.KAFKA_CLIENT_ID,
            security_protocol=cast(Any, settings.KAFKA_SECURITY_PROTOCOL),
            sasl_mechanism=cast(Any, settings.KAFKA_SASL_MECHANISM),
            enable_auto_commit=False,
            value_deserializer=deserialize_value,
            key_deserializer=deserialize_key,
        )

    def subscribe(self, topics: list[str]) -> None:
        self._consumer.subscribe(topics)

    def consume(self) -> KafkaMessage | None:
        records = self._consumer.poll(
            timeout_ms=1000,
            max_records=1,
        )

        if not records:
            return None

        _, messages = next(iter(records.items()))
        message = messages[0]

        return KafkaMessage(
            topic=message.topic,
            key=message.key,
            value=message.value,
            partition=message.partition,
            offset=message.offset,
        )

    def commit(self, message: KafkaMessage) -> None:
        self._consumer.commit()

    def close(self) -> None:
        self._consumer.close()

class KafkaBackendImpl(KafkaBackend):
    def producer(self) -> KafkaProducer:
        return KafkaProducerImpl()

    def consumer(self, group_id: str) -> KafkaConsumer:
        return KafkaConsumerImpl(group_id)