from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import traceback

from app.database import SessionLocal
from app.models.music import MusicGeneration
from app.nlp.pipeline import process_text
from app.music.generator import generate_music
from app.lyrics.generator import generate_lyrics
from app.audio.converter import midi_to_wav
from app.audio.mixer import merge_audio
from app.audio.tts import generate_speech
from app.audio.singing import speech_to_singing


router = APIRouter(prefix="/music", tags=["Music"])


# ===================== DB =====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===================== LYRICS → TTS PREP =====================
def prepare_lyrics_for_tts(lyrics: str) -> str:
    lines = [l.strip() for l in lyrics.split("\n") if l.strip()]

    verse, chorus, bridge = [], [], []
    current = None

    for line in lines:
        lower = line.lower()
        if lower.startswith("verse"):
            current = verse
            continue
        elif lower.startswith("chorus"):
            current = chorus
            continue
        elif lower.startswith("bridge"):
            current = bridge
            continue

        if current is not None:
            current.append(line)

    def speak_block(block):
        return "\n".join(b + "..." for b in block)

    tts_text = ""

    if verse:
        tts_text += speak_block(verse) + "\n\n"
    if chorus:
        tts_text += speak_block(chorus) + "\n\n"
        tts_text += speak_block(chorus) + "\n\n"
    if bridge:
        tts_text += speak_block(bridge) + "\n\n"
    if chorus:
        tts_text += speak_block(chorus)

    return tts_text.strip()


# ===================== GENERATE =====================
@router.post("/generate")
def generate_music_api(data: dict, db: Session = Depends(get_db)):
    try:
        prompt = (data.get("prompt") or "").strip()
        voice = data.get("voice", "male")
        genre = data.get("genre", "lofi")

        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")

        if voice not in ("male", "female"):
            voice = "male"

        if genre not in ("lofi", "pop", "classical"):
            genre = "lofi"

        # 🧠 NLP
        analysis = process_text(prompt)

        # 🎵 MIDI generation (GENRE AWARE)
        midi_path, duration = generate_music(
            analysis["music_features"],
            prompt,
            genre=genre
        )

        # 🔊 MIDI → WAV
        instrumental_wav = midi_to_wav(
            midi_path,
            midi_path.replace(".mid", "_instrumental.wav")
        )

        if not os.path.exists(instrumental_wav):
            raise HTTPException(500, "Instrumental audio generation failed")

        # ✍️ Lyrics
        lyrics = generate_lyrics(
            prompt,
            analysis["emotion"],
            duration
        )

        # 🎤 Lyrics → TTS
        tts_text = prepare_lyrics_for_tts(lyrics)

        speech_wav = generate_speech(
            tts_text,
            midi_path.replace(".mid", "_speech.wav"),
            voice=voice,
        )

        if not os.path.exists(speech_wav):
            raise HTTPException(500, "TTS audio generation failed")

        # 🎶 Singing-style effect (optional)
        try:
            vocal_wav = speech_to_singing(
                speech_wav,
                midi_path,
                midi_path.replace(".mid", "_vocal.wav"),
                voice=voice
            )
        except Exception:
            vocal_wav = speech_wav

        # 🎼 Merge audio
        final_wav = midi_path.replace(".mid", "_final.wav")
        wav_path = merge_audio(instrumental_wav, vocal_wav, final_wav)

        # 💾 Save DB
        record = MusicGeneration(
            prompt=prompt,
            emotion=analysis["emotion"],
            genre=genre,
            tempo=analysis["music_features"]["tempo"],
            scale=analysis["music_features"]["scale"],
            midi_path=midi_path,
            wav_path=wav_path,
            duration=duration,
            lyrics=lyrics,
            status="completed"
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "id": record.id,
            "prompt": prompt,
            "genre": genre,
            "duration": duration,
            "lyrics": lyrics,
            "wav_path": wav_path
        }

    except HTTPException:
        raise
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# ===================== LIST =====================
@router.get("/")
def list_music(db: Session = Depends(get_db)):
    records = db.query(MusicGeneration).order_by(
        MusicGeneration.created_at.desc()
    ).all()

    return [
        {
            "id": r.id,
            "prompt": r.prompt,
            "emotion": r.emotion,
            "genre": r.genre,
            "tempo": r.tempo,
            "scale": r.scale,
            "wav_path": r.wav_path,
            "duration": r.duration,
            "lyrics": r.lyrics,
            "created_at": r.created_at.isoformat()
        }
        for r in records
    ]


# ===================== DOWNLOAD =====================
@router.get("/download/wav/{music_id}")
def download_wav(music_id: int, db: Session = Depends(get_db)):
    record = db.query(MusicGeneration).get(music_id)

    if not record or not record.wav_path or not os.path.exists(record.wav_path):
        raise HTTPException(404, "WAV not found")

    return FileResponse(
        record.wav_path,
        media_type="audio/wav",
        filename=os.path.basename(record.wav_path)
    )


# ===================== DELETE =====================
@router.delete("/{music_id}")
def delete_music(music_id: int, db: Session = Depends(get_db)):
    record = db.query(MusicGeneration).get(music_id)

    if not record:
        raise HTTPException(404, "Not found")

    if record.wav_path and os.path.exists(record.wav_path):
        os.remove(record.wav_path)

    if record.midi_path and os.path.exists(record.midi_path):
        os.remove(record.midi_path)

    db.delete(record)
    db.commit()

    return {"message": "Deleted successfully"}
