"""
Phase 5.3: Functional Tests - Query Types
Tests for different query types from requirements
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestQueryTypes:
    """Test different query types."""
    
    def test_expense_ratio_query(self):
        """Test expense ratio queries."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the expense ratio of HDFC Mid Cap Fund?"
        result = rag_pipeline(query, use_cache=False)
        
        assert result is not None
        assert result.get("query_type") == "factual"
    
    def test_exit_load_query(self):
        """Test exit load queries."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the exit load for HDFC Large Cap Fund?"
        result = rag_pipeline(query, use_cache=False)
        
        assert result is not None
        assert result.get("query_type") == "factual"
    
    def test_sip_amount_query(self):
        """Test SIP amount queries."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the minimum SIP amount?"
        result = rag_pipeline(query, use_cache=False)
        
        assert result is not None
        assert result.get("query_type") == "factual"
    
    def test_nav_query(self):
        """Test NAV queries."""
        from phase2.pipeline import rag_pipeline
        
        query = "What is the current NAV of HDFC Equity Fund?"
        result = rag_pipeline(query, use_cache=False)
        
        assert result is not None
        assert result.get("query_type") == "factual"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
