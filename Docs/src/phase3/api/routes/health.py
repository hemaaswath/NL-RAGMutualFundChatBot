"""
Health route for Phase 3 API
"""

from fastapi import APIRouter
from datetime import datetime
from ..models.schemas import HealthResponse
from phase3.config import API_VERSION

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return HealthResponse(
        status="healthy",
        version=API_VERSION,
        timestamp=datetime.utcnow().isoformat()
    )
