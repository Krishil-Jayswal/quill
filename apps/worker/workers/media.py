from infra.logging import Logger
from schemas import KafkaMessage, VideoUploadedPayload, MediaReadyPayload
from .base import Worker
from config.enums import KafkaTopic, KafkaConsumerGroup, WorkerType
from pipelines.ffmpeg import ffmpeg_pipeline
from pathlib import Path

class MediaWorker(Worker):
    def __init__(self) -> None:
        super().__init__(
            worker_type=WorkerType.MEDIA,
            consumer_group=KafkaConsumerGroup.MEDIA, 
            topics=[KafkaTopic.VIDEO_UPLOADED]
        )

    def process(self, message: KafkaMessage, logger: Logger) -> None:
        payload = VideoUploadedPayload.model_validate(message.value)

        job_id = payload.jobId
        filename = payload.filename
        object_key = payload.objectKey

        logger.info("Media processing started")

        workspace = Path("artifacts") / job_id

        video_path = workspace / filename
        frames_dir = workspace / "frames"
        audio_dir = workspace / "audio"
        audio_chunks_dir = workspace / "audio_chunks"

        logger.info("Downloading video")

        self._storage.download_file(
            object_key=object_key,
            local_path=str(video_path),
        )

        logger.info("Video downloaded")

        ffmpeg_pipeline(
            video_path=video_path,
            frames_dir=frames_dir,
            audio_dir=audio_dir,
            audio_chunks_dir=audio_chunks_dir,
            on_log=logger.info,
        )

        logger.info("FFmpeg processing finished")

        frames_prefix = (
            f"jobs/{job_id}/frames"
        )

        audio_prefix = (
            f"jobs/{job_id}/audio"
        )

        logger.info("Uploading frames")

        self._storage.upload_directory(
            local_dir=str(frames_dir),
            object_prefix=frames_prefix,
        )

        logger.info("Frames uploaded")

        logger.info("Uploading audio chunks")

        self._storage.upload_directory(
            local_dir=str(audio_chunks_dir),
            object_prefix=audio_prefix,
        )

        logger.info("Audio chunks uploaded")

        self._producer.publish(
            topic=KafkaTopic.MEDIA_COMPLETED,
            key=job_id,
            value=MediaReadyPayload(
                jobId=job_id,
                videoId=payload.videoId,
                audioObjectPrefix=audio_prefix,
                framesObjectPrefix=frames_prefix
            ).model_dump(),
        )

        logger.info("Media processing completed")