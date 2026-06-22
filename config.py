import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH          = str(BASE_DIR / "data" / "chroma")
UPLOADS_PATH         = str(BASE_DIR / "data" / "uploads")
DATABASE_URL         = f"sqlite:///{BASE_DIR / 'college_rules.db'}"

EMBEDDING_MODEL      = "all-MiniLM-L6-v2"
OLLAMA_URL           = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

TOP_K                = 3
SIMILARITY_THRESHOLD = 0.20 
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "admin-secret-key-2024")