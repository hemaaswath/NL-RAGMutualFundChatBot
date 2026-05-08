"""
Phase 6.5: Documentation Tests
Tests for documentation files
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))


class TestDeploymentDocumentation:
    """Test deployment documentation."""
    
    def test_deployment_readme_exists(self):
        """Test that deployment README exists."""
        readme_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.5_documentation" / "README.md"
        assert readme_path.exists()
    
    def test_deployment_readme_content(self):
        """Test that deployment README has required sections."""
        readme_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.5_documentation" / "README.md"
        content = readme_path.read_text(encoding='utf-8')
        
        assert "Prerequisites" in content
        assert "Local Development" in content
        assert "Docker Deployment" in content
        assert "Cloud Deployment" in content
        assert "CI/CD Pipeline" in content
        assert "Monitoring" in content
        assert "Troubleshooting" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
