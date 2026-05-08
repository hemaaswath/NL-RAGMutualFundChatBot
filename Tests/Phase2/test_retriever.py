"""
Test cases for Phase 2 Retriever
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))

from phase2.retriever import retrieve


class TestRetriever:
    """Test retrieval mechanism."""
    
    def test_retrieve_returns_results(self):
        """Test that retrieval returns results."""
        query = "What is the expense ratio of HDFC Mid Cap Fund?"
        results = retrieve(query, top_k=3)
        
        assert isinstance(results, list), "Results should be a list"
    
    def test_retrieve_returns_metadata(self):
        """Test that retrieved chunks have metadata."""
        query = "What is the NAV?"
        results = retrieve(query, top_k=1)
        
        if results:
            assert "metadata" in results[0], "Chunk should have metadata"
            assert "scheme_name" in results[0]["metadata"], "Metadata should have scheme_name"
    
    def test_retrieve_returns_similarity_score(self):
        """Test that retrieved chunks have similarity scores."""
        query = "What is the expense ratio?"
        results = retrieve(query, top_k=1)
        
        if results:
            assert "similarity" in results[0], "Chunk should have similarity score"
            assert 0 <= results[0]["similarity"] <= 1, "Similarity should be between 0 and 1"
    
    def test_retrieve_with_scheme_filter(self):
        """Test retrieval with scheme filter."""
        query = "What is the expense ratio?"
        scheme = "HDFC Mid-Cap Fund (Direct Growth)"
        results = retrieve(query, scheme=scheme, top_k=3)
        
        if results:
            for result in results:
                assert result["metadata"]["scheme_name"] == scheme, "Scheme filter not working"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
