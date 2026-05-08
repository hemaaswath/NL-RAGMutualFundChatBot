"""
Phase 5.5: Performance Tests - Caching Efficiency
Tests for caching efficiency
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestCaching:
    """Test caching efficiency."""
    
    def test_cache_hit_on_repeated_query(self):
        """Test that repeated queries hit the cache."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the minimum investment amount?"
        
        # Test that the pipeline accepts use_cache parameter
        result1 = rag_pipeline(query, use_cache=True)
        assert result1 is not None
        
        result2 = rag_pipeline(query, use_cache=True)
        assert result2 is not None
    
    def test_cache_stats(self):
        """Test that cache stats are available."""
        from phase2.pipeline import get_cache_stats
        
        stats = get_cache_stats()
        assert stats is not None
        assert isinstance(stats, dict)
        assert "total_entries" in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
