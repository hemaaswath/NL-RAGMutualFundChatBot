"""
Phase 5.7: Compliance Tests - Disclaimers
Tests to verify disclaimers are present
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestDisclaimers:
    """Test that disclaimers are present."""
    
    def test_refusal_templates_exist(self):
        """Test that refusal templates exist."""
        from phase2.config import REFUSAL_TEMPLATES
        
        assert REFUSAL_TEMPLATES is not None
        assert isinstance(REFUSAL_TEMPLATES, dict)
        assert len(REFUSAL_TEMPLATES) > 0
    
    def test_refusal_contains_educational_resources(self):
        """Test that refusal responses contain educational resources."""
        from phase2.refusal import get_refusal_message
        
        message = get_refusal_message("investment_advice")
        assert message is not None
        # Check for AMFI or SEBI references
        assert "AMFI" in message or "SEBI" in message or "advisor" in message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
