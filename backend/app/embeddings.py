"""
Turns text into embedding vectors using Gemini's embedding API
instead of running a model locally -- keeps memory usage low.
"""
import time
from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Takes a list of strings, returns a list of embedding vectors."""
    max_retries = 4
    for attempt in range(max_retries):
        try:
            result = client.models.embed_content(
                model="gemini-embedding-001",
                contents=texts
            )
            return [e.values for e in result.embeddings]
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # give up after final attempt, let the error surface
            wait_time = 2 ** attempt  # 1s, 2s, 4s, 8s
            print(f"Embedding call failed (attempt {attempt+1}), retrying in {wait_time}s...")
            time.sleep(wait_time)