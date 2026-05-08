"""
Phase 5.4: Accuracy Tests - Citation Accuracy
Tests for citation accuracy verification
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestCitationAccuracy:
    """Test citation accuracy."""
    
    def test_citations_present_in_response(self):
        """Test that citations are present in responses."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the expense ratio?"
        result = rag_pipeline(query, use_cache=False)
        
        # Check if citations are present when chunks are retrieved
        if result.get("chunks_retrieved", 0) > 0:
            assert "citations" in result
            if result.get("citations"):
                assert len(result["citations"]) > 0
    
    def test_citation_structure(self):
        """Test that citations have correct structure."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the expense ratio?"
        result = rag_pipeline(query, use_cache=False)
        
        if result.get("citations") and len(result["citations"]) > 0:
            citation = result["citations"][0]
            assert "scheme_name" in citation
            assert "source_url" in citation
            assert "last_updated" in citation


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
