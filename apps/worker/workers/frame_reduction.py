from pathlib import Path
from infra.logging.base import Logger
from schemas import KafkaMessage, MediaReadyPayload, FrameReductionReadyPayload
from .base import Worker
from config.enums import WorkerType, KafkaConsumerGroup, KafkaTopic
from providers.frame_reduction import FrameReductionFactory
from pipelines.frame_reduction import frame_reduction_pipeline

class FrameReductionWorker(Worker):
    def __init__(self) -> None:
        super().__init__(
            worker_type=WorkerType.FRAME_REDUCTION,
            consumer_group=KafkaConsumerGroup.FRAME_REDUCTION,
            topics=[KafkaTopic.MEDIA_COMPLETED],
        )

        self._provider = FrameReductionFactory.create()

    def process(
        self,
        message: KafkaMessage,
        logger: Logger,
    ) -> None:

        payload = MediaReadyPayload.model_validate(
            message.value
        )

        job_id = payload.jobId
        frames_object_prefix = payload.framesObjectPrefix

        logger.info("Frame reduction processing started")

        workspace = Path("artifacts") / job_id
        frames_dir = workspace / "frames"
        frame_reduction_dir = workspace / "frame_reduction"
        selected_frames_path = (
            frame_reduction_dir / "selected_frames.json"
        )

        logger.info("Downloading frames")

        self._storage.download_folder(
            object_prefix=frames_object_prefix,
            local_path=str(frames_dir),
        )

        logger.info("Frames downloaded")

        frame_reduction_pipeline(
            frames_dir=frames_dir,
            selected_frames_path=selected_frames_path,
            provider=self._provider,
            logger=logger,
        )
        
        object_key = (
            f"jobs/{job_id}/frame_reduction/selected_frames.json"
        )
        
        logger.info("Uploading selected frames artifact")
        
        self._storage.upload_file(
            local_path=str(selected_frames_path),
            object_key=object_key
        )

        logger.info("Selected frames artifact uploaded")

        self._producer.publish(
            topic=KafkaTopic.FRAME_REDUCTION_COMPLETED,
            key=job_id,
            value=FrameReductionReadyPayload(
                jobId=job_id,
                videoId=payload.videoId,
                selectedFramesObjectKey=object_key,
                framesObjectPrefix=payload.framesObjectPrefix
            ).model_dump()
        )

        logger.info("Frame reduction pipeline completed")