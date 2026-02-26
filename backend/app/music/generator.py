import pretty_midi
import random
import os
import time


# ===================== EMOTION → CHORDS =====================
CHORD_PROGRESSIONS = {
    "happy": [[60, 64, 67], [62, 65, 69], [67, 71, 74]],
    "sad": [[60, 63, 67], [62, 65, 68]],
    "calm": [[60, 64, 67], [65, 69, 72]],
    "angry": [[60, 63, 67], [59, 62, 65]],
    "neutral": [[60, 64, 67]]
}


# ===================== GENRE → MUSIC STYLE =====================
GENRE_SETTINGS = {
    "lofi": {
        "instrument": 0,        # Piano
        "tempo": (60, 80),
        "melody_gap": (0.5, 0.9),
        "velocity": (50, 80),
        "octaves": [0],
    },
    "pop": {
        "instrument": 24,       # Guitar
        "tempo": (90, 120),
        "melody_gap": (0.25, 0.45),
        "velocity": (80, 120),
        "octaves": [0, 12],
    },
    "classical": {
        "instrument": 40,       # Violin
        "tempo": (70, 100),
        "melody_gap": (0.4, 0.8),
        "velocity": (60, 100),
        "octaves": [-12, 0, 12],
    }
}


# ===================== MAIN GENERATOR =====================
def generate_music(features, prompt: str, genre: str = "lofi"):
    os.makedirs("generated_music", exist_ok=True)

    # Same prompt → same style
    random.seed(prompt.lower().strip())

    # Validate genre
    genre_cfg = GENRE_SETTINGS.get(genre, GENRE_SETTINGS["lofi"])

    # Tempo priority: genre > NLP
    tempo = random.randint(*genre_cfg["tempo"])

    midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    instrument = pretty_midi.Instrument(program=genre_cfg["instrument"])

    # Emotion-based harmony
    emotion = features.get("emotion", "neutral")
    chords = CHORD_PROGRESSIONS.get(emotion, CHORD_PROGRESSIONS["neutral"])
    random.shuffle(chords)

    scale = features.get("scale", "major")
    scale_notes = (
        [60, 62, 64, 65, 67, 69, 71]
        if scale == "major"
        else [60, 62, 63, 65, 67, 68, 70]
    )

    beat = 60 / tempo
    time_cursor = 0.0

    # ===================== INTRO (CHORDS) =====================
    for chord in chords:
        duration = beat * random.choice([2, 3, 4])
        for pitch in chord:
            instrument.notes.append(
                pretty_midi.Note(
                    velocity=70,
                    pitch=pitch,
                    start=time_cursor,
                    end=time_cursor + duration
                )
            )
        time_cursor += duration

    # ===================== MAIN MELODY (1 MIN) =====================
    TARGET_DURATION = 60  # seconds

    while time_cursor < TARGET_DURATION:
        pitch = (
            random.choice(scale_notes)
            + random.choice(genre_cfg["octaves"])
        )

        duration = random.uniform(*genre_cfg["melody_gap"])

        instrument.notes.append(
            pretty_midi.Note(
                velocity=random.randint(*genre_cfg["velocity"]),
                pitch=pitch,
                start=time_cursor,
                end=time_cursor + duration
            )
        )
        time_cursor += duration

    midi.instruments.append(instrument)

    filename = f"music_{int(time.time() * 1000)}.mid"
    path = os.path.join("generated_music", filename)
    midi.write(path)

    duration = round(midi.get_end_time(), 2)
    return path, duration
