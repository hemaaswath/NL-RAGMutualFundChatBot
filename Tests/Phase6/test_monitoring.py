"""
Phase 6.6: Monitoring & Maintenance Tests
Tests for monitoring and maintenance scripts
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))


class TestHealthCheck:
    """Test health check script."""
    
    def test_health_check_script_exists(self):
        """Test that health_check.py exists."""
        health_check_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.6_monitoring_maintenance" / "health_check.py"
        assert health_check_path.exists()
    
    def test_health_check_content(self):
        """Test that health_check.py has required functions."""
        health_check_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.6_monitoring_maintenance" / "health_check.py"
        content = health_check_path.read_text(encoding='utf-8')
        
        assert "check_backend_health" in content
        assert "check_frontend_health" in content
        assert "run_health_checks" in content


class TestLoggingConfig:
    """Test logging configuration."""
    
    def test_logging_config_exists(self):
        """Test that logging_config.py exists."""
        logging_config_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.6_monitoring_maintenance" / "logging_config.py"
        assert logging_config_path.exists()
    
    def test_logging_config_content(self):
        """Test that logging_config.py has required functions."""
        logging_config_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.6_monitoring_maintenance" / "logging_config.py"
        content = logging_config_path.read_text(encoding='utf-8')
        
        assert "setup_logging" in content
        assert "JSONFormatter" in content
        assert "get_logger" in content


class TestMonitoringDocumentation:
    """Test monitoring documentation."""
    
    def test_monitoring_readme_exists(self):
        """Test that monitoring README exists."""
        readme_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.6_monitoring_maintenance" / "README.md"
        assert readme_path.exists()
    
    def test_monitoring_readme_content(self):
        """Test that monitoring README has required sections."""
        readme_path = Path(__file__).parent.parent.parent / "Docs" / "Deployment" / "6.6_monitoring_maintenance" / "README.md"
        content = readme_path.read_text(encoding='utf-8')
        
        assert "Health Checks" in content
        assert "Logging" in content
        assert "Monitoring Metrics" in content
        assert "Maintenance Tasks" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
