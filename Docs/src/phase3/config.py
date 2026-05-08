"""
Configuration for Phase 3: Backend API Development
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────
# Project Paths
# ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "Docs"

# ──────────────────────────────────────────────
# API Configuration
# ──────────────────────────────────────────────
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_TITLE = "RAG Mutual Fund FAQ Assistant API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "REST API for Mutual Fund FAQ Assistant using RAG"

# ──────────────────────────────────────────────
# CORS Configuration
# ──────────────────────────────────────────────
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
CORS_ALLOW_METHODS = os.getenv("CORS_ALLOW_METHODS", "*").split(",")
CORS_ALLOW_HEADERS = os.getenv("CORS_ALLOW_HEADERS", "*").split(",")

# ──────────────────────────────────────────────
# Rate Limiting
# ──────────────────────────────────────────────
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))  # requests per minute
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))  # seconds

# ──────────────────────────────────────────────
# Request Validation
# ──────────────────────────────────────────────
MAX_QUERY_LENGTH = int(os.getenv("MAX_QUERY_LENGTH", "500"))  # characters
MIN_QUERY_LENGTH = int(os.getenv("MIN_QUERY_LENGTH", "5"))  # characters
MAX_SCHEME_NAME_LENGTH = int(os.getenv("MAX_SCHEME_NAME_LENGTH", "100"))

# ──────────────────────────────────────────────
# Authentication (Optional)
# ──────────────────────────────────────────────
API_KEY_REQUIRED = os.getenv("API_KEY_REQUIRED", "false").lower() == "true"
API_KEY = os.getenv("API_KEY", "")

# ──────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "json")  # json or text

# ──────────────────────────────────────────────
# Timeout Configuration
# ──────────────────────────────────────────────
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))  # seconds
