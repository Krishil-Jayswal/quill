import subprocess
from collections.abc import Callable
from pathlib import Path
from threading import Thread

LogCallback = Callable[[str], None]

def _stream_output(
    process: subprocess.Popen[str],
    on_log: LogCallback,
) -> None:
    assert process.stdout is not None

    for line in process.stdout:
        line = line.rstrip()

        if line:
            on_log(line)

def _start_ffmpeg(
    command: list[str],
    on_log: LogCallback,
) -> subprocess.Popen[str]:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    Thread(
        target=_stream_output,
        args=(process, on_log),
        daemon=True,
    ).start()

    return process

def ffmpeg_pipeline(
    video_path: Path,
    frames_dir: Path,
    audio_dir: Path,
    audio_chunks_dir: Path,
    on_log: LogCallback,
) -> None:

    frames_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    audio_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    audio_chunks_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    on_log(
        "Starting audio extraction and frame extraction"
    )

    audio_process = _start_ffmpeg(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            f"{audio_dir}/audio.wav",
        ],
        on_log,
    )

    frames_process = _start_ffmpeg(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vf",
            "fps=1",
            f"{frames_dir}/frame_%05d.jpg",
        ],
        on_log,
    )

    audio_return_code = audio_process.wait()

    if audio_return_code != 0:
        raise RuntimeError(
            "Audio extraction failed "
            f"with exit code {audio_return_code}"
        )

    on_log(
        "Audio extraction finished"
    )

    on_log(
        "Starting audio chunking"
    )

    audio_chunk_process = _start_ffmpeg(
        [
            "ffmpeg",
            "-y",
            "-i",
            f"{audio_dir}/audio.wav",
            "-f",
            "segment",
            "-segment_time",
            "600",
            "-c",
            "copy",
            f"{audio_chunks_dir}/chunk_%03d.wav",
        ],
        on_log,
    )

    audio_chunk_return_code = audio_chunk_process.wait()

    frames_return_code = frames_process.wait()

    if audio_chunk_return_code != 0:
        raise RuntimeError(
            "Audio chunking failed "
            f"with exit code {audio_chunk_return_code}"
        )

    if frames_return_code != 0:
        raise RuntimeError(
            "Frame extraction failed "
            f"with exit code {frames_return_code}"
        )

    on_log(
        "Audio chunks and frames generated successfully"
    )