"""
INGESTION PIPELINE
This is the "load your notes into the system" step. Run this file once
(or whenever your notes change) to rebuild the searchable database.

Flow: read files -> split into chunks -> embed each chunk -> store in ChromaDB

We'll build this together step by step. For now, here's the skeleton with
guidance. Don't write the implementation yet -- we'll do this piece by piece
in our next session, starting with load_documents().
"""

from pathlib import Path
import chromadb
from app.config import NOTES_DIR, CHROMA_DB_PATH
from app.embeddings import embed_texts


def load_documents(notes_dir: str) -> list[dict]:
    """
    Read every .txt file (add .pdf support later using pypdf) in notes_dir.

    Returns a list of dicts like:
        [{"source": "quicksort.txt", "text": "full file content..."}, ...]

    Things to think about when you write this:
    - What happens if a file is empty?
    - Should filenames become part of the metadata? (yes -- you'll want
      to know which file an answer came from later)
    """
    folder = Path(notes_dir)
    documents = []
    for file_path in folder.glob("*.txt"):

        content = file_path.read_text(encoding="utf-8")
        source = file_path.name  # e.g. "quicksort.txt", not "../data/notes/quicksort.txt"

        if content.strip():
            documents.append({"source": source, "text": content})

    return documents


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split a long piece of text into smaller overlapping chunks.

    Why chunks, not whole documents?
    - Embeddings work best on focused pieces of text, not huge documents
    - You want to retrieve just the relevant paragraph, not an entire file

    Why overlap?
    - Prevents cutting a sentence/idea in half exactly at a chunk boundary

    Think about: should you split by character count, word count, or by
    sentences/paragraphs? Each has trade-offs -- we'll discuss when you're here.
    """

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        piece = text[start:end]

        if piece.strip():
            chunks.append(piece)

        start = start + (chunk_size - overlap)

    return chunks


def embed_and_store(chunks: list[dict], db_path: str):
    """
    Turn each chunk into an embedding vector and store it in ChromaDB
    along with its source metadata.

    Steps you'll implement:
    1. Create/connect to a persistent Chroma client at db_path
    2. Create or get a collection (think of it like a table)
    3. For each chunk: encode it to a vector, then add it to the collection
       along with its text and source filename as metadata
    """

    # 1. Create/connect to persistent ChromaDB
    client = chromadb.PersistentClient(path=db_path)

    # Start fresh each time ingestion runs, so old/stale data never lingers
    try:
        client.delete_collection("notes")
    except Exception:
        pass  # collection didn't exist yet, nothing to delete

    # 2. Create or get the collection
    collection = client.get_or_create_collection("notes")

    # 3. Extract text from all chunks
    texts = [chunk["text"] for chunk in chunks]

    # Encode all texts at once
    vectors = embed_texts(texts)

    # 4. Build IDs
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    # Documents = original text
    documents = [chunk["text"] for chunk in chunks]

    # Metadata = source filename
    metadatas = [
        {"source": chunk["source"]}
        for chunk in chunks
    ]

    # 5. Store everything in ChromaDB
    collection.add(
        ids=ids,
        embeddings=vectors,
        documents=documents,
        metadatas=metadatas
    )


def run_ingestion(notes_dir: str, db_path: str) -> int:
    """
    Full ingestion pipeline: load -> chunk -> embed -> store.
    Returns the number of chunks stored, so callers can report it.
    """
    docs = load_documents(notes_dir)
    
    all_chunks = []
    for doc in docs:
        pieces = chunk_text(doc["text"])
        for piece in pieces:
            all_chunks.append({"text": piece, "source": doc["source"]})
    
    embed_and_store(all_chunks, db_path)

    return len(all_chunks)

if __name__ == "__main__":
    count = run_ingestion(NOTES_DIR, CHROMA_DB_PATH)
    print(f"Stored {count} chunks in the vector database.")
