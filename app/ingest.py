import os

from app.config import (
    CHROMA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    PDF_PATH,
    WEBSITE_URL
)

from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

def _load_documents():
    """Carga las dos fuentes (web + PDF) y devuelve una lista unificada de Documents."""
    print(f"[ingest] Loading web: {WEBSITE_URL}")
    web_docs = WebBaseLoader([WEBSITE_URL]).load()
    print(f"[ingest] Web docs loaded: {len(web_docs)} documents, "
          f"{sum(len(d.page_content) for d in web_docs)} chars total")
    
    print(f"[ingest] Loading PDF: {PDF_PATH}")
    pdf_docs = PyPDFLoader(PDF_PATH).load()
    print(f"[ingest] PDF docs loaded: {len(pdf_docs)} pages")
    
    return web_docs + pdf_docs



def _split_documents(documents):
    """Parte los documentos en chunks usando RecursiveCharacterTextSplitter."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"[ingest] Split into {len(chunks)} chunks")
    return chunks


def build_vectorstore():
    """Construye el vectorstore desde cero. Borra el índice anterior si existe."""
    documents = _load_documents()
    chunks = _split_documents(documents)
    
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    
    print(f"[ingest] Embedding {len(chunks)} chunks and persisting to {CHROMA_DIR}")
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        )
    print(f"[ingest] Vectorstore built successfully")
    return vectorstore


def get_or_build_vectorstore():
    """
    Si ya existe el índice en disco, lo carga. Si no, lo construye.
    """
    if os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR):
        print(f"[ingest] Loading existing vectorstore from {CHROMA_DIR}")
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
        )
        
    print(f"[ingest] No existing vectorstore found, building from scratch")
    return build_vectorstore()

if __name__ == "__main__":
    # Permite correr "python -m app.ingest" para construir el índice manualmente
    get_or_build_vectorstore()
