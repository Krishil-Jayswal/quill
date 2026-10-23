from pydantic import BaseModel
from typing import List

class Segment(BaseModel):
    text: str
    start: float
    end: float

class Transcript(BaseModel):
    segments: List[Segment]
