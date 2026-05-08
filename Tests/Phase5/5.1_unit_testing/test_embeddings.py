"""
Phase 5.1: Unit Tests - Embedding Generation
Tests for Phase 1/2 embedding functionality
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Docs" / "src"))


class TestEmbeddings:
    """Test embedding generation functionality."""
    
    def test_embeddings_module_exists(self):
        """Test that embeddings module exists."""
        from phase1.embeddings import generate_embeddings, generate_single_embedding
        assert generate_embeddings is not None
        assert generate_single_embedding is not None
    
    def test_generate_single_embedding(self):
        """Test single embedding generation."""
        from phase1.embeddings import generate_single_embedding
        
        text = "This is a test text for embedding generation."
        embedding = generate_single_embedding(text)
        
        assert embedding is not None
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert isinstance(embedding[0], float)
    
    def test_generate_embeddings_batch(self):
        """Test batch embedding generation."""
        from phase1.embeddings import generate_embeddings
        
        texts = ["First test text.", "Second test text.", "Third test text."]
        embeddings = generate_embeddings(texts)
        
        assert embeddings is not None
        assert len(embeddings) == len(texts)
        assert all(isinstance(emb, list) for emb in embeddings)
        assert all(len(emb) > 0 for emb in embeddings)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
