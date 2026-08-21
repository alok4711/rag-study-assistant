"""
API SERVER
Exposes your RAG pipeline as a web API so the React frontend (built later,
Week 2) can call it.

This file is mostly wiring -- the real work happens in retrieve.py and
generate.py. We'll fill this in once those two are working.
"""

from fastapi import FastAPI
from pydantic import BaseModel

from app.retrieve import retrieve_relevant_chunks
from app.generate import generate_answer
from app.config import CHROMA_DB_PATH

app = FastAPI(title="RAG Study Assistant")


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
