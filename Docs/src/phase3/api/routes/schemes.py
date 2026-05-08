"""
Schemes route for Phase 3 API
"""

from fastapi import APIRouter
from ..models.schemas import SchemesResponse
from ..services.rag_service import RAGService
from ..utils.logger import get_logger

router = APIRouter(prefix="/api", tags=["schemes"])
logger = get_logger(__name__)


@router.get("/schemes", response_model=SchemesResponse)
async def get_schemes():
    """
    Get list of available mutual fund schemes.
    
    Returns:
        List of scheme names
    """
    try:
        schemes = RAGService.get_schemes()
        logger.info(f"Retrieved {len(schemes)} schemes")
        
        return SchemesResponse(
            schemes=schemes,
            count=len(schemes)
        )
    
    except Exception as e:
        logger.error(f"Error retrieving schemes: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving schemes: {str(e)}")
