"""
Phase 6.1: Containerization Tests
Tests for Dockerfile and Docker Compose configurations
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))


class TestDockerfileBackend:
    """Test backend Dockerfile configuration."""
    
    def test_dockerfile_backend_exists(self):
        """Test that backend Dockerfile exists."""
        dockerfile_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.1_containerization" / "Dockerfile.backend"
        assert dockerfile_path.exists()
    
    def test_dockerfile_backend_content(self):
        """Test that backend Dockerfile has required content."""
        dockerfile_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.1_containerization" / "Dockerfile.backend"
        content = dockerfile_path.read_text(encoding='utf-8')
        
        assert "FROM python:" in content
        assert "uvicorn" in content
        assert "phase3.api.main:app" in content


class TestDockerfileFrontend:
    """Test frontend Dockerfile configuration."""
    
    def test_dockerfile_frontend_exists(self):
        """Test that frontend Dockerfile exists."""
        dockerfile_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.1_containerization" / "Dockerfile.frontend"
        assert dockerfile_path.exists()
    
    def test_dockerfile_frontend_content(self):
        """Test that frontend Dockerfile has required content."""
        dockerfile_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.1_containerization" / "Dockerfile.frontend"
        content = dockerfile_path.read_text(encoding='utf-8')
        
        assert "FROM python:" in content
        assert "streamlit" in content
        assert "phase4/app.py" in content


class TestDockerCompose:
    """Test Docker Compose configuration."""
    
    def test_docker_compose_exists(self):
        """Test that docker-compose.yml exists."""
        compose_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.1_containerization" / "docker-compose.yml"
        assert compose_path.exists()
    
    def test_docker_compose_content(self):
        """Test that docker-compose.yml has required services."""
        compose_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.1_containerization" / "docker-compose.yml"
        content = compose_path.read_text(encoding='utf-8')
        
        assert "backend:" in content
        assert "frontend:" in content
        assert "networks:" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
