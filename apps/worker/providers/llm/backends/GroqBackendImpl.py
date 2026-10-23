from ..base import NotesGenerationBackend
from config.settings import settings
from groq import Groq

class GroqBackendImpl(NotesGenerationBackend):
    def __init__(self) -> None:
        self._client = Groq(api_key=settings.GROQ_API_KEY)

    def summarise(self, model_name: str, content: str) -> str:
        