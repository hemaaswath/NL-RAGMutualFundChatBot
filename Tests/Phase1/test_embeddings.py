"""
Test cases for Phase 1 Embeddings - Edge Cases from EdgeCases_Phase1_DataCollection.md
"""

import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))

from phase1.embeddings import generate_embeddings, generate_single_embedding, get_model
from phase1.config import EMBEDDING_MODEL, EMBEDDING_DIMENSIONS


class TestEmbeddingGeneration:
    """Test embedding generation edge cases."""
    
    def test_model_loads_successfully(self):
        """Test that the embedding model loads successfully."""
        model = get_model()
        assert model is not None, "Model failed to load"
    
    def test_single_embedding_generation(self):
        """Test that single embedding is generated successfully."""
        test_text = "HDFC Mid Cap Fund is a mutual fund scheme."
        embedding = generate_single_embedding(test_text)
        
        assert embedding is not None, "Failed to generate embedding"
        assert len(embedding) == EMBEDDING_DIMENSIONS, f"Wrong embedding dimension: {len(embedding)}"
        assert all(isinstance(x, float) for x in embedding), "Embedding contains non-float values"
    
    def test_batch_embedding_generation(self):
        """Test that batch embeddings are generated successfully."""
        test_texts = [
            "HDFC Mid Cap Fund invests in mid-sized companies.",
            "Expense ratio is 0.73% for this fund.",
            "Minimum SIP investment is ₹100.",
            "Exit load is 1% if redeemed within 1 year.",
            "The fund benchmark is NIFTY Midcap 150 Total Return Index."
        ]
        
        embeddings = generate_embeddings(test_texts)
        
        assert len(embeddings) == len(test_texts), f"Wrong number of embeddings: {len(embeddings)}"
        assert all(len(emb) == EMBEDDING_DIMENSIONS for emb in embeddings), "Wrong embedding dimensions"
        assert all(emb is not None for emb in embeddings), "Some embeddings are None"


class TestEmbeddingDimensions:
    """Test embedding dimension edge cases."""
    
    def test_embedding_dimensions_match_config(self):
        """Test that embedding dimensions match configuration."""
        test_text = "Test text for embedding dimension check."
        embedding = generate_single_embedding(test_text)
        
        assert len(embedding) == EMBEDDING_DIMENSIONS, f"Dimension mismatch: {len(embedding)} vs {EMBEDDING_DIMENSIONS}"
    
    def test_all_embeddings_same_dimension(self):
        """Test that all embeddings have the same dimension."""
        test_texts = ["Text 1", "Text 2", "Text 3", "Text 4", "Text 5"]
        embeddings = generate_embeddings(test_texts)
        
        dimensions = [len(emb) for emb in embeddings]
        assert len(set(dimensions)) == 1, f"Inconsistent dimensions: {set(dimensions)}"


class TestEmbeddingQuality:
    """Test embedding quality edge cases."""
    
    def test_embeddings_not_all_zeros(self):
        """Test that embeddings are not all zeros."""
        test_texts = ["Different text 1", "Different text 2"]
        embeddings = generate_embeddings(test_texts)
        
        for emb in embeddings:
            assert not all(x == 0.0 for x in emb), "Embedding is all zeros"
    
    def test_similar_texts_similar_embeddings(self):
        """Test that similar texts produce similar embeddings."""
        text1 = "HDFC Mid Cap Fund is a mutual fund"
        text2 = "HDFC Mid Cap Fund is a mutual fund scheme"
        
        emb1 = generate_single_embedding(text1)
        emb2 = generate_single_embedding(text2)
        
        # Calculate cosine similarity
        import numpy as np
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        assert similarity > 0.9, f"Similar texts have low similarity: {similarity}"
    
    def test_different_texts_different_embeddings(self):
        """Test that different texts produce different embeddings."""
        text1 = "HDFC Mid Cap Fund invests in mid-sized companies"
        text2 = "Large Cap funds invest in large companies"
        
        emb1 = generate_single_embedding(text1)
        emb2 = generate_single_embedding(text2)
        
        # Calculate cosine similarity
        import numpy as np
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        assert similarity < 0.8, f"Different texts have high similarity: {similarity}"


class TestEmbeddingAPIFailures:
    """Test embedding API failure edge cases (local model fallback)."""
    
    def test_empty_text_handling(self):
        """Test that empty text is handled gracefully."""
        embedding = generate_single_embedding("")
        
        # Should still generate embedding for empty string
        assert embedding is not None, "Empty text should still generate embedding"
        assert len(embedding) == EMBEDDING_DIMENSIONS, "Wrong dimension for empty text"
    
    def test_very_long_text_handling(self):
        """Test that very long text is handled gracefully."""
        # Create text longer than typical chunk size
        long_text = "This is a test. " * 1000  # ~15,000 characters
        
        embedding = generate_single_embedding(long_text)
        
        assert embedding is not None, "Long text should generate embedding"
        assert len(embedding) == EMBEDDING_DIMENSIONS, "Wrong dimension for long text"


class TestEmbeddingPerformance:
    """Test embedding performance edge cases."""
    
    def test_embedding_speed(self):
        """Test that embedding generation is reasonably fast."""
        import time
        test_texts = ["Test text"] * 10
        
        start_time = time.time()
        embeddings = generate_embeddings(test_texts)
        elapsed_time = time.time() - start_time
        
        assert elapsed_time < 10, f"Embedding too slow: {elapsed_time}s for {len(test_texts)} texts"
    
    def test_batch_processing_efficient(self):
        """Test that batch processing is efficient."""
        import time
        
        # Single embeddings
        start_time = time.time()
        for _ in range(10):
            generate_single_embedding("Test text")
        single_time = time.time() - start_time
        
        # Batch embeddings
        start_time = time.time()
        generate_embeddings(["Test text"] * 10)
        batch_time = time.time() - start_time
        
        # Batch should be faster or similar
        assert batch_time <= single_time * 1.5, f"Batch processing not efficient: {batch_time} vs {single_time}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
