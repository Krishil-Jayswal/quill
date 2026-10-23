from enum import StrEnum

class WorkerType(StrEnum):
    MEDIA = "media"
    TRANSCRIPTION = "transcription"
    FRAME_REDUCTION = "frame-reduction"
    OCR = "ocr"
    CONTEXT = "context"
    NOTES = "notes"