"""
Phase 5.3: Functional Tests - Refusal Scenarios
Tests for refusal scenarios
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestRefusalScenarios:
    """Test refusal scenarios."""
    
    def test_investment_advice_query(self):
        """Test investment advice queries should be refused."""
        from phase2.pipeline import rag_pipeline
        
        query = "Should I invest in HDFC Mid Cap Fund?"
        result = rag_pipeline(query, use_cache=False)
        
        assert result is not None
        assert result.get("query_type") == "advisory"
        assert result.get("refusal_type") is not None
    
    def test_performance_comparison_query(self):
        """Test performance comparison queries should be refused."""
        from phase2.pipeline import rag_pipeline
        
        query = "Which fund is better - HDFC Mid Cap or HDFC Large Cap?"
        result = rag_pipeline(query, use_cache=False)
        
        assert result is not None
        assert result.get("query_type") == "advisory"
    
    def test_recommendation_query(self):
        """Test recommendation queries should be refused."""
        from phase2.pipeline import rag_pipeline
        
        query = "Can you recommend a good mutual fund for me?"
        result = rag_pipeline(query, use_cache=False)
        
        assert result is not None
        assert result.get("query_type") == "advisory"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
