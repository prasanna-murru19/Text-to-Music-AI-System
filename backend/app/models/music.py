from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class MusicGeneration(Base):
    __tablename__ = "text_to_music"

    id = Column(Integer, primary_key=True, index=True)

    prompt = Column(Text)
    emotion = Column(String)
    genre = Column(String)
    tempo = Column(Integer)
    scale = Column(String)

    midi_path = Column(String, nullable=True)
    wav_path = Column(String, nullable=True)

    duration = Column(Float)
    lyrics = Column(Text)

    status = Column(String, default="completed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
