from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import re

from app.database import SessionLocal
from app.models.user import User


router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ===================== DB =====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===================== VALIDATIONS =====================
def _validate_email(email: str) -> bool:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email or ""))


def _validate_password(password: str) -> str | None:
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not re.search(r"[A-Za-z]", password):
        return "Password must contain at least one letter"
    if not re.search(r"\d", password):
        return "Password must contain at least one number"
    return None

@router.post("/register")
def register_user(data: dict, db: Session = Depends(get_db)):
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not username:
        raise HTTPException(status_code=400, detail="Username is required")

    if not _validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    pw_error = _validate_password(password)
    if pw_error:
        raise HTTPException(status_code=400, detail=pw_error)

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered")

    password_hash = pwd_context.hash(password)

    user = User(
        username=username,          # ✅ FIXED
        email=email,
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "message": "Registration successful"
    }

@router.post("/login")
def login_user(data: dict, db: Session = Depends(get_db)):
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not _validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {
        "id": user.id,
        "email": user.email,
        "message": "Login successful"
    }
