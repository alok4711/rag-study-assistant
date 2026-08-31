"""
RETRIEVAL
Given a user's question, find the most relevant chunks from the notes
you already embedded and stored (see ingest.py).

We'll build this after ingest.py is working.
"""

import chromadb
from app.embeddings import embed_texts

def retrieve_relevant_chunks(question: str, db_path: str, top_k: int = 3) -> list[dict]:
    """
    1. Embed the incoming question the same way you embedded chunks
    2. Query the Chroma collection for the top_k closest chunks
    3. Return them as a list of dicts: [{"text": ..., "source": ...}, ...]

    Important: whatever embedding model you used to store chunks, you must
    use the exact same one here -- otherwise the vectors won't be
    comparable (they'd be measuring "distance" in different spaces).
    """

    question_vector = embed_texts([question])  # note: wrapped in a list

    # Create/connect to persistent ChromaDB
    client = chromadb.PersistentClient(path=db_path)

    # Create or get the collection
    collection = client.get_collection("notes")

    # Find the most relevant chunks
    results = collection.query(
        query_embeddings=question_vector,
        n_results=top_k
    )

    # Convert ChromaDB results into our desired format
    chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for text, metadata in zip(documents, metadatas):
        chunks.append({
            "text": text,
            "source": metadata["source"]
        })

    return chunks