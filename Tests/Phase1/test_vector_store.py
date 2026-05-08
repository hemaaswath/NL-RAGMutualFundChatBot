"""
Test cases for Phase 1 Vector Store - Edge Cases from EdgeCases_Phase1_DataCollection.md
"""

import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))

from phase1.vector_store import get_client, get_or_create_collection, upsert_chunks, get_collection_stats, query_similar
from phase1.chunker import chunk_all_schemes
from phase1.config import CHROMA_COLLECTION_NAME, EMBEDDING_DIMENSIONS


class TestDatabaseConnection:
    """Test database connection edge cases."""
    
    def test_client_initializes(self):
        """Test that ChromaDB client initializes successfully."""
        client = get_client()
        assert client is not None, "Failed to initialize ChromaDB client"
    
    def test_collection_exists(self):
        """Test that collection can be created/retrieved."""
        client = get_client()
        collection = get_or_create_collection(client)
        assert collection is not None, "Failed to get collection"
        assert collection.name == CHROMA_COLLECTION_NAME, f"Wrong collection name: {collection.name}"


class TestIndexing:
    """Test indexing edge cases."""
    
    def test_chunks_indexed(self):
        """Test that chunks are successfully indexed."""
        stats = get_collection_stats()
        assert "total_vectors" in stats, "Missing total_vectors in stats"
        assert stats["total_vectors"] > 0, "No vectors indexed in database"
        assert stats["total_vectors"] >= 100, f"Too few vectors: {stats['total_vectors']}"
    
    def test_embedding_dimensions_match(self):
        """Test that indexed embeddings have correct dimensions."""
        client = get_client()
        collection = get_or_create_collection(client)
        
        results = collection.get(limit=1, include=["embeddings"])
        
        if len(results["embeddings"]) > 0:
            embedding = results["embeddings"][0]
            assert len(embedding) == EMBEDDING_DIMENSIONS, f"Wrong dimension: {len(embedding)}"
    
    def test_metadata_attached(self):
        """Test that metadata is attached to all indexed chunks."""
        client = get_client()
        collection = get_or_create_collection(client)
        
        results = collection.get(limit=10, include=["metadatas"])
        
        assert len(results["metadatas"]) > 0, "No metadata found"
        
        required_fields = ["scheme_name", "source_url", "section", "category"]
        for metadata in results["metadatas"]:
            for field in required_fields:
                assert field in metadata, f"Missing metadata field: {field}"


class TestQuerying:
    """Test querying edge cases."""
    
    def test_query_returns_results(self):
        """Test that queries return results."""
        query_text = "What is the expense ratio of HDFC Mid Cap Fund?"
        results = query_similar(query_text, n_results=3)
        
        assert "documents" in results, "Missing documents in results"
        assert "metadatas" in results, "Missing metadatas in results"
        assert "distances" in results, "Missing distances in results"
        assert len(results["documents"][0]) > 0, "No results returned"
    
    def test_query_distances_valid(self):
        """Test that query distances are valid."""
        query_text = "HDFC Mid Cap Fund details"
        results = query_similar(query_text, n_results=5)
        
        distances = results["distances"][0]
        assert len(distances) > 0, "No distances returned"
        assert all(d >= 0 for d in distances), "Negative distances found"
        assert all(d <= 2 for d in distances), "Suspiciously large distances"
    
    def test_query_metadata_consistent(self):
        """Test that query metadata is consistent with documents."""
        query_text = "Fund performance"
        results = query_similar(query_text, n_results=3)
        
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        
        assert len(documents) == len(metadatas), "Documents and metadatas count mismatch"
        
        for metadata in metadatas:
            assert "scheme_name" in metadata, "Missing scheme_name in query results"


class TestMetadataFiltering:
    """Test metadata filtering edge cases."""
    
    def test_filter_by_scheme(self):
        """Test filtering by scheme name."""
        client = get_client()
        collection = get_or_create_collection(client)
        
        results = collection.get(where={"scheme_name": "HDFC Mid-Cap Fund (Direct Growth)"}, include=["metadatas"])
        
        assert len(results["metadatas"]) > 0, "No results for scheme filter"
        
        for metadata in results["metadatas"]:
            assert metadata["scheme_name"] == "HDFC Mid-Cap Fund (Direct Growth)", "Filter not working correctly"
    
    def test_filter_by_category(self):
        """Test filtering by category."""
        client = get_client()
        collection = get_or_create_collection(client)
        
        results = collection.get(where={"category": "Mid Cap"}, include=["metadatas"])
        
        assert len(results["metadatas"]) > 0, "No results for category filter"
        
        for metadata in results["metadatas"]:
            assert metadata["category"] == "Mid Cap", "Filter not working correctly"


class TestDataIntegrity:
    """Test data integrity edge cases."""
    
    def test_no_null_embeddings(self):
        """Test that there are no null embeddings."""
        client = get_client()
        collection = get_or_create_collection(client)
        
        results = collection.get(include=["embeddings"])
        
        for embedding in results["embeddings"]:
            assert embedding is not None, "Null embedding found"
            assert len(embedding) == EMBEDDING_DIMENSIONS, f"Invalid embedding dimension: {len(embedding)}"
    
    def test_no_empty_documents(self):
        """Test that there are no empty documents."""
        client = get_client()
        collection = get_or_create_collection(client)
        
        results = collection.get(include=["documents"])
        
        for doc in results["documents"]:
            assert doc.strip(), "Empty document found"
            assert len(doc) > 50, f"Suspiciously short document: {len(doc)}"


class TestCollectionStats:
    """Test collection statistics edge cases."""
    
    def test_stats_returned(self):
        """Test that collection stats are returned."""
        stats = get_collection_stats()
        
        assert "collection" in stats, "Missing collection name in stats"
        assert "total_vectors" in stats, "Missing total_vectors in stats"
    
    def test_stats_consistent(self):
        """Test that stats are consistent with actual data."""
        client = get_client()
        collection = get_or_create_collection(client)
        
        stats = get_collection_stats()
        actual_count = collection.count()
        
        assert stats["total_vectors"] == actual_count, f"Stats mismatch: {stats['total_vectors']} vs {actual_count}"


class TestIndexCorruption:
    """Test index corruption edge cases."""
    
    def test_all_ids_unique(self):
        """Test that all chunk IDs are unique."""
        client = get_client()
        collection = get_or_create_collection(client)
        
        results = collection.get(include=["documents"])
        ids = results["ids"]
        
        assert len(ids) == len(set(ids)), "Duplicate IDs found in collection"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
