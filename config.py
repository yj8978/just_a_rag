from pathlib import Path

BASE_DIR = Path(__file__).parent

DOCUMENTS_PATH = BASE_DIR / "documents"
CHROMA_PATH = BASE_DIR / "data" / "chroma_db"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "documents"

TOP_K = 3
CHUNK_THRESHOLD = 0.7
MAX_TOKENS = 500

LLM_MODEL = "qwen3:8b"