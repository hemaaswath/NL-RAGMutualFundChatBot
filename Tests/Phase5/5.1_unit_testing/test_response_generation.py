"""
Phase 5.1: Unit Tests - Response Generation
Tests for Phase 2 response generation functionality
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestResponseGeneration:
    """Test response generation functionality."""
    
    def test_generator_module_exists(self):
        """Test that generator module exists."""
        from phase2.generator import generate_response, generate_refusal_response
        assert generate_response is not None
        assert generate_refusal_response is not None
    
    def test_generate_response_basic(self):
        """Test basic response generation."""
        from phase2.generator import generate_response
        
        context = "The expense ratio is 1.25% as per the latest factsheet."
        query = "What is the expense ratio?"
        
        result = generate_response(context, query)
        
        assert result is not None
        assert "answer" in result
    
    def test_generate_refusal_response(self):
        """Test refusal response generation."""
        from phase2.generator import generate_refusal_response
        from phase2.config import REFUSAL_TEMPLATES
        
        refusal_type = "investment_advice"
        result = generate_refusal_response(refusal_type, REFUSAL_TEMPLATES)
        
        assert result is not None
        assert isinstance(result, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
