from pydantic import BaseModel
from typing import Optional

class Track(BaseModel):
    id: str
    title: str
    artist: str
    source_url: str
    audio_path: str
    cover_art_url: str
    bpm: Optional[float] = None
    duration_seconds: Optional[float] = None
