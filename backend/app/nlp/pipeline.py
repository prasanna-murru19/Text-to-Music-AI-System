import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os

# ----------------------------
# NLTK Setup
# ----------------------------
nltk_data_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "nltk_data")
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

nltk.download("punkt", download_dir=nltk_data_path, quiet=True)
nltk.download("stopwords", download_dir=nltk_data_path, quiet=True)

stop_words = set(stopwords.words("english"))

# ----------------------------
# Preprocess
# ----------------------------
def preprocess(text: str):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    return tokens

# ----------------------------
# Emotion Detection (IMPROVED)
# ----------------------------
emotion_map = {
    "happy": [
        "happy", "joy", "love", "excited", "energetic",
        "fun", "party", "cheerful", "smile", "enjoy"
    ],
    "sad": ["sad", "lonely", "cry", "pain", "tear", "depressed"],
    "angry": ["angry", "rage", "hate", "furious", "mad"],
    "calm": ["peace", "relax", "calm", "quiet", "slow"]
}

def detect_emotion(tokens):
    scores = {emotion: 0 for emotion in emotion_map}
    for emotion, keywords in emotion_map.items():
        for t in tokens:
            if t in keywords:
                scores[emotion] += 2   # 🔥 boost weight

    detected = max(scores, key=scores.get)
    return detected if scores[detected] > 0 else "neutral"

# ----------------------------
# Genre Detection
# ----------------------------
genre_map = {
    "lofi": ["chill", "study", "relax"],
    "classical": ["piano", "violin", "orchestra"],
    "rock": ["guitar", "drums", "band"],
    "pop": ["dance", "party", "beat"],
    "ambient": ["space", "atmosphere", "background"]
}

def detect_genre(tokens):
    for genre, keywords in genre_map.items():
        for t in tokens:
            if t in keywords:
                return genre
    return "pop"   # 🎵 better default for energy

# ----------------------------
# Map Emotion → Music Features
# ----------------------------
def map_to_music_features(emotion, genre):
    tempo_map = {
        "happy": 150,     # 🔥 FAST
        "sad": 70,
        "angry": 160,     # 🔥 VERY FAST
        "calm": 60,
        "neutral": 100
    }

    scale_map = {
        "happy": "major",
        "sad": "minor",
        "angry": "minor",
        "calm": "major",
        "neutral": "major"
    }

    return {
        "emotion": emotion,
        "genre": genre,
        "tempo": tempo_map.get(emotion, 100),
        "scale": scale_map.get(emotion, "major")
    }

# ----------------------------
# Full Pipeline
# ----------------------------
def process_text(text: str):
    tokens = preprocess(text)
    emotion = detect_emotion(tokens)
    genre = detect_genre(tokens)
    features = map_to_music_features(emotion, genre)

    return {
        "tokens": tokens,
        "emotion": emotion,
        "genre": genre,
        "music_features": features
    }
