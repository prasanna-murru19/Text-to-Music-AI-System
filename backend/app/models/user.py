from sqlalchemy import Column, Integer, String, DateTime ,Text
from sqlalchemy.sql import func
from app.database import Base
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)  # ✅ matches DB
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

