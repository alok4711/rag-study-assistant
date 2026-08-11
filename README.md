# RAG Study Assistant (with built-in evaluation)

A retrieval-augmented AI assistant that answers questions using your own
study notes, with a self-built evaluation layer that measures how good
its answers actually are.

Built by Alok Kumar as a placement portfolio project.

## Project status

- [ ] Phase 1: Ingestion pipeline (`ingest.py`)
- [ ] Phase 1: Retrieval (`retrieve.py`)
- [ ] Phase 1: Generation (`generate.py`)
- [ ] Phase 1: API server (`main.py`)
- [ ] Phase 1: React frontend
- [ ] Phase 2: Evaluation test set
- [ ] Phase 2: LLM-as-Judge scoring
- [ ] Phase 2: Experiment log (chunk size / prompt tuning results)

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then edit .env and add your Anthropic API key
```

## Project structure

```
rag-study-assistant/
├── backend/
│   ├── app/
│   │   ├── config.py      # loads settings from .env
│   │   ├── ingest.py      # loads notes -> chunks -> embeddings -> vector DB
│   │   ├── retrieve.py    # question -> relevant chunks
│   │   ├── generate.py    # question + chunks -> answer (via Claude API)
│   │   └── main.py        # FastAPI server tying it together
│   └── requirements.txt
├── data/
│   └── notes/             # put your .txt/.pdf notes here
├── eval/                  # Phase 2: evaluation framework goes here
└── frontend/              # React UI, built in Week 2
```

## How to get an Anthropic API key

1. Go to https://console.anthropic.com/
2. Sign up / log in, go to "API Keys"
3. Create a new key, paste it into `backend/.env` as ANTHROPIC_API_KEY

## Why these tools

- **sentence-transformers**: generates embeddings locally, free, no API
  key needed for this part (only generation uses the paid API)
- **ChromaDB**: lightweight local vector database, no separate server needed
- **FastAPI**: simple Python web framework for the backend API
- **Anthropic API**: generates the actual answers using retrieved context
