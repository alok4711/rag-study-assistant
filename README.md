# RAG Study Assistant

A retrieval-augmented AI study assistant that answers questions from your own notes — with a built-in LLM-as-Judge evaluation framework that scores answer quality automatically.

Built by Alok Kumar.

**Live app:** https://rag-study-assistant-one.vercel.app
**API:** https://rag-backend-qx3e.onrender.com

*(The backend is on a free tier and sleeps after 15 minutes of inactivity — the first request may take 30-60 seconds while it wakes up.)*

## What it does

- Upload your own `.txt` notes — the app chunks, embeds, and indexes them for search
- Ask questions in plain English (or by voice) — answers are generated only from your notes, with source citations, and the model explicitly says "I don't know" when your notes don't cover something
- Upload a CSV of test questions with expected answers, and the built-in Judge automatically scores how well the assistant performs, with per-question reasoning — turning "it works" into a measured, repeatable evaluation

## Architecture

User (browser)
|
v
React frontend (Vercel)
| fetch()
v
FastAPI backend (Render)
|
|-- /ask -> retrieve relevant chunks -> Gemini generates grounded answer
|-- /upload -> chunk + embed new notes -> store in ChromaDB
|-- /evaluate -> run test questions through the pipeline -> Gemini judges each answer
|
v
ChromaDB (vector store) + Gemini API (embeddings + generation + judging)

Embeddings are generated via the Gemini API rather than a locally-hosted model — this was a deliberate change after the local `sentence-transformers`/`torch` setup caused out-of-memory crashes on free-tier hosting (512MB RAM). Moving embedding generation to an API call removed the heaviest dependency entirely.

## Tech stack

- **Backend:** FastAPI, ChromaDB, Gemini API (embeddings + generation + evaluation judging)
- **Frontend:** React (Vite), React Router
- **Hosting:** Render (backend), Vercel (frontend)

## Project structure

rag-study-assistant/
├── backend/
│ └── app/
│   ├── config.py # environment-based settings
│   ├── embeddings.py # Gemini embedding calls
│   ├── ingest.py # load -> chunk -> embed -> store pipeline
│   ├── retrieve.py # semantic search over stored notes
│   ├── generate.py # grounded answer generation with citations
│   ├── evaluate.py # LLM-as-Judge evaluation pipeline
│   └── main.py # FastAPI app: /ask, /upload, /evaluate
├── data/notes/ # sample notes
└── frontend/
  └── src/
    ├── pages/
    │ ├── AskPage.jsx # ask questions, upload notes, voice input
    │ └── EvaluatePage.jsx # upload CSV test sets, view scored results
    └── App.jsx # routing + navbar


## Running locally

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # add your Gemini API key
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env          # set VITE_API_URL to your backend URL
npm run dev
```

Get a free Gemini API key at https://aistudio.google.com — no credit card required.

## What I'd build next

- User accounts, so notes and evaluation history are saved per user instead of shared globally
- PDF note support (currently `.txt` only)
- Persistent storage for the vector database on the hosting side (currently rebuilds on every server restart, a workaround for free-tier ephemeral disk)