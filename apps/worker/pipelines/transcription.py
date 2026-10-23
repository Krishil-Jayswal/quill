import json
from pathlib import Path
from tqdm import tqdm
from infra.logging import Logger
from providers.transcription import TranscriptionProvider
from schemas import Segment, Transcript

CHUNK_DURATION = 600

def transcription_pipeline(
    audio_chunks_dir: Path,
    transcript_path: Path,
    provider: TranscriptionProvider,
    logger: Logger,
) -> None:

    chunks = sorted(
        [
            path
            for path in audio_chunks_dir.glob("*")
            if path.is_file()
        ]
    )

    logger.info(
        f"Starting audio transcription pipeline. "
        f"Total chunks: {len(chunks)}"
    )

    transcriptions: list[Transcript] = []

    with tqdm(
        total=len(chunks),
        desc="Processing Audio Chunks",
        ncols=100,
    ) as pbar:

        for chunk_index, chunk_path in enumerate(chunks):

            logger.info(
                f"Transcribing chunk "
                f"{chunk_index + 1}/{len(chunks)}: "
                f"{chunk_path.name}"
            )

            transcription = provider.transcribe(
                str(chunk_path)
            )

            transcriptions.append(transcription)

            pbar.update(1)

    transcript = Transcript(
        segments=[
            Segment(
                text=segment.text,
                start=segment.start + chunk_index * CHUNK_DURATION,
                end=segment.end + chunk_index * CHUNK_DURATION,
            )
            for chunk_index, transcription in enumerate(transcriptions)
            for segment in transcription.segments
        ]
    )

    transcript_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    transcript_path.write_text(
        json.dumps(
            transcript.model_dump(),
            indent=2,
        ),
        encoding="utf-8",
    )

    logger.info(
        f"Transcript generated: {transcript_path}"
    )
