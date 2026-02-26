from pydantic import BaseModel

class MusicCreate(BaseModel):
    prompt: str
    emotion: str
    genre: str
    tempo: int
    scale: str

class MusicResponse(MusicCreate):
    id: int
    midi_path: str

    class Config:
        from_attributes = True
