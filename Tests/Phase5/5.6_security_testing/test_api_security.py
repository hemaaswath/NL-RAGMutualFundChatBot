"""
Phase 5.6: Security Tests - API Security
Tests for API security
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestAPISecurity:
    """Test API security."""
    
    def test_pydantic_validation(self):
        """Test that Pydantic models validate input correctly."""
        from phase3.api.models.schemas import QueryRequest
        from pydantic import ValidationError
        
        # Test valid input
        valid_request = QueryRequest(query="What is the expense ratio?")
        assert valid_request.query == "What is the expense ratio?"
        
        # Test invalid input (empty query)
        with pytest.raises(ValidationError):
            QueryRequest(query="")
        
        # Test invalid input (too long)
        with pytest.raises(ValidationError):
            QueryRequest(query="a" * 600)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
