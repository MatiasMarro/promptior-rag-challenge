import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no configurada")

# LangSmith
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "default-project")

# Modelos
LLM_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_TEMPERATURE = 0

# Paths
CHROMA_DIR = "./chroma_db"
PDF_PATH = "./data/AI_Engineer.pdf"

# URLs
WEBSITE_URL = "https://promtior.ai/"

# --- Retrieval ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 4