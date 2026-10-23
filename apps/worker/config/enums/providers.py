from enum import StrEnum

class TranscriptionProviderType(StrEnum):
    GROQ = "groq"
    WHISPER = "whisper"

class FrameReductionProviderType(StrEnum):
    MOBILE_NET = "mobilenet"

class OcrProviderType(StrEnum):
    GROQ = "groq"

class LLMProvider(StrEnum):
    GROQ = "groq"
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
