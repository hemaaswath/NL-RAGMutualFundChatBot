"""
Phase 5.6: Security Tests - Input Validation
Tests for input validation
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestInputValidation:
    """Test input validation."""
    
    def test_empty_query_handling(self):
        """Test that empty queries are handled correctly."""
        from phase2.pipeline import rag_pipeline
        
        result = rag_pipeline("", use_cache=False)
        # Should return an error or handle gracefully
        assert result is not None
    
    def test_very_long_query_handling(self):
        """Test that very long queries are handled correctly."""
        from phase2.pipeline import rag_pipeline
        
        # Create a very long query
        long_query = "What is the expense ratio? " * 100
        
        # Should handle gracefully (either truncate or reject)
        result = rag_pipeline(long_query, use_cache=False)
        assert result is not None
    
    def test_special_characters_in_query(self):
        """Test that special characters in queries are handled correctly."""
        from phase2.pipeline import rag_pipeline
        
        queries_with_special_chars = [
            "What is the expense ratio?",
            "What is the NAV <script>alert('xss')</script>?",
            "What is the exit load; DROP TABLE users;?"
        ]
        
        for query in queries_with_special_chars:
            result = rag_pipeline(query, use_cache=False)
            assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
