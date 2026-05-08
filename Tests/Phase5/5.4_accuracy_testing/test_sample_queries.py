"""
Phase 5.4: Accuracy Tests - Sample Queries
Tests for sample query accuracy
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestSampleQueries:
    """Test sample query accuracy."""
    
    def test_sample_query_returns_answer(self):
        """Test that sample queries return answers."""
        from phase2.pipeline import rag_pipeline
        
        sample_queries = [
            "What is the expense ratio?",
            "What is the exit load?",
            "What is the minimum SIP amount?"
        ]
        
        for query in sample_queries:
            result = rag_pipeline(query, use_cache=False)
            assert result is not None
            assert result.get("answer") is not None
            assert len(result.get("answer", "")) > 0
    
    def test_response_length_validation(self):
        """Test that response length is within limits."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the expense ratio?"
        result = rag_pipeline(query, use_cache=False)
        
        answer = result.get("answer", "")
        assert len(answer) <= 500  # Max response length limit


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
