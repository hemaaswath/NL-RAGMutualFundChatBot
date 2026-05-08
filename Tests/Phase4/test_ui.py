"""
Test cases for Phase 4 UI (Streamlit Application)
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))


class TestUIComponents:
    """Test UI component functions."""
    
    def test_app_module_exists(self):
        """Test that the app module can be imported."""
        try:
            from phase4 import app
            assert app is not None
        except ImportError:
            pytest.skip("Streamlit app cannot be imported directly (normal for Streamlit)")
    
    def test_phase4_module_exists(self):
        """Test that phase4 module exists."""
        try:
            from phase4 import __init__
            assert __init__ is not None
        except ImportError:
            pytest.fail("phase4 module does not exist")


class TestUIIntegration:
    """Test UI integration with backend."""
    
    def test_rag_pipeline_available(self):
        """Test that RAG pipeline is available for UI."""
        from phase2.pipeline import rag_pipeline
        assert rag_pipeline is not None
    
    def test_get_schemes_available(self):
        """Test that get_schemes is available for UI."""
        from phase2.pipeline import get_available_schemes
        assert get_available_schemes is not None
    
    def test_rag_pipeline_works(self):
        """Test that RAG pipeline works as expected for UI."""
        from phase2.pipeline import rag_pipeline
        
        result = rag_pipeline("What is the expense ratio?", use_cache=False)
        
        assert result is not None
        assert "answer" in result
        assert "query_type" in result


class TestUIConfiguration:
    """Test UI configuration files."""
    
    def test_streamlit_config_exists(self):
        """Test that Streamlit config file exists."""
        config_path = Path(__file__).parent.parent.parent / "Docs" / "src" / "phase4" / ".streamlit" / "config.toml"
        assert config_path.exists()
    
    def test_app_file_exists(self):
        """Test that app.py file exists."""
        app_path = Path(__file__).parent.parent.parent / "Docs" / "src" / "phase4" / "app.py"
        assert app_path.exists()
    
    def test_app_file_content(self):
        """Test that app.py contains essential components."""
        app_path = Path(__file__).parent.parent.parent / "Docs" / "src" / "phase4" / "app.py"
        content = app_path.read_text(encoding='utf-8')
        
        # Check for essential components
        assert "streamlit" in content
        assert "rag_pipeline" in content
        assert "Disclaimer" in content or "disclaimer" in content
        assert "Query Input" in content or "query" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
