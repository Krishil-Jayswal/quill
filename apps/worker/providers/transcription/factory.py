from collections.abc import Callable
from .backends.WhisperProviderImpl import WhisperProviderImpl
from .backends.GroqProviderImpl import GroqProviderImpl
from .base import TranscriptionProvider
from config import settings
from config.enums import TranscriptionProviderType
from typing import Any

TranscriptionProviderConstructor = Callable[..., TranscriptionProvider]

_BACKEND_REGISTRY: dict[
    TranscriptionProviderType,
    TranscriptionProviderConstructor
] = {
    TranscriptionProviderType.GROQ: GroqProviderImpl,
    TranscriptionProviderType.WHISPER: WhisperProviderImpl
}

class TranscriptionFactory():
    @staticmethod
    def create(**kwargs: Any) -> TranscriptionProvider:
        backend_constructor = _BACKEND_REGISTRY.get(
            settings.TRANSCRIPTION_PROVIDER
        )

        if backend_constructor is None:
            raise ValueError(
                f"Unsupported transcription provider: "
                f"{settings.TRANSCRIPTION_PROVIDER}"
            )

        return backend_constructor(**kwargs)