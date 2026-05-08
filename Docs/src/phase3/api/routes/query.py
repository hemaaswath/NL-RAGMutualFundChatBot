"""
Query route for Phase 3 API
"""

from fastapi import APIRouter, HTTPException
from ..models.schemas import QueryRequest, QueryResponse
from ..services.rag_service import RAGService
from ..utils.logger import get_logger

router = APIRouter(prefix="/api", tags=["query"])
logger = get_logger(__name__)


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a user query about mutual funds.
    
    Args:
        request: Query request with query text and optional scheme filter
    
    Returns:
        Query response with answer and metadata
    """
    try:
        logger.info(f"Processing query: {request.query}")
        if request.scheme:
            logger.info(f"Scheme filter: {request.scheme}")
        
        # Process query through RAG pipeline
        result = RAGService.process_query(
            query=request.query,
            scheme=request.scheme,
            use_cache=True
        )
        
        # Build response
        response = QueryResponse(
            answer=result.get("answer", ""),
            source_url=result.get("citations", [{}])[0].get("source_url") if result.get("citations") else None,
            last_updated=result.get("citations", [{}])[0].get("last_updated") if result.get("citations") else None,
            query_type=result.get("query_type", "unknown"),
            chunks_retrieved=result.get("chunks_retrieved", 0),
            cached=result.get("cached", False),
            refusal_type=result.get("refusal_type"),
            citations=result.get("citations")
        )
        
        logger.info(f"Query processed successfully: {request.query}")
        return response
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
