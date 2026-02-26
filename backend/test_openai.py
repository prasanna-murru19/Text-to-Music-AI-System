from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # <<< THIS LINE IS MUST

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Write 2 lines of a happy song"}
    ],
    max_tokens=50
)

print(resp.choices[0].message.content)
