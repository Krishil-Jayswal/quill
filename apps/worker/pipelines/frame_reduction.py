import json
from pathlib import Path
from infra.logging import Logger
from providers.frame_reduction import FrameReductionBackend
from schemas import SelectedFrames

def frame_reduction_pipeline(
    frames_dir: Path,
    selected_frames_path: Path,
    provider: FrameReductionBackend,
    logger: Logger,
) -> None:

    frames = sorted(
        [
            path
            for path in frames_dir.glob("*.jpg")
            if path.is_file()
        ]
    )

    logger.info(
        f"Starting frame reduction. "
        f"Total frames: {len(frames)}"
    )

    selected_frames = provider.reduce(
        frames=frames
    )

    logger.info(
        f"Frame reduction completed. "
        f"Selected {len(selected_frames)} "
        f"of {len(frames)} frames"
    )

    artifact = SelectedFrames(
        frames=selected_frames
    )

    logger.info("Writing selected frames artifact")

    selected_frames_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )
    
    selected_frames_path.write_text(
        json.dumps(
            artifact.model_dump(),
            indent=2,
        ),
        encoding="utf-8",
    )

    logger.info(
        f"Selected frames artifact written: "
        f"{selected_frames_path}"
    )