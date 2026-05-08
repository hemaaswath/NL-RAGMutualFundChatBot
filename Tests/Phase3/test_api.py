"""
Test cases for Phase 3 API
"""

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))

from phase3.api.main import app
from phase3.api.models.schemas import QueryRequest, SchemesResponse, HealthResponse

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test health check returns correct response."""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data


class TestSchemesEndpoint:
    """Test schemes endpoint."""
    
    def test_get_schemes(self):
        """Test getting list of schemes."""
        response = client.get("/api/schemes")
        
        assert response.status_code == 200
        data = response.json()
        assert "schemes" in data
        assert "count" in data
        assert isinstance(data["schemes"], list)
        assert data["count"] > 0
    
    def test_schemes_count_matches(self):
        """Test that count matches number of schemes."""
        response = client.get("/api/schemes")
        
        data = response.json()
        assert data["count"] == len(data["schemes"])


class TestQueryEndpoint:
    """Test query endpoint."""
    
    def test_query_factual(self):
        """Test factual query."""
        request_data = {
            "query": "What is the expense ratio?"
        }
        
        response = client.post("/api/query", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "query_type" in data
        assert "chunks_retrieved" in data
        assert data["query_type"] == "factual"
    
    def test_query_with_scheme_filter(self):
        """Test query with scheme filter."""
        request_data = {
            "query": "What is the NAV?",
            "scheme": "HDFC Mid-Cap Fund (Direct Growth)"
        }
        
        response = client.post("/api/query", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
    
    def test_query_empty(self):
        """Test query with empty string should fail validation."""
        request_data = {
            "query": ""
        }
        
        response = client.post("/api/query", json=request_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_query_too_long(self):
        """Test query exceeding max length should fail validation."""
        request_data = {
            "query": "a" * 600  # Exceeds 500 char limit
        }
        
        response = client.post("/api/query", json=request_data)
        
        assert response.status_code == 422  # Validation error


class TestFeedbackEndpoint:
    """Test feedback endpoint."""
    
    def test_submit_feedback_positive(self):
        """Test submitting positive feedback."""
        request_data = {
            "query": "What is the expense ratio?",
            "answer": "The expense ratio is 1.25%.",
            "feedback": "positive",
            "rating": 5
        }
        
        response = client.post("/api/feedback", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "feedback_id" in data
    
    def test_submit_feedback_negative(self):
        """Test submitting negative feedback."""
        request_data = {
            "query": "What is the NAV?",
            "answer": "I couldn't find that information.",
            "feedback": "negative",
            "rating": 2
        }
        
        response = client.post("/api/feedback", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
    
    def test_feedback_invalid_type(self):
        """Test feedback with invalid type should fail validation."""
        request_data = {
            "query": "Test query",
            "answer": "Test answer",
            "feedback": "invalid"
        }
        
        response = client.post("/api/feedback", json=request_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_feedback_invalid_rating(self):
        """Test feedback with invalid rating should fail validation."""
        request_data = {
            "query": "Test query",
            "answer": "Test answer",
            "feedback": "positive",
            "rating": 10  # Exceeds 5
        }
        
        response = client.post("/api/feedback", json=request_data)
        
        assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
