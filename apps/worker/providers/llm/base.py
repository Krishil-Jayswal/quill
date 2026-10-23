from abc import ABC, abstractmethod
from pathlib import Path

class NotesGenerationBackend(ABC):
    def __init__(self) -> None:
        prompts_dir = Path("prompts")
        self._summarisation_system_prompt = (prompts_dir / "summarise.md").read_text(encoding="utf-8")
        self._notes_generation_system_prompt = (prompts_dir / "generate_notes.md").read_text(encoding="utf-8")

    @abstractmethod
    def summarise(self, model_name: str, content: str) -> str:
        ...

    @abstractmethod
    def generate_notes(self, model_name: str, content: str) -> str:
        ...
