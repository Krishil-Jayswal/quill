from dataclasses import dataclass
from typing import Any
from config.enums import WorkerType, LogLevel

@dataclass(frozen=True)
class KafkaMessage:
    topic: str
    key: str | None
    value: dict[str, Any]
    partition: int
    offset: int

@dataclass(frozen=True)
class LogEvent:
    jobId: str
    stage: WorkerType | None
    level: LogLevel
    message: str
    timestamp: str