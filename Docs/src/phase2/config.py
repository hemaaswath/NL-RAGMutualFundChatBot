"""
Configuration for Phase 2: RAG Pipeline Implementation
"""

import os
from pathlib import Path

# Try to load from .env for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Helper function to get config from st.secrets or environment variables
def get_config(key, default=""):
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except:
        pass
    return os.getenv(key, default)

# ──────────────────────────────────────────────
# Project Paths
# ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "Docs"
DATA_DIR = PROJECT_ROOT / "data"

# ──────────────────────────────────────────────
# Vector Database Configuration
# ──────────────────────────────────────────────
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "mutual_fund_faq")

# ──────────────────────────────────────────────
# Retrieval Configuration
# ──────────────────────────────────────────────
TOP_K = int(os.getenv("TOP_K", "5"))  # Number of results to retrieve
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))  # Minimum similarity score (lowered for better recall)
MAX_CONTEXT_TOKENS = int(os.getenv("MAX_CONTEXT_TOKENS", "2000"))  # Max tokens in context

# ──────────────────────────────────────────────
# LLM Configuration
# ──────────────────────────────────────────────
# Using Groq for LLM (already configured in Phase 1)
GROQ_API_KEY = get_config("GROQ_API_KEY", "")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")  # Groq model
MAX_RESPONSE_LENGTH = int(os.getenv("MAX_RESPONSE_LENGTH", "200"))  # Max characters in response
MAX_SENTENCES = int(os.getenv("MAX_SENTENCES", "3"))  # Max sentences in response

# ──────────────────────────────────────────────
# Response Configuration
# ──────────────────────────────────────────────
RESPONSE_STYLE = os.getenv("RESPONSE_STYLE", "factual_only")  # factual_only, advisory_allowed
INCLUDE_CITATIONS = os.getenv("INCLUDE_CITATIONS", "true").lower() == "true"
INCLUDE_FOOTER = os.getenv("INCLUDE_FOOTER", "true").lower() == "true"

# ──────────────────────────────────────────────
# Cache Configuration
# ──────────────────────────────────────────────
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # Cache TTL in seconds (1 hour)
CACHE_DIR = PROJECT_ROOT / "cache"

# ──────────────────────────────────────────────
# Query Classification
# ──────────────────────────────────────────────
ADVISORY_KEYWORDS = [
    "should i", "should i invest", "recommend", "advice", "best",
    "which fund is better", "which is better", "compare", "performance comparison",
    "buy", "sell", "hold", "investment advice", "suggest",
    "good investment", "is this a good", "better for", "which fund should",
    "which mutual fund is better", "which fund", "better", "comparison",
    "give money", "money", "invest money", "put money", "how much money"
]

FACTUAL_KEYWORDS = [
    "what is", "how much", "expense ratio", "nav", "exit load",
    "minimum investment", "fund manager", "benchmark", "aum",
    "category", "type", "details", "information"
]

# ──────────────────────────────────────────────
# Refusal Templates
# ──────────────────────────────────────────────
COMPLIANCE_MESSAGE = (
    "I cannot provide investment advice, recommendations, or comparisons. "
    "For personalized guidance, please consult a SEBI-registered investment advisor."
)

REFUSAL_TEMPLATES = {
    "investment_advice": COMPLIANCE_MESSAGE,
    "performance_comparison": COMPLIANCE_MESSAGE,
    "recommendation_request": COMPLIANCE_MESSAGE,
    "default": COMPLIANCE_MESSAGE
}

# ──────────────────────────────────────────────
# System Prompt
# ──────────────────────────────────────────────
SYSTEM_PROMPT = """You are a factual mutual fund information assistant. Your role is to:

1. Answer questions using ONLY the provided context from official fund documents
2. Provide concise, factual responses (maximum 3 sentences)
3. Never give investment advice, recommendations, or comparisons
4. Never suggest which fund to buy, sell, or hold
5. Include the source URL from the context
6. If the answer is not in the context, state that clearly

Strict Rules:
- Do not use phrases like "you should", "I recommend", "consider investing"
- Do not compare funds or declare one better than another
- Do not provide any form of financial advice
- Only state facts from the provided documents"""

# ──────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
