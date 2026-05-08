"""
Phase 5.1: Unit Tests - API Endpoints
Tests for Phase 3 API functionality
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestAPIUnit:
    """Test API endpoint functionality."""
    
    def test_api_main_exists(self):
        """Test that API main module exists."""
        from phase3.api.main import app
        assert app is not None
    
    def test_api_models_exist(self):
        """Test that API models exist."""
        from phase3.api.models.schemas import QueryRequest, QueryResponse, SchemesResponse
        assert QueryRequest is not None
        assert QueryResponse is not None
        assert SchemesResponse is not None
    
    def test_api_rag_service_exists(self):
        """Test that RAG service exists."""
        from phase3.api.services.rag_service import RAGService
        assert RAGService is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
