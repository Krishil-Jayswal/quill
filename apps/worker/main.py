from config import settings
from config.enums import WorkerType
from workers.base import Worker

def create_worker(worker_type: WorkerType) -> Worker:
    match worker_type:
        case WorkerType.MEDIA:
            from workers.media import MediaWorker
            return MediaWorker()

        case WorkerType.TRANSCRIPTION:
            from workers.transcription import TranscriptionWorker
            return TranscriptionWorker()

        case WorkerType.FRAME_REDUCTION:
            from workers.frame_reduction import FrameReductionWorker
            return FrameReductionWorker()

        case WorkerType.OCR:
            from workers.ocr import OcrWorker
            return OcrWorker()

        case _:
            raise ValueError(
                f"Unsupported worker type: {worker_type}"
            )

def main() -> None:
    worker_type = WorkerType(settings.WORKER_TYPE)

    worker = create_worker(worker_type)

    worker.run()

if __name__ == "__main__":
    main()
