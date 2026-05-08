"""
Phase 5.7: Compliance Tests - No Investment Advice
Tests to verify no investment advice is provided
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestNoAdvice:
    """Test that no investment advice is provided."""
    
    def test_advisory_queries_refused(self):
        """Test that advisory queries are refused."""
        from phase2.pipeline import rag_pipeline
        
        advisory_queries = [
            "Should I invest in HDFC Mid Cap Fund?",
            "Which fund is better?",
            "Can you recommend a fund?",
            "Is this a good investment?"
        ]
        
        for query in advisory_queries:
            result = rag_pipeline(query, use_cache=False)
            assert result.get("query_type") == "advisory"
            assert result.get("refusal_type") is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
