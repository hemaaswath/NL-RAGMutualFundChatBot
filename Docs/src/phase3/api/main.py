"""
Main FastAPI application for Phase 3
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from phase3.config import (
    API_TITLE, API_VERSION, API_DESCRIPTION, API_HOST, API_PORT,
    CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
)
from phase3.api.routes import query, schemes, health, feedback
from phase3.api.utils.logger import get_logger
from phase3.api.utils.error_handlers import (
    http_exception_handler,
    general_exception_handler,
    validation_exception_handler
)

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    logger.info("Starting RAG Mutual Fund FAQ Assistant API...")
    yield
    logger.info("Shutting down RAG Mutual Fund FAQ Assistant API...")


# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include routers
app.include_router(query.router)
app.include_router(schemes.router)
app.include_router(health.router)
app.include_router(feedback.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "RAG Mutual Fund FAQ Assistant API",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/api/health"
    }


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {API_HOST}:{API_PORT}")
    uvicorn.run(
        "phase3.api.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )
