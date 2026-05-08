"""
Feedback route for Phase 3 API
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from ..models.schemas import FeedbackRequest, FeedbackResponse
from ..utils.logger import get_logger

router = APIRouter(prefix="/api", tags=["feedback"])
logger = get_logger(__name__)


# In-memory feedback storage (in production, use a database)
_feedback_storage = {}


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """
    Submit user feedback on API responses.
    
    Args:
        request: Feedback request with query, answer, and feedback
    
    Returns:
        Feedback response with feedback ID
    """
    try:
        feedback_id = str(uuid.uuid4())
        
        # Store feedback
        _feedback_storage[feedback_id] = {
            "query": request.query,
            "answer": request.answer,
            "feedback": request.feedback,
            "rating": request.rating,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Feedback submitted: {feedback_id}")
        
        return FeedbackResponse(
            message="Feedback submitted successfully",
            feedback_id=feedback_id
        )
    
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")
