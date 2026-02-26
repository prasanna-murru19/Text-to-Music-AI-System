from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes.music import router as music_router
from app.routes.auth import router as auth_router
from app.database import Base, engine
import nltk

# Load environment variables
load_dotenv()

app = FastAPI(title="Text-to-Music AI System")


# Download NLTK data on startup
@app.on_event("startup")
def setup_nltk():
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")


# ✅ CORS (Frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTES
app.include_router(auth_router)
app.include_router(music_router)


@app.get("/")
def root():
    return {"message": "Text-to-Music Backend Running"}


# Create DB tables (music + user models)
Base.metadata.create_all(bind=engine)
