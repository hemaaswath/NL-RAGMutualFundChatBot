"""
Phase 6.4: Environment Configuration Tests
Tests for environment configuration files
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))


class TestEnvironmentFiles:
    """Test environment configuration files."""
    
    def test_env_example_exists(self):
        """Test that .env.example exists."""
        env_example_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.4_environment_config" / ".env.example"
        assert env_example_path.exists()
    
    def test_env_example_content(self):
        """Test that .env.example has required variables."""
        env_example_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.4_environment_config" / ".env.example"
        content = env_example_path.read_text(encoding='utf-8')
        
        assert "GROQ_API_KEY" in content
        assert "API_HOST" in content
        assert "API_PORT" in content
        assert "ENVIRONMENT" in content


class TestConfigModule:
    """Test configuration module."""
    
    def test_config_py_exists(self):
        """Test that config.py exists."""
        config_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.4_environment_config" / "config.py"
        assert config_path.exists()
    
    def test_config_py_content(self):
        """Test that config.py has required classes."""
        config_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.4_environment_config" / "config.py"
        content = config_path.read_text(encoding='utf-8')
        
        assert "class Settings" in content
        assert "BaseSettings" in content
        assert "get_settings" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
