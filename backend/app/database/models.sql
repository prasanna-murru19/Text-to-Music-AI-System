CREATE TABLE music_generation (
    id SERIAL PRIMARY KEY,
    prompt TEXT,
    emotion VARCHAR(50),
    genre VARCHAR(50),
    midi_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
