from config.enums import LogLevel, WorkerType, KafkaTopic
from ..base import Logger
from infra.kafka import KafkaProducer
from schemas import LogEvent
from datetime import datetime, timezone
from dataclasses import asdict

class KafkaLoggerImpl(Logger):
    def __init__(self, producer: KafkaProducer, job_id: str, stage: WorkerType) -> None:
        self._producer = producer
        self._job_id = job_id
        self._stage = stage

    def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        self._producer.publish(
            topic=KafkaTopic.LOGS,
            value=asdict(LogEvent(
                jobId=self._job_id,
                stage=self._stage,
                level=level,
                message=message,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
        ))