"""
Configuration for Phase 1: Data Collection & Corpus Preparation.

Contains all URLs, scheme mappings, constants, and directory paths.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────
# Project Paths
# ──────────────────────────────────────────────

# For Streamlit Cloud deployment, use relative paths
import sys
from pathlib import Path

# Debug: Log environment info
import logging
logger = logging.getLogger(__name__)
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"STREAMLIT_SERVER_PORT: {os.getenv('STREAMLIT_SERVER_PORT')}")
logger.info(f"streamlit in sys.modules: {'streamlit' in sys.modules}")

# Check if we're on Streamlit Cloud (different working directory)
# Also check if we're in a containerized environment
is_streamlit_cloud = (
    os.getenv("STREAMLIT_SERVER_PORT") or 
    "streamlit" in sys.modules or
    os.getenv("STREAMLIT_SHARING") or
    "/app" in os.getcwd()  # Common container path
)
logger.info(f"Detected Streamlit Cloud: {is_streamlit_cloud}")

if is_streamlit_cloud:
    # On Streamlit Cloud, use relative paths
    PROJECT_ROOT = Path(".")
    logger.info("Using relative paths for Streamlit Cloud")
else:
    # Local development, use absolute paths
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
    logger.info("Using absolute paths for local development")

DATA_RAW_DIR = Path(os.getenv("DATA_RAW_DIR", PROJECT_ROOT / "data" / "raw"))
DATA_PROCESSED_DIR = Path(os.getenv("DATA_PROCESSED_DIR", PROJECT_ROOT / "data" / "processed"))
DATA_CHUNKS_DIR = Path(os.getenv("DATA_CHUNKS_DIR", PROJECT_ROOT / "data" / "chunks"))
# Use relative path for ChromaDB to work on Streamlit Cloud deployment
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
DOCS_PHASE1_DIR = PROJECT_ROOT / "Docs" / "Phase1_DataCollection"

# ──────────────────────────────────────────────
# Scheme Definitions
# ──────────────────────────────────────────────

SCHEMES = [
    {
        "name": "HDFC Mid-Cap Fund (Direct Growth)",
        "slug": "hdfc-mid-cap-fund-direct-growth",
        "url": "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
        "category": "Mid Cap",
        "document_type": "scheme_page",
    },
    {
        "name": "HDFC Equity Fund (Direct Growth)",
        "slug": "hdfc-equity-fund-direct-growth",
        "url": "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
        "category": "Multi Cap",
        "document_type": "scheme_page",
    },
    {
        "name": "HDFC Focused Fund (Direct Growth)",
        "slug": "hdfc-focused-fund-direct-growth",
        "url": "https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth",
        "category": "Focused",
        "document_type": "scheme_page",
    },
    {
        "name": "HDFC ELSS Tax Saver Fund (Direct Plan Growth)",
        "slug": "hdfc-elss-tax-saver-fund-direct-plan-growth",
        "url": "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth",
        "category": "ELSS",
        "document_type": "scheme_page",
    },
    {
        "name": "HDFC Large-Cap Fund (Direct Growth)",
        "slug": "hdfc-large-cap-fund-direct-growth",
        "url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
        "category": "Large Cap",
        "document_type": "scheme_page",
    },
]

# ──────────────────────────────────────────────
# Scraping Configuration
# ──────────────────────────────────────────────

SCRAPE_DELAY_MIN = int(os.getenv("SCRAPE_DELAY_MIN", "2"))
SCRAPE_DELAY_MAX = int(os.getenv("SCRAPE_DELAY_MAX", "5"))
SCRAPE_MAX_RETRIES = int(os.getenv("SCRAPE_MAX_RETRIES", "3"))

# ──────────────────────────────────────────────
# Chunking Configuration
# ──────────────────────────────────────────────

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "750"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
TOKENIZER_MODEL = "cl100k_base"  # Used by text-embedding-3-small

# ──────────────────────────────────────────────
# Embedding Configuration
# ──────────────────────────────────────────────

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "384"))

# ──────────────────────────────────────────────
# ChromaDB Configuration
# ──────────────────────────────────────────────

CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "mutual_fund_faq")

# ──────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
