from abc import ABC, abstractmethod
from schemas import Transcript

class TranscriptionProvider(ABC):
    @abstractmethod
    def transcribe(self, audio_path: str) -> Transcript:
        ...