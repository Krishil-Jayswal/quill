import json
from pathlib import Path

from schemas import (
    KafkaMessage,
    FrameReductionReadyPayload,
    OcrReadyPayload,
    SelectedFrames,
)
from .base import Worker
from config.enums import WorkerType, KafkaTopic, KafkaConsumerGroup
from providers.ocr import OcrBackendFactory
from infra.logging import Logger
from pipelines.ocr import ocr_pipeline

class OcrWorker(Worker):
    def __init__(self) -> None:
        super().__init__(
            worker_type=WorkerType.OCR,
            consumer_group=KafkaConsumerGroup.OCR,
            topics=[KafkaTopic.FRAME_REDUCTION_COMPLETED],
        )

        self._provider = OcrBackendFactory.create()

    def process(
        self,
        message: KafkaMessage,
        logger: Logger,
    ) -> None:
        payload = FrameReductionReadyPayload.model_validate(
            message.value
        )

        job_id = payload.jobId
        selected_frames_object_key = (
            payload.selectedFramesObjectKey
        )
        frames_object_prefix = payload.framesObjectPrefix

        workspace = Path("artifacts") / job_id
        frames_dir = workspace / "frames"
        frame_reduction_dir = workspace / "frame_reduction"
        ocr_dir = workspace / "ocr"

        selected_frames_path = (
            frame_reduction_dir / "selected_frames.json"
        )

        logger.info("OCR processing started")

        logger.info("Downloading selected frames metadata")

        self._storage.download_file(
            object_key=selected_frames_object_key,
            local_path=str(selected_frames_path),
        )

        logger.info("Selected frames metadata downloaded")

        selected_frames = SelectedFrames.model_validate(
            json.loads(
                selected_frames_path.read_text(
                    encoding="utf-8"
                )
            )
        )

        logger.info(
            f"Selected frames loaded: "
            f"{len(selected_frames.frames)} frames"
        )

        selected_frames_object_keys = [
            f"{frames_object_prefix.rstrip('/')}/{frame}"
            for frame in selected_frames.frames
        ]

        logger.info(
            f"Downloading {len(selected_frames_object_keys)} "
            "selected frames"
        )

        self._storage.download_files(
            object_keys=selected_frames_object_keys,
            local_dir=str(frames_dir),
        )

        logger.info("Selected frames downloaded")

        ocr_pipeline(
            frames_dir=frames_dir,
            ocr_dir=ocr_dir,
            provider=self._provider,
            logger=logger,
        )

        ocr_prefix = (
            f"jobs/{job_id}/ocr"
        )

        logger.info(
            f"Uploading OCR artifacts"
        )

        self._storage.upload_directory(
            local_dir=str(ocr_dir),
            object_prefix=ocr_prefix,
        )

        logger.info("OCR artifacts uploaded")

        self._producer.publish(
            topic=KafkaTopic.OCR_COMPLETED,
            key=job_id,
            value=OcrReadyPayload(
                jobId=job_id,
                videoId=payload.videoId,
                ocrObjectPrefix=ocr_prefix,
            ).model_dump(),
        )

        logger.info("OCR processing completed")
