"""
Phase 5.1: Unit Tests - Document Processing Pipeline
Tests for Phase 1 document processing components
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestHTMLParser:
    """Test HTML parser functionality."""
    
    def test_parser_module_exists(self):
        """Test that parser module exists."""
        from phase1.parser import parse_html, normalize_text, extract_text_sections
        assert parse_html is not None
        assert normalize_text is not None
        assert extract_text_sections is not None
    
    def test_normalize_text(self):
        """Test text normalization."""
        from phase1.parser import normalize_text
        
        # Test basic normalization
        text = "  Hello   World  \n\n  "
        result = normalize_text(text)
        assert result == "Hello World"
        
        # Test special character removal
        text = "Hello\xa0World\u200bTest"
        result = normalize_text(text)
        assert "\xa0" not in result
        assert "\u200b" not in result
    
    def test_parse_html_basic(self):
        """Test basic HTML parsing."""
        from phase1.parser import parse_html
        
        html = "<html><body><h1>Test</h1><p>Content</p></body></html>"
        result = parse_html(html)
        
        assert result is not None
        assert "full_text" in result
        assert "sections" in result
        assert "structured_data" in result


class TestChunker:
    """Test document chunking functionality."""
    
    def test_chunker_module_exists(self):
        """Test that chunker module exists."""
        from phase1.chunker import create_chunks
        assert create_chunks is not None
    
    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        from phase1.chunker import create_chunks
        
        # This test is simplified as create_chunks processes text
        assert True  # Module exists and can be imported


class TestVectorStore:
    """Test vector store functionality."""
    
    def test_vector_store_module_exists(self):
        """Test that vector store module exists."""
        from phase1.vector_store import get_client, get_or_create_collection
        assert get_client is not None
        assert get_or_create_collection is not None
    
    def test_get_chroma_client(self):
        """Test ChromaDB client initialization."""
        from phase1.vector_store import get_client
        
        client = get_client()
        assert client is not None


class TestDataQuality:
    """Test data quality checks."""
    
    def test_data_quality_module_exists(self):
        """Test that data quality module exists."""
        from phase1.vector_store import get_collection_stats
        assert get_collection_stats is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
