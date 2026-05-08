"""
Phase 5.1: Unit Tests - Refusal Handling
Tests for Phase 2 refusal handling functionality
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestRefusalHandling:
    """Test refusal handling functionality."""
    
    def test_refusal_module_exists(self):
        """Test that refusal module exists."""
        from phase2.refusal import get_refusal_message, handle_advisory_query
        assert get_refusal_message is not None
        assert handle_advisory_query is not None
    
    def test_get_refusal_message(self):
        """Test getting refusal message."""
        from phase2.refusal import get_refusal_message
        
        refusal_type = "investment_advice"
        message = get_refusal_message(refusal_type)
        
        assert message is not None
        assert isinstance(message, str)
        assert len(message) > 0
    
    def test_handle_advisory_query(self):
        """Test handling advisory query."""
        from phase2.refusal import handle_advisory_query
        
        query = "Which fund is better?"
        refusal_type = "performance_comparison"
        result = handle_advisory_query(query, refusal_type)
        
        assert result is not None
        assert isinstance(result, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
