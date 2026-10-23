from groq import Groq
from schemas import Transcript, Segment
from ..base import TranscriptionProvider
from config import settings

class GroqProviderImpl(TranscriptionProvider):
    def __init__(self, model_name: str = "whisper-large-v3-turbo") -> None:
        self._client = Groq(api_key=settings.GROQ_API_KEY)
        self._model_name = model_name

    def transcribe(self, audio_path: str) -> Transcript:
        f = open(audio_path, "rb")
        
        result = self._client.audio.transcriptions.create(
                model=self._model_name,
                file=f,
                response_format="verbose_json"
            ).model_dump()

        f.close()

        segments = [
            Segment(
                text=segment['text'].strip(),
                start=segment['start'],
                end=segment['end']
            )
            for segment in result['segments']
        ]

        return Transcript(
            segments=segments
        )