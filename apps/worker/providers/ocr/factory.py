from .base import OcrBackend
from config import settings
from config.enums import OcrProviderType
from collections.abc import Callable
from backends.GroqBackendImpl import GroqBackendImpl

OcrBackendConstructor = Callable[..., OcrBackend]

_BACKEND_REGISTRY: dict[
    OcrProviderType,
    OcrBackendConstructor
] = {
    OcrProviderType.GROQ: GroqBackendImpl
}

class OcrBackendFactory():
    @staticmethod
    def create(**kwargs) -> OcrBackend:
        backend_constructor = _BACKEND_REGISTRY.get(
            settings.OCR_PROVIDER
        )

        if backend_constructor is None:
            raise ValueError(
                f"Unsupported ocr provider: "
                f"{settings.OCR_PROVIDER}"
            )

        return backend_constructor(**kwargs)
