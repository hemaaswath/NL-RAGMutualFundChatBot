"""
Phase 6.2: Cloud Infrastructure Tests
Tests for Terraform configurations
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))


class TestTerraformConfig:
    """Test Terraform configuration files."""
    
    def test_main_tf_exists(self):
        """Test that main.tf exists."""
        main_tf_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.2_cloud_infrastructure" / "main.tf"
        assert main_tf_path.exists()
    
    def test_variables_tf_exists(self):
        """Test that variables.tf exists."""
        variables_tf_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.2_cloud_infrastructure" / "variables.tf"
        assert variables_tf_path.exists()
    
    def test_main_tf_content(self):
        """Test that main.tf has required resources."""
        main_tf_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.2_cloud_infrastructure" / "main.tf"
        content = main_tf_path.read_text(encoding='utf-8')
        
        assert "aws_vpc" in content
        assert "aws_ecs_cluster" in content
        assert "aws_lb" in content
        assert "aws_cloudwatch_log_group" in content
    
    def test_variables_tf_content(self):
        """Test that variables.tf has required variables."""
        variables_tf_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.2_cloud_infrastructure" / "variables.tf"
        content = variables_tf_path.read_text(encoding='utf-8')
        
        assert 'variable "aws_region"' in content
        assert 'variable "project_name"' in content
        assert 'variable "groq_api_key"' in content


class TestInfrastructureDocumentation:
    """Test infrastructure documentation."""
    
    def test_infrastructure_readme_exists(self):
        """Test that infrastructure README exists."""
        readme_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.2_cloud_infrastructure" / "README.md"
        assert readme_path.exists()
    
    def test_infrastructure_readme_content(self):
        """Test that infrastructure README has required sections."""
        readme_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.2_cloud_infrastructure" / "README.md"
        content = readme_path.read_text(encoding='utf-8')
        
        assert "Terraform" in content
        assert "Prerequisites" in content
        assert "Usage" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
