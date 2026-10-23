from pathlib import Path
from infra.logging import Logger
from providers.ocr import OcrBackend

def _save_ocr_output(
    ocr_dir: Path,
    frame_name: str,
    text: str,
) -> None:
    ocr_result_path = (
        ocr_dir / f"{Path(frame_name).stem}.md"
    )
    ocr_result_path.write_text(
        text,
        encoding="utf-8",
    )

def ocr_pipeline(
    frames_dir: Path,
    ocr_dir: Path,
    provider: OcrBackend,
    logger: Logger,
) -> None:
    ocr_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    frames = sorted(
        path
        for path in frames_dir.glob("*.jpg")
        if path.is_file()
    )

    logger.info(
        f"Starting OCR pipeline. Total frames: {len(frames)}"
    )

    if not frames:
        logger.warn("No frames found for OCR")
        return

    processed_frames = 0

    for result in provider.extract(frames=frames):
        for frame_name, text in result.items():
            _save_ocr_output(
                ocr_dir=ocr_dir,
                frame_name=frame_name,
                text=text,
            )

            processed_frames += 1

        logger.info(
            f"OCR progress: {processed_frames}/{len(frames)} frames"
        )

    logger.info(
        f"OCR pipeline completed. "
        f"Processed {processed_frames}/{len(frames)} frames"
    )