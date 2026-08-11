"""
API SERVER
Exposes your RAG pipeline as a web API so the React frontend (built later,
Week 2) can call it.

This file is mostly wiring -- the real work happens in retrieve.py and
generate.py. We'll fill this in once those two are working.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="RAG Study Assistant")


class QuestionRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(req: QuestionRequest):
    """
    TODO once retrieve.py and generate.py are done:
    1. chunks = retrieve_relevant_chunks(req.question, ...)
    2. answer = generate_answer(req.question, chunks)
    3. return {"answer": answer, "sources": [c["source"] for c in chunks]}
    """
    return {"answer": "Not implemented yet", "sources": []}
