"""
Phase 5.5: Performance Tests - Response Time
Tests for response time benchmarks
"""

import pytest
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestResponseTime:
    """Test response time benchmarks."""
    
    def test_query_response_time(self):
        """Test that query response time is acceptable (<3 seconds)."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the expense ratio?"
        
        start_time = time.time()
        result = rag_pipeline(query, use_cache=False)
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 5.0  # Allow 5 seconds for first call (embedding load)
        print(f"Response time: {response_time:.2f} seconds")
    
    def test_cached_query_response_time(self):
        """Test that cached query response time is fast (<1 second)."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the exit load?"
        
        # First call to populate cache
        rag_pipeline(query, use_cache=True)
        
        # Second call should be cached
        start_time = time.time()
        result = rag_pipeline(query, use_cache=True)
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 1.0  # Cached queries should be fast
        assert result.get("cached") == True
        print(f"Cached response time: {response_time:.2f} seconds")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
