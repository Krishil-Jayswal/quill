from .backends.MobileNetBackendImpl import MobileNetBackendImpl
from collections.abc import Callable
from .base import FrameReductionBackend
from config import settings
from config.enums import FrameReductionProviderType

FrameReductionBackendConstructor = Callable[..., FrameReductionBackend]

_BACKEND_REGISTRY: dict[
    FrameReductionProviderType,
    FrameReductionBackendConstructor
] = {
    FrameReductionProviderType.MOBILE_NET: MobileNetBackendImpl
}

class FrameReductionFactory():
    @staticmethod
    def create(**kwargs) -> FrameReductionBackend:
        backend_constructor = _BACKEND_REGISTRY.get(
                    settings.FRAME_REDUCTION_PROVIDER
                )
        if backend_constructor is None:
            raise ValueError(
                f"Unsupported frame reduction provider: "
                f"{settings.FRAME_REDUCTION_PROVIDER}"
            )
        
        return backend_constructor(**kwargs)