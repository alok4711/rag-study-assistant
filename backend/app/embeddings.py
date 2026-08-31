"""
Turns text into embedding vectors using Gemini's embedding API
instead of running a model locally -- keeps memory usage low.
"""
from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def embed_texts(texts: list[str]) -> list[list[float]]:
    """Takes a list of strings, returns a list of embedding vectors."""
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts
    )
    return [e.values for e in result.embeddings]