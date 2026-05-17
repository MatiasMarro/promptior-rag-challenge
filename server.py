from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

from app.chain import rag_chain


app = FastAPI(
    title="Promtior RAG API",
    version="1.0",
    description="A chatbot that answers questions about Promtior using RAG architecture.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

@app.get("/")
def root():
    return{
        "status": "ok",
        "message": "Welcome to the Promtior RAG API! Use the /ask endpoint to interact with the chatbot.",
        "playground": "/playground",
        "docs": "/docs",
    }

add_routes(
    app,
    rag_chain.with_types(input_type=str, output_type=str),
    path="/promptior",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)