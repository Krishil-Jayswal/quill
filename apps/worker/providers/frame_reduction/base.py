from abc import ABC, abstractmethod
from pathlib import Path

class FrameReductionBackend(ABC):
    @abstractmethod
    def reduce(
        self,
        frames: list[Path]
    ) -> list[str]:
        ...