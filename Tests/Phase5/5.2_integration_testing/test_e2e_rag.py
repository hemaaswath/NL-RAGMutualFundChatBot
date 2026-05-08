"""
Phase 5.2: Integration Tests - End-to-End RAG Pipeline
Tests for complete RAG pipeline integration
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestE2ERAG:
    """Test end-to-end RAG pipeline."""
    
    def test_rag_pipeline_integration(self):
        """Test complete RAG pipeline integration."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the expense ratio?"
        result = rag_pipeline(query, use_cache=False)
        
        assert result is not None
        assert "answer" in result
        assert "query_type" in result
        assert "chunks_retrieved" in result
    
    def test_rag_pipeline_with_cache(self):
        """Test RAG pipeline with caching."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the exit load?"
        
        # Test that the pipeline accepts use_cache parameter
        result1 = rag_pipeline(query, use_cache=True)
        assert result1 is not None
        
        result2 = rag_pipeline(query, use_cache=True)
        assert result2 is not None
    
    def test_rag_pipeline_with_scheme_filter(self):
        """Test RAG pipeline with scheme filter."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the NAV?"
        scheme = "HDFC Mid-Cap Fund (Direct Growth)"
        
        result = rag_pipeline(query, scheme=scheme, use_cache=False)
        
        assert result is not None
        assert "answer" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
