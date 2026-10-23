from pydantic import BaseModel

class VideoUploadedPayload(BaseModel):
    jobId: str
    videoId: str
    filename: str
    objectKey: str

class MediaReadyPayload(BaseModel):
    jobId: str
    videoId: str
    audioObjectPrefix: str
    framesObjectPrefix: str

class TranscriptionReadyPayload(BaseModel):
    jobId: str
    videoId: str
    transcriptObjectKey: str

class FrameReductionReadyPayload(BaseModel):
    jobId: str
    videoId: str
    selectedFramesObjectKey: str
    framesObjectPrefix: str

class OcrReadyPayload(BaseModel):
    jobId: str
    videoId: str
    ocrObjectPrefix: str

class NotesReadyPayload(BaseModel):
    jobId: str
    videoId: str
    notesObjectKey: str