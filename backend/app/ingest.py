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
from sentence_transformers import SentenceTransformer
import chromadb


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
    raise NotImplementedError("Write me second.")


def embed_and_store(chunks: list[dict], db_path: str):
    """
    Turn each chunk into an embedding vector and store it in ChromaDB
    along with its source metadata.

    Steps you'll implement:
    1. Load the embedding model: SentenceTransformer("all-MiniLM-L6-v2")
    2. Create/connect to a persistent Chroma client at db_path
    3. Create or get a collection (think of it like a table)
    4. For each chunk: encode it to a vector, then add it to the collection
       along with its text and source filename as metadata
    """
    raise NotImplementedError("Write me third.")


if __name__ == "__main__":
    # This will become: load -> chunk -> embed_and_store
    # once the functions above are implemented.
    print("Ingestion pipeline not implemented yet. See TODOs above.")
