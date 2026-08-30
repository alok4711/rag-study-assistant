"""
API SERVER
Exposes your RAG pipeline as a web API so the React frontend (built later,
Week 2) can call it.

This file is mostly wiring -- the real work happens in retrieve.py and
generate.py. We'll fill this in once those two are working.
"""

from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.retrieve import retrieve_relevant_chunks
from app.generate import generate_answer
from app.config import NOTES_DIR, CHROMA_DB_PATH
from app.ingest import run_ingestion

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="RAG Study Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(req: QuestionRequest):
    chunks = retrieve_relevant_chunks(req.question, CHROMA_DB_PATH)
    answer = generate_answer(req.question, chunks)
    return {"answer": answer, "sources": [c["source"] for c in chunks]}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    # 1. Validate file type
    if not file.filename or not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are allowed"
        )

    # 2. Get safe filename
    filename = Path(file.filename).name

    # 3. Read uploaded file
    contents = await file.read()

    # 4. Save file to notes directory
    file_path = Path(NOTES_DIR) / filename
    file_path.write_bytes(contents)


    count = run_ingestion(NOTES_DIR, CHROMA_DB_PATH)
    return {"message": f"Uploaded and indexed {filename}", "chunks_indexed": count}
