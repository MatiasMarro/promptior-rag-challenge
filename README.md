# Promtior RAG Challenge

RAG (Retrieval-Augmented Generation) chatbot that answers questions about
Promtior from indexed documents: the official website and a technical PDF.
It ships with a custom React frontend served by the same FastAPI app.

## Stack

- **FastAPI + LangServe**: REST API with endpoints for the chain and an interactive playground
- **LangChain (LCEL)**: RAG pipeline orchestration
- **OpenAI**: GPT-4o-mini as LLM, text-embedding-3-small for embeddings
- **ChromaDB**: on-disk persistent vector store
- **Vite + React 18 + TypeScript + Tailwind**: single-page chat UI

## Local setup

Requirements: Python 3.11+, an available `OPENAI_API_KEY`.

```bash
git clone https://github.com/MatiasMarro/promptior-rag-challenge.git
cd promptior-rag-challenge

python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\Activate.ps1     # Windows

pip install -r requirements.txt

cp .env.example .env
# Fill in OPENAI_API_KEY in .env

python server.py
```

Server available at `http://localhost:8000`.


## Frontend

The frontend is a SPA built with **Vite + React 18 + TypeScript + Tailwind**,
located in `web/`. In production the same FastAPI app serves the static build
(`web/dist`), so Railway stays a single service. The RAG logic is untouched:
the frontend only consumes `POST /promtior/invoke`.

### Development (two terminals)

```bash
# Terminal 1 — backend
python server.py

# Terminal 2 — frontend (proxied to :8000)
cd web
npm install
npm run dev          # http://localhost:5173
```

### Production build

```bash
cd web
npm run build        # generates web/dist
```

With `web/dist` present, `python server.py` serves the SPA at `GET /` while
keeping `/promtior/*`, `/docs` and `/health` intact.

> The official Promtior logo lives at `web/public/logo.svg` (used in the
> header, the empty state and the favicon).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | SPA (React frontend) when `web/dist` exists |
| GET | `/health` | Health check (status JSON) |
| GET | `/docs` | Swagger UI |
| GET | `/promtior/playground/` | LangServe interactive playground |
| POST | `/promtior/invoke` | Run a query against the RAG chain |

### Usage example

```bash
curl -X POST http://localhost:8000/promtior/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": "What is Promtior?"}'
```

```json
{"output": "Promtior is a technology consulting company..."}
```

## Architecture

```
server.py
    └── app/chain.py          <- RAG chain (LCEL)
        ├── app/config.py     <- Configuration
        ├── app/prompts.py    <- Prompt template
        └── app/ingest.py     <- Document loading and vectorization
            ├── Web: promtior.ai
            ├── PDF: data/AI_Engineer.pdf
            └── Persistence: ./chroma_db/
```

The vector store is built on first startup; subsequent boots reuse the
persisted index. `chroma_db/` is intentionally not committed, so a fresh
deploy rebuilds it on the first boot.

## Configuration

See [.env.example](.env.example). The only required variable is:

```env
OPENAI_API_KEY=sk-...
```

The rest have working defaults (see `app/config.py`).

## Main dependencies

| Package | Version |
|---------|---------|
| fastapi | 0.115.6 |
| langchain | 0.3.27 |
| langchain-openai | 0.2.14 |
| langserve[server] | 0.3.1 |
| chromadb | 0.5.23 |
| uvicorn[standard] | 0.34.0 |

## Deployment

Deployed on Railway using the multi-stage [Dockerfile](Dockerfile) (Node stage
builds the SPA, Python stage serves everything). Railway setup:

- **Settings → Build → Builder = Dockerfile** (Railpack, the default builder,
  ignores `nixpacks.toml` and never builds the frontend)
- **Settings → Deploy → Healthcheck Path = `/health`**, timeout `~300s`
  (first boot rebuilds the vector store since `chroma_db/` is not committed)
- **Variables → `OPENAI_API_KEY`** (the only env var read by the app)

The container's `CMD` binds `$PORT`. `nixpacks.toml` is inert under the
Dockerfile builder (kept only as a fallback if the builder is switched).

Production URL: https://promtior-rag-challenge-production.up.railway.app

## Troubleshooting

**`ValueError: OPENAI_API_KEY no configurada`**
Add the variable to `.env` (local) or Railway Variables (production).

**502 Bad Gateway / slow first request on Railway**
Wait 30–90 seconds after a deploy: the first boot rebuilds the vector store
(`chroma_db/` is not committed). If it persists, check the deploy logs.

**Corrupt or empty vector store**
Delete `./chroma_db/` and restart. It is rebuilt automatically.

**Swagger UI at `/docs` renders empty**
Known pre-existing issue: `/openapi.json` can 500 due to a LangServe/Pydantic
schema-generation mismatch. `/promtior/invoke` and `/promtior/playground/`
work normally.

---

Version 1.1 — May 2026
