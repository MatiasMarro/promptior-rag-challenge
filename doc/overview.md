# Promtior RAG Chatbot — Project Overview

## Approach

Built a chatbot that answers questions about Promtior using the RAG (Retrieval-Augmented Generation) architecture. The bot indexes two sources — the Promtior website (https://promtior.ai/) and the challenge PDF — into a ChromaDB vector store. At query time, it retrieves the top-4 most semantically similar chunks and passes them as context to gpt-4o-mini, which generates the final answer.

## Implementation

The solution is composed of four main modules:

**1. Ingestion pipeline (`app/ingest.py`)**
Loads the website with `WebBaseLoader` and the PDF with `PyPDFLoader`, splits them with `RecursiveCharacterTextSplitter` (chunk_size=1000, overlap=200), embeds each chunk using `text-embedding-3-small`, and persists the result in a local ChromaDB at `./chroma_db`. The function `get_or_build_vectorstore()` checks if the index already exists on disk and loads it instead of rebuilding — this avoids re-indexing on every cold start.

**2. RAG chain (`app/chain.py`)**
Built with LangChain Expression Language (LCEL). The chain takes a question, retrieves the top-4 chunks in parallel with passing the question through via `RunnableParallel`, formats both into a prompt template, sends it to gpt-4o-mini (temperature=0), and parses the output to a plain string with `StrOutputParser`.

**3. Prompt template (`app/prompts.py`)**
A strict system prompt that instructs the model to use ONLY the provided context and respond with "I don't have that information." when the answer is not in the context. Combined with temperature=0, this keeps responses deterministic and grounded.

**4. REST API (`server.py`)**
Exposes the chain via LangServe's `add_routes`, which automatically provides `/invoke`, `/batch`, `/stream`, and `/playground` endpoints under `/promptior`. CORS is enabled for all origins.

## Key Decisions

**LCEL over legacy chain classes**
Used modern LCEL syntax (the `|` operator) instead of deprecated patterns like `RetrievalQA.from_chain_type`. LCEL provides streaming, batch, and async support out of the box, and is the API LangChain will support going forward.

**ChromaDB over Pinecone or FAISS**
ChromaDB is embedded in the process (no external service), persists to disk, and integrates natively with LangChain. Appropriate for the scale of this project.

**gpt-4o-mini over gpt-4**
The task is information extraction, not complex reasoning. gpt-4o-mini is significantly cheaper and quality is virtually identical for this use case.

**chunk_size=1000, overlap=200**
Balance between retrieval precision (smaller chunks = better semantic matches) and context richness (larger chunks = more complete information per result).

**k=4 retrieval**
Enough context for multi-part questions without overwhelming the LLM with irrelevant chunks.

**temperature=0**
Deterministic responses, ideal for factual retrieval. Reduces the risk of the model elaborating beyond the context.

## Challenges and Solutions

**The website renders content with JavaScript**
`WebBaseLoader` uses `requests` + BeautifulSoup, which only sees static HTML — most of the page content was missing on first load. Solution: complemented the website data with the challenge PDF, which contains all the key information (founding date, services, client list, case studies).

**LLM answering from prior knowledge**
In early tests, when asked about Promtior's founding date, the model would produce confident but incorrect answers from its training data. Solution: hardened the system prompt with explicit "Use ONLY the context. Do NOT use prior knowledge." instructions, combined with temperature=0.

**Cold start on first deploy**
The first request after a Railway deploy triggered a full vectorstore rebuild (web scraping + PDF loading + embedding + persistence), causing 30-60 second delays. Solution: implemented `get_or_build_vectorstore()` that checks for an existing `./chroma_db` directory before building. Subsequent deploys load the persisted index instead.

**Pydantic v1/v2 compatibility**
Early versions of LangServe had conflicts with Pydantic v2. Solution: pinned `langserve[server]==0.3.1` in `requirements.txt` to ensure compatibility.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11 |
| LLM | OpenAI gpt-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector Store | ChromaDB 0.5.23 |
| RAG Framework | LangChain 0.3.27 + LCEL |
| API Layer | FastAPI 0.115.6 + LangServe 0.3.1 |
| Deployment | Railway |

## Project Structure

```
.
├── server.py              # FastAPI + LangServe entrypoint
├── Procfile               # Railway start command
├── requirements.txt
├── .env.example
├── app/
│   ├── config.py          # environment variables and constants
│   ├── ingest.py          # document loading and indexing
│   ├── prompts.py         # prompt template
│   └── chain.py           # RAG chain (LCEL)
├── data/
│   └── AI_Engineer.pdf
├── doc/
│   ├── overview.md        # this file
│   └── architecture.png   # component diagram
└── tests/
    └── test_chain.py
```

## Live Endpoints

- API: https://promptior-rag-challenge-production.up.railway.app
- Playground: https://promptior-rag-challenge-production.up.railway.app/promptior/playground/
- Docs: https://promptior-rag-challenge-production.up.railway.app/docs
