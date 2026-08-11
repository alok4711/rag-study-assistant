"""
RETRIEVAL
Given a user's question, find the most relevant chunks from the notes
you already embedded and stored (see ingest.py).

We'll build this after ingest.py is working.
"""


def retrieve_relevant_chunks(question: str, db_path: str, top_k: int = 3) -> list[dict]:
    """
    1. Load the SAME embedding model used in ingest.py (must match!)
    2. Embed the incoming question the same way you embedded chunks
    3. Query the Chroma collection for the top_k closest chunks
    4. Return them as a list of dicts: [{"text": ..., "source": ...}, ...]

    Important: whatever embedding model you used to store chunks, you must
    use the exact same one here -- otherwise the vectors won't be
    comparable (they'd be measuring "distance" in different spaces).
    """
    raise NotImplementedError("We'll build this after ingest.py works end to end.")
