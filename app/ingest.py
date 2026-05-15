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


def build_vectorstore():

    print("Loading documents...")

    # 1. Cargar web
    try:
        web_docs = WebBaseLoader([WEBSITE_URL]).load()
    except Exception as e:
        print(f"Error loading website: {e}")
        web_docs = []

    # 2. Cargar PDF
    pdf_docs = PyPDFLoader(PDF_PATH).load()

    # 3. Juntar documentos
    all_docs = web_docs + pdf_docs

    print(f"Total documents loaded: {len(all_docs)}")

    # 4. Splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(all_docs)

    print(f"Total chunks created: {len(chunks)}")

    # 5. Embeddings
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL
    )

    print("Creating embeddings and ChromaDB...")

    # 6. Crear ChromaDB
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )

    print("ChromaDB created successfully.")

    return vectorstore


def get_or_build_vectorstore():

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL
    )

    # Si ya existe la DB, cargarla
    if os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR):

        print("Loading existing ChromaDB...")

        return Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings
        )

    # Si no existe, construirla
    print("No existing ChromaDB found.")
    print("Building new vectorstore...")

    return build_vectorstore()