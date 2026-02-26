
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MusicGeneration(Base):
    __tablename__ = "music_generation"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    emotion = Column(String(50))
    genre = Column(String(50))
    tempo = Column(Integer)
    scale = Column(String(20))
    midi_path = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
