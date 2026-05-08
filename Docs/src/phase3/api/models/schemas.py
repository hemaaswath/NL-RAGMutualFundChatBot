"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List


class QueryRequest(BaseModel):
    """Request model for /api/query endpoint."""
    
    query: str = Field(
        ...,
        description="User query about mutual funds",
        min_length=5,
        max_length=500
    )
    scheme: Optional[str] = Field(
        None,
        description="Optional scheme filter",
        max_length=100
    )
    
    @validator('query')
    def query_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()
    
    @validator('scheme')
    def scheme_must_be_valid(cls, v):
        if v and not v.strip():
            return None
        return v.strip() if v else None


class Citation(BaseModel):
    """Citation model for response."""
    
    scheme_name: str
    source_url: str
    last_updated: str
    section: Optional[str] = None


class QueryResponse(BaseModel):
    """Response model for /api/query endpoint."""
    
    answer: str
    source_url: Optional[str] = None
    last_updated: Optional[str] = None
    query_type: str
    chunks_retrieved: int
    cached: bool = False
    refusal_type: Optional[str] = None
    citations: Optional[List[Citation]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "The expense ratio is 1.25% as per the latest factsheet.",
                "source_url": "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
                "last_updated": "2026-05-07",
                "query_type": "factual",
                "chunks_retrieved": 5,
                "cached": False
            }
        }


class SchemeInfo(BaseModel):
    """Model for scheme information."""
    
    name: str
    category: Optional[str] = None


class SchemesResponse(BaseModel):
    """Response model for /api/schemes endpoint."""
    
    schemes: List[str]
    count: int


class HealthResponse(BaseModel):
    """Response model for /api/health endpoint."""
    
    status: str
    version: str
    timestamp: str


class FeedbackRequest(BaseModel):
    """Request model for /api/feedback endpoint."""
    
    query: str
    answer: str
    feedback: str = Field(..., description="User feedback (positive/negative)")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1 to 5")
    
    @validator('feedback')
    def feedback_must_be_valid(cls, v):
        valid_feedback = ['positive', 'negative', 'neutral']
        if v.lower() not in valid_feedback:
            raise ValueError(f'Feedback must be one of {valid_feedback}')
        return v.lower()


class FeedbackResponse(BaseModel):
    """Response model for /api/feedback endpoint."""
    
    message: str
    feedback_id: str


class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    error: str
    detail: str
    status_code: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "detail": "Query cannot be empty",
                "status_code": 400
            }
        }
