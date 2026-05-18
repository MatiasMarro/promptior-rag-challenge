# Promtior RAG Challenge

Chatbot basado en RAG (Retrieval-Augmented Generation) que responde preguntas sobre Promtior a partir de documentos indexados: el sitio web oficial y un PDF técnico.

## Stack

- **FastAPI + LangServe**: API REST con endpoints para el chain y playground interactivo
- **LangChain (LCEL)**: Orquestación del pipeline RAG
- **OpenAI**: GPT-4o-mini como LLM, text-embedding-3-small para embeddings
- **ChromaDB**: Vector store persistente en disco

## Instalación local

Requisitos: Python 3.10+, `OPENAI_API_KEY` disponible.

```bash
git clone https://github.com/your-org/promptior-rag-challenge.git
cd promptior-rag-challenge

python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\Activate.ps1     # Windows

pip install -r requirements.txt

cp .env.example .env
# Completar OPENAI_API_KEY en .env

python server.py
```

Servidor disponible en `http://localhost:8000`.

## Frontend

El frontend es una SPA en **Vite + React 18 + TypeScript + Tailwind**, ubicada
en `web/`. En producción la misma app de FastAPI sirve el build estático
(`web/dist`), así que Railway sigue siendo un único servicio. La lógica RAG no
cambia: el frontend solo consume `POST /promtior/invoke`.

### Desarrollo (dos terminales)

```bash
# Terminal 1 — backend
python server.py

# Terminal 2 — frontend (con proxy a :8000)
cd web
npm install
npm run dev          # http://localhost:5173
```

### Build de producción

```bash
cd web
npm run build        # genera web/dist
```

Con `web/dist` presente, `python server.py` sirve la SPA en `GET /` y mantiene
intactos `/promtior/*`, `/docs` y `/health`.

> El logo oficial de Promtior está en `web/public/logo.svg` (se usa en el
> header, el empty state y el favicon).

## Endpoints

| Método | Path | Descripción |
|--------|------|-------------|
| GET | `/` | SPA (frontend React) si `web/dist` existe |
| GET | `/health` | Health check (JSON de estado) |
| GET | `/docs` | Swagger UI |
| GET | `/promptior/playground/` | Playground interactivo de LangServe |
| POST | `/promptior/invoke` | Ejecutar una query contra el RAG chain |

### Ejemplo de uso

```bash
curl -X POST http://localhost:8000/promptior/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": "¿Qué es Promtior?"}'
```

```json
{"output": "Promtior es una empresa de consultoría tecnológica..."}
```

## Arquitectura

```
server.py
    └── app/chain.py          <- RAG chain (LCEL)
        ├── app/config.py     <- Variables de entorno
        ├── app/prompts.py    <- Prompt template
        └── app/ingest.py     <- Carga y vectorización de documentos
            ├── Web: promtior.ai
            ├── PDF: data/AI_Engineer.pdf
            └── Persistencia: ./chroma_db/
```

El vectorstore se construye en el primer arranque. Los siguientes usan el índice ya persistido.

## Configuración

Ver [.env.example](.env.example) para todas las variables disponibles. Las obligatorias son:

```env
OPENAI_API_KEY=sk-...
```

El resto tiene valores por defecto funcionales.

## Dependencias principales

| Package | Version |
|---------|---------|
| fastapi | 0.115.6 |
| langchain | 0.3.27 |
| langchain-openai | 0.2.14 |
| langserve[server] | 0.3.1 |
| chromadb | 0.5.23 |
| uvicorn[standard] | 0.34.0 |

## Deployment

El proyecto está configurado para Railway. Ver [DEPLOYMENT.md](DEPLOYMENT.md) para la guía completa.

URL de producción: https://promptior-rag-challenge-production.up.railway.app

## Troubleshooting

**`ValueError: OPENAI_API_KEY no configurada`**
Agregar la variable en `.env` (local) o en Railway Variables (producción).

**502 Bad Gateway en Railway**
Esperar 30-60 segundos luego del deploy. El primer arranque tarda por la construcción del vectorstore. Si persiste, revisar los logs desde el dashboard.

**Vectorstore corrupto o vacío**
Eliminar `./chroma_db/` y reiniciar. Se reconstruye automáticamente.

---

Versión 1.0 — Mayo 2026

