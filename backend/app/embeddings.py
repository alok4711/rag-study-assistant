"""
Loads the embedding model ONCE when this module is first imported,
so every other file that needs it reuses the same loaded model
instead of reloading it repeatedly.
"""
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")