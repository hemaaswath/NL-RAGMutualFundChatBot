"""
Phase 5.2: Integration Tests - Database Integration
Tests for ChromaDB integration
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestDatabaseIntegration:
    """Test database integration."""
    
    def test_chromadb_connection(self):
        """Test ChromaDB connection."""
        from phase1.vector_store import get_client
        
        client = get_client()
        assert client is not None
    
    def test_collection_access(self):
        """Test collection access."""
        from phase1.vector_store import get_or_create_collection
        
        collection = get_or_create_collection()
        assert collection is not None
    
    def test_retrieval_from_database(self):
        """Test retrieval from database."""
        from phase2.retriever import retrieve
        
        query = "What is the expense ratio?"
        results = retrieve(query)
        
        assert results is not None
        assert isinstance(results, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
