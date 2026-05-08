"""
Phase 5.1: Unit Tests - Retrieval Mechanism
Tests for Phase 2 retrieval functionality
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestRetrieval:
    """Test retrieval mechanism functionality."""
    
    def test_retriever_module_exists(self):
        """Test that retriever module exists."""
        from phase2.retriever import retrieve
        assert retrieve is not None
    
    def test_retrieve_basic(self):
        """Test basic retrieval functionality."""
        from phase2.retriever import retrieve
        
        query = "What is the expense ratio?"
        results = retrieve(query)
        
        assert results is not None
        assert isinstance(results, list)
    
    def test_retrieve_with_scheme_filter(self):
        """Test retrieval with scheme filter."""
        from phase2.retriever import retrieve
        
        query = "What is the NAV?"
        scheme = "HDFC Mid-Cap Fund (Direct Growth)"
        results = retrieve(query, scheme=scheme)
        
        assert results is not None
        assert isinstance(results, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
