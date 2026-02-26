import os
import subprocess
import sys
from typing import Literal

import pyttsx3


def _choose_voice(engine, voice_type: str):
    voices = engine.getProperty("voices")
    if not voices:
        return None

    vt = (voice_type or "female").lower()

    # Helper getters (pyttsx3 voice objects vary by platform/driver)
    def _name(v) -> str:
        return (getattr(v, "name", "") or "").lower()

    def _gender(v) -> str:
        return (getattr(v, "gender", "") or "").lower()

    # Prefer explicit gender match first
    if vt == "female":
        for v in voices:
            if "female" in _gender(v):
                return v.id
        # Next: name hints (avoid David when possible)
        for v in voices:
            n = _name(v)
            if "zira" in n or "female" in n or "hazel" in n:
                return v.id
        for v in voices:
            if "david" not in _name(v):
                return v.id

    if vt == "male":
        for v in voices:
            if "male" in _gender(v):
                return v.id
        for v in voices:
            n = _name(v)
            if "david" in n or "male" in n or "mark" in n:
                return v.id

    # Fallback: first available voice
    return voices[0].id


def _edge_tts_voice(voice: str) -> str:
    # These are free Microsoft neural voices (online, not heavy on your PC)
    # You can change these later if you want a different accent.
    v = (voice or "female").lower()
    if v == "male":
        return "en-US-GuyNeural"
    return "en-US-JennyNeural"


def generate_speech(
    text: str,
    out_path: str,
    voice: Literal["male", "female"] = "male",
):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Try high-quality Edge TTS first (if installed + internet).
    # Produces WAV directly (no ffmpeg needed) and usually sounds much less robotic.
    try:
        cmd = [
            sys.executable,
            "-m",
            "edge_tts",
            "--voice",
            _edge_tts_voice(voice),
            "--text",
            text,
            "--write-media",
            out_path,
            "--format",
            "riff-24khz-16bit-mono-pcm",
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return out_path
    except Exception:
        # Fall back to offline Windows voice (pyttsx3)
        pass

    engine = pyttsx3.init()

    # Tune voice slightly by gender
    if voice == "female":
        engine.setProperty("rate", 95)     # slower = less metallic
        engine.setProperty("volume", 0.9)
    else:
        engine.setProperty("rate", 110)
        engine.setProperty("volume", 1.0)

    voice_id = _choose_voice(engine, voice)
    if voice_id:
        engine.setProperty("voice", voice_id)

    engine.save_to_file(text, out_path)
    engine.runAndWait()

    return out_path
