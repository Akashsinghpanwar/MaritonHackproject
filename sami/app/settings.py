from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

def _clean_key(k: str | None) -> str | None:
    if not k: return None
    k = k.strip().strip('"').strip("'")
    if "..." in k or k.startswith("OPENAI_") or len(k) < 20: return None
    return k

OPENAI_API_KEY = _clean_key(os.getenv("OPENAI_API_KEY"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")

USE_LOCAL_EMBEDDINGS = os.getenv("USE_LOCAL_EMBEDDINGS", "0") == "1"
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "0") == "1"

PKG_DIR = Path(__file__).resolve().parents[1]
BASE_DIR = PKG_DIR
STORAGE_DIR = BASE_DIR / "app" / "storage"
UPLOAD_DIR = STORAGE_DIR / "uploads"
VECTOR_DIR = STORAGE_DIR / "vector"
DATA_DIR = BASE_DIR / "data"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

# LlamaParse toggle/key
LLAMA_PARSE_ENABLED = os.getenv("LLAMA_PARSE_ENABLED", "1") == "1"
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
