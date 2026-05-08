"""
Phase 5.2: Integration Tests - API-Frontend Integration
Tests for API and frontend integration
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestAPIFrontendIntegration:
    """Test API and frontend integration."""
    
    def test_api_available_for_frontend(self):
        """Test that API is available for frontend."""
        from phase3.api.main import app
        from phase3.api.services.rag_service import RAGService
        
        assert app is not None
        assert RAGService is not None
    
    def test_rag_service_accessible(self):
        """Test that RAG service is accessible from API layer."""
        from phase3.api.services.rag_service import RAGService
        
        schemes = RAGService.get_schemes()
        assert schemes is not None
        assert isinstance(schemes, list)
    
    def test_phase4_can_access_phase2(self):
        """Test that Phase 4 UI can access Phase 2 pipeline."""
        from phase2.pipeline import rag_pipeline, get_available_schemes
        
        # Test that Phase 2 functions are accessible
        assert rag_pipeline is not None
        assert get_available_schemes is not None
        
        # Test basic functionality
        schemes = get_available_schemes()
        assert schemes is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
