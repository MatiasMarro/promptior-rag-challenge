import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from langserve import add_routes

from app.chain import rag_chain


app = FastAPI(
    title="Promtior RAG API",
    version="1.1.0",
    description="A chatbot that answers questions about Promtior using RAG architecture.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "Promtior RAG API is running.",
        "playground": "/promtior/playground",
        "docs": "/docs",
    }


add_routes(
    app,
    rag_chain.with_types(input_type=str, output_type=str),
    path="/promtior",
)


# --- Frontend estático (SPA) ---
# Se sirve la app de React buildeada desde web/dist para mantener un solo
# servicio en Railway. El bloque está guardado por os.path.exists para no
# romper el desarrollo local (donde web/dist puede no existir todavía).
#
# Importante: este catch-all se registra DESPUÉS de /health, /promtior/* y de
# las rutas internas de FastAPI (/docs, /openapi.json). FastAPI evalúa las
# rutas en orden de registro, así que esas rutas explícitas tienen prioridad
# y no quedan tapadas por el fallback de la SPA.
WEB_DIST = "web/dist"

if os.path.exists(WEB_DIST):
    app.mount(
        "/assets",
        StaticFiles(directory=os.path.join(WEB_DIST, "assets")),
        name="assets",
    )

    @app.get("/{full_path:path}")
    def spa_fallback(full_path: str):
        candidate = os.path.join(WEB_DIST, full_path)
        if full_path and os.path.isfile(candidate):
            return FileResponse(candidate)
        return FileResponse(os.path.join(WEB_DIST, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
