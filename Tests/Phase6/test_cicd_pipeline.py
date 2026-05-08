"""
Phase 6.3: CI/CD Pipeline Tests
Tests for GitHub Actions workflows
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))


class TestCIPipeline:
    """Test CI pipeline configuration."""
    
    def test_ci_workflow_exists(self):
        """Test that CI workflow exists."""
        ci_workflow_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.3_cicd_pipeline" / "ci.yml"
        assert ci_workflow_path.exists()
    
    def test_ci_workflow_content(self):
        """Test that CI workflow has required jobs."""
        ci_workflow_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.3_cicd_pipeline" / "ci.yml"
        content = ci_workflow_path.read_text(encoding='utf-8')
        
        assert "lint:" in content
        assert "test-phase1:" in content
        assert "test-phase2:" in content
        assert "test-phase3:" in content
        assert "test-phase5:" in content


class TestCDPipeline:
    """Test CD pipeline configuration."""
    
    def test_cd_workflow_exists(self):
        """Test that CD workflow exists."""
        cd_workflow_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.3_cicd_pipeline" / "cd.yml"
        assert cd_workflow_path.exists()
    
    def test_cd_workflow_content(self):
        """Test that CD workflow has required jobs."""
        cd_workflow_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.3_cicd_pipeline" / "cd.yml"
        content = cd_workflow_path.read_text(encoding='utf-8')
        
        assert "build-and-push:" in content
        assert "deploy-staging:" in content
        assert "deploy-production:" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
