"""
Error handling utilities for Phase 3 API
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from ..utils.logger import get_logger
from ..models.schemas import ErrorResponse

logger = get_logger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP Exception: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "detail": "An unexpected error occurred",
            "status_code": 500
        }
    )


async def validation_exception_handler(request: Request, exc):
    """Handle validation exceptions (Pydantic)."""
    logger.error(f"Validation error: {exc}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "detail": str(exc),
            "status_code": 422
        }
    )
