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

print(f"""
Configuración cargada:
LLM_MODEL={LLM_MODEL}
EMBEDDING_MODEL={EMBEDDING_MODEL}
LLM_TEMPERATURE={LLM_TEMPERATURE}
CHROMA_DIR={CHROMA_DIR}
PDF_PATH={PDF_PATH}
WEBSITE_URL={WEBSITE_URL}
LANGSMITH_TRACING={LANGSMITH_TRACING}
LANGSMITH_PROJECT={LANGSMITH_PROJECT}
CHUNK_SIZE={CHUNK_SIZE}
CHUNK_OVERLAP={CHUNK_OVERLAP}
TOP_K={TOP_K}
""")