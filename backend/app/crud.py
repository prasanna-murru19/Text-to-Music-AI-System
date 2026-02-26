from sqlalchemy.orm import Session
from app.models.music import MusicGeneration


def create_music(db: Session, data: dict):
    music = MusicGeneration(**data)
    db.add(music)
    db.commit()
    db.refresh(music)
    return music

def get_all_music(db: Session):
    return db.query(MusicGeneration).order_by(MusicGeneration.created_at.desc()).all()


