import os
from dotenv import load_dotenv
from google import genai

load_dotenv(dotenv_path=".env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say only Hello"
    )

    print(response.text)

except Exception as e:
    print("ERROR:", e)