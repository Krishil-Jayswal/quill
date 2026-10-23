from abc import ABC, abstractmethod
from infra.kafka import KafkaFactory
from infra.storage import StorageFactory
from infra.logging import LoggerFactory, Logger
from schemas import KafkaMessage
from config.enums import WorkerType
from pathlib import Path

class Worker(ABC):
    def __init__(self, worker_type: WorkerType, consumer_group: str, topics: list[str]) -> None:
        kafka = KafkaFactory.create()

        self._worker_type = worker_type
        self._consumer = kafka.consumer(group_id=consumer_group)
        self._consumer.subscribe(topics=topics)
        self._producer = kafka.producer()
        self._storage = StorageFactory.create()

    def run(self) -> None:
        while True:
            message = self._consumer.consume()

            if message is None:
                continue

            try:
                job_id = message.value.get("jobId", "")

                logger = LoggerFactory.create(self._producer, job_id)

                self.create_workspace(job_id)

                self.process(message, logger)
                self._consumer.commit(message)

                self.clear_workspace(job_id)

            except Exception as error:
                self.handle_error(message, error)

    @abstractmethod
    def process(self, message: KafkaMessage, logger: Logger) -> None:
        ...

    def handle_error(self, message: KafkaMessage, error: Exception) -> None:
        print(
            f"Worker failed: "
            f"{message.topic}"
            f"{message.partition}"
            f"{message.offset}"
            f"{error}"
        )

    def create_workspace(self, job_id: str) -> None:
        workspace = Path("artifacts") / job_id
        frames_dir = workspace / "frames"
        audio_dir = workspace / "audio"
        audio_chunks_dir = audio_dir / "audio_chunks"
        transcript_path = workspace / "transcription" / "transcript.json"
        selected_frames_path = workspace / "frame_reduction" / "selected_frames.json"
        ocr_dir = workspace / "ocr"

    def clear_workspace(self, job_id: str) -> None:
        pass