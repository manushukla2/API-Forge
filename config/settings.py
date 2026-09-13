import os
from dotenv import load_dotenv

load_dotenv()

# App
APP_NAME    = "APIForge"
APP_VERSION = "0.1.0"

# ── AI Framework ──────────────────────────────────────
# direct | langchain | langgraph
AI_FRAMEWORK = os.getenv("AI_FRAMEWORK", "direct")

# ── LLM Backend ───────────────────────────────────────
# groq | openai | ollama
AI_LLM = os.getenv("AI_LLM", "groq")

# ── Groq ──────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL   = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# ── OpenAI ────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4o")

# ── Ollama (local) ────────────────────────────────────
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL", "llama3")

# ── Paths ─────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR      = os.path.join(BASE_DIR, "data")
SESSIONS_DIR  = os.path.join(DATA_DIR, "sessions")
REPORTS_DIR   = os.path.join(DATA_DIR, "reports")
CAPTURES_DIR  = os.path.join(DATA_DIR, "captures")
TEMPLATES_DIR = os.path.join(DATA_DIR, "templates")

# ── HTTP ──────────────────────────────────────────────
DEFAULT_TIMEOUT   = 30
DEFAULT_RETRIES   = 3
MAX_RESPONSE_SIZE = 10 * 1024 * 1024

# Ensure dirs exist
for _dir in [SESSIONS_DIR, REPORTS_DIR, CAPTURES_DIR, TEMPLATES_DIR]:
    os.makedirs(_dir, exist_ok=True)
