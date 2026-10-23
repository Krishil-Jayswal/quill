from schemas import KafkaMessage, MediaReadyPayload, TranscriptionReadyPayload
from .base import Worker
from infra.logging import Logger
from config.enums import WorkerType, KafkaConsumerGroup, KafkaTopic
from providers.transcription import TranscriptionFactory
from pipelines.transcription import transcription_pipeline
from pathlib import Path

class TranscriptionWorker(Worker):
    def __init__(self) -> None:
        super().__init__(
            worker_type=WorkerType.TRANSCRIPTION, 
            consumer_group=KafkaConsumerGroup.TRANSCRIPTION, 
            topics=[KafkaTopic.MEDIA_COMPLETED]
        )
        self._provider = TranscriptionFactory.create()

    def process(self, message: KafkaMessage, logger: Logger) -> None:
        payload = MediaReadyPayload.model_validate(message.value)

        job_id = payload.jobId
        audio_prefix = payload.audioObjectPrefix

        logger.info("Transcription processing started")

        workspace = Path("artifacts") / job_id
        audio_chunks_dir = workspace / "audio"
        transcription_dir = workspace / "transcription"
        transcript_path = transcription_dir / "transcript.json"

        logger.info("Downloding audio chunks")

        self._storage.download_folder(
            object_prefix=audio_prefix,
            local_path=str(audio_chunks_dir)
        )

        logger.info("Audio chunks downloaded")

        transcription_pipeline(
            audio_chunks_dir=audio_chunks_dir,
            transcript_path=transcript_path,
            provider=self._provider,
            logger=logger
        )

        logger.info("Audio transcription completed")

        object_key = (
            f"jobs/{job_id}/transcription/transcript.json"
        )
        
        logger.info("Uploading transcript")

        self._storage.upload_file(
            local_path=str(transcript_path),
            object_key=object_key
        )

        logger.info("Transcript uploaded")

        self._producer.publish(
            topic=KafkaTopic.TRANSCRIPTION_COMPLETED,
            key=job_id,
            value=TranscriptionReadyPayload(
                jobId=job_id,
                videoId=payload.videoId,
                transcriptObjectKey=object_key
            ).model_dump()
        )

        logger.info("Transcription processing completed")