"""
Test cases for Phase 2 RAG Pipeline
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))

from phase2.pipeline import rag_pipeline, get_available_schemes, get_cache_stats, clear_cache


class TestRAGPipeline:
    """Test main RAG pipeline."""
    
    def test_factual_query_pipeline(self):
        """Test pipeline with factual query."""
        query = "What is the expense ratio of HDFC Mid Cap Fund?"
        result = rag_pipeline(query, use_cache=False)
        
        assert "answer" in result, "Result should have answer"
        assert "query_type" in result, "Result should have query_type"
        assert result["query_type"] == "factual", "Query type should be factual"
    
    def test_advisory_query_pipeline(self):
        """Test pipeline with advisory query."""
        query = "Should I invest in HDFC Mid Cap Fund?"
        result = rag_pipeline(query, use_cache=False)
        
        assert "answer" in result, "Result should have answer"
        assert "query_type" in result, "Result should have query_type"
        assert result["query_type"] == "advisory", "Query type should be advisory"
        assert "refusal_type" in result, "Advisory query should have refusal_type"
    
    def test_pipeline_with_scheme_filter(self):
        """Test pipeline with scheme filter."""
        query = "What is the NAV?"
        scheme = "HDFC Mid-Cap Fund (Direct Growth)"
        result = rag_pipeline(query, scheme=scheme, use_cache=False)
        
        assert "answer" in result, "Result should have answer"
    
    def test_pipeline_uses_cache(self):
        """Test that pipeline uses cache."""
        query = "What is the expense ratio?"
        
        # First call - not cached
        result1 = rag_pipeline(query, use_cache=True)
        assert result1["cached"] == False, "First call should not be cached"
        
        # Second call - should be cached
        result2 = rag_pipeline(query, use_cache=True)
        assert result2["cached"] == True, "Second call should be cached"
        
        # Clear cache for cleanup
        clear_cache()
    
    def test_get_available_schemes(self):
        """Test getting available schemes."""
        schemes = get_available_schemes()
        
        assert isinstance(schemes, list), "Schemes should be a list"
        assert len(schemes) > 0, "Should have at least one scheme"
    
    def test_cache_stats(self):
        """Test cache statistics."""
        stats = get_cache_stats()
        
        assert "enabled" in stats, "Stats should have enabled field"
        assert isinstance(stats["enabled"], bool), "Enabled should be boolean"


class TestCache:
    """Test caching functionality."""
    
    def test_clear_cache(self):
        """Test clearing cache."""
        success = clear_cache()
        assert isinstance(success, bool), "Should return boolean"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
