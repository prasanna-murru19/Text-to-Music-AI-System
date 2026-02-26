import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_lyrics(prompt: str, emotion: str, duration: float):
    # minutes = max(1, int(duration // 60))
    minutes = 1


    full_prompt = f"""
Write song lyrics.

Mood: {emotion}
Duration: about {minutes} minute(s)
Structure:
- Verses
- Chorus
- Optional bridge

Guidelines:
- Creative and non-repetitive
- Matches the mood
- Suitable for a song

Song idea:
{prompt}
"""

    payload = {
        "model": "phi",
        "prompt": full_prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["response"].strip()
