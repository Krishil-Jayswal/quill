import torch
import whisper
from ..base import TranscriptionProvider
from schemas import Transcript, Segment
from typing import cast, Any

class WhisperProviderImpl(TranscriptionProvider):
    def __init__(self, model_name: str = "turbo") -> None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model = whisper.load_model(
            model_name,
            device=device
        )

    def transcribe(self, audio_path: str) -> Transcript:
        result = self._model.transcribe(
            audio=audio_path,
            verbose=False,
        )

        segments = [
            Segment(
                text=segment["text"].strip(),
                start=segment["start"],
                end=segment["end"],
            )
            for segment in cast(list[dict[str, Any]], result["segments"])
        ]

        return Transcript(segments=segments)