from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

OLLAMA_MODEL = "llama3"

CHROMA_DIR = BASE_DIR / "rag_db"

UPLOAD_DIR = BASE_DIR / "uploads"

POSTGRES_URL = "postgresql://postgres:postgres@localhost/primeiro_llm"nano backend/app/core/config.py
