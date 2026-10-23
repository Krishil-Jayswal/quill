from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
import base64
import re

class OcrBackend(ABC):
    def __init__(self) -> None:
        self._system_prompt = (Path("prompts") / "ocr.md").read_text(encoding="utf-8")

    def encode(
        self,
        frame_path: Path
    ) -> str:
        with frame_path.open("rb") as f:
            return base64.b64encode(
                f.read()
            ).decode("utf-8")

    @abstractmethod
    def extract(
        self,
        frames: list[Path]
    ) -> Iterator[dict[str, str]]:
        ...

    def parse_response(
        self,
        frames: list[Path],
        content: str
    ) -> dict[str, str]:
        matches = re.findall(
            r"### Image (\d+)\s*(.*?)(?=### Image \d+|$)",
            content,
            flags=re.DOTALL,
        )

        results: dict[str, str] = {}

        for image_number, text in matches:
            index = int(image_number) - 1

            if not 0 <= index < len(frames):
                continue

            results[frames[index].name] = text.strip()

        return results