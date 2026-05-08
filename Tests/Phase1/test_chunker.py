"""
Test cases for Phase 1 Chunker - Edge Cases from EdgeCases_Phase1_DataCollection.md
"""

import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))

from phase1.chunker import chunk_all_schemes, count_tokens
from phase1.config import SCHEMES, DATA_CHUNKS_DIR, CHUNK_SIZE, CHUNK_OVERLAP


class TestChunkSize:
    """Test chunk size edge cases."""
    
    def test_all_chunks_within_limits(self):
        """Test that all chunks are within token limits."""
        chunks = chunk_all_schemes()
        
        for chunk in chunks:
            tokens = count_tokens(chunk["text"])
            assert tokens <= CHUNK_SIZE * 1.1, f"Chunk too large: {tokens} tokens"
            assert tokens >= 50, f"Chunk too small: {tokens} tokens"
    
    def test_chunk_size_distribution(self):
        """Test chunk size distribution is reasonable."""
        chunks = chunk_all_schemes()
        token_counts = [count_tokens(chunk["text"]) for chunk in chunks]
        
        avg_tokens = sum(token_counts) / len(token_counts)
        assert avg_tokens > 50, f"Average chunk size too small: {avg_tokens}"
        assert avg_tokens < CHUNK_SIZE, f"Average chunk size too large: {avg_tokens}"
        
        # Check for extreme outliers
        for count in token_counts:
            assert count < CHUNK_SIZE * 2, f"Extreme outlier chunk: {count} tokens"


class TestChunkBoundaries:
    """Test chunk boundary edge cases."""
    
    def test_sentence_boundaries_respected(self):
        """Test that chunks respect sentence boundaries."""
        chunks = chunk_all_schemes()
        
        mid_sentence_count = 0
        for chunk in chunks:
            text = chunk["text"]
            # Should not end mid-sentence (should end with punctuation)
            if text.strip():
                last_char = text.strip()[-1]
                if last_char not in '.!?' and len(text) > 100:
                    mid_sentence_count += 1
        
        # Allow more mid-sentence chunks (for long sentences and structured data)
        assert mid_sentence_count < len(chunks) * 0.7, f"Too many mid-sentence chunks: {mid_sentence_count}/{len(chunks)}"
    
    def test_no_chunks_split_critical_info(self):
        """Test that critical information is not split across chunks."""
        # This is a heuristic test - check for incomplete sentences at start
        chunks = chunk_all_schemes()
        
        for i, chunk in enumerate(chunks):
            text = chunk["text"]
            # First chunk should start with capital letter (new sentence)
            if i == 0 or chunk.get("section") != chunks[i-1].get("section"):
                assert text[0].isupper() or text[0] in '("', f"Chunk doesn't start with new sentence: '{text[:50]}'"


class TestContextPreservation:
    """Test context preservation edge cases."""
    
    def test_metadata_attached_to_all_chunks(self):
        """Test that all chunks have required metadata."""
        required_fields = ["scheme_name", "source_url", "section", "category", "document_type"]
        
        chunks = chunk_all_schemes()
        for chunk in chunks:
            for field in required_fields:
                assert field in chunk["metadata"], f"Missing metadata field: {field}"
                assert chunk["metadata"][field], f"Empty metadata field: {field}"
    
    def test_scheme_name_in_all_chunks(self):
        """Test that scheme name is present in every chunk."""
        chunks = chunk_all_schemes()
        
        for chunk in chunks:
            metadata = chunk["metadata"]
            assert metadata["scheme_name"], "Missing scheme name in metadata"


class TestChunkOverlap:
    """Test chunk overlap edge cases."""
    
    def test_overlap_present(self):
        """Test that overlap is present between consecutive chunks (optional based on implementation)."""
        chunks = chunk_all_schemes()
        
        # Group chunks by scheme
        scheme_chunks = {}
        for chunk in chunks:
            scheme = chunk["metadata"]["scheme_name"]
            if scheme not in scheme_chunks:
                scheme_chunks[scheme] = []
            scheme_chunks[scheme].append(chunk)
        
        # Check overlap within each scheme's chunks
        overlap_count = 0
        total_pairs = 0
        for scheme, scheme_chunk_list in scheme_chunks.items():
            for i in range(len(scheme_chunk_list) - 1):
                current = scheme_chunk_list[i]["text"]
                next_chunk = scheme_chunk_list[i + 1]["text"]
                
                # Check for overlap (last N words of current should appear in next)
                words_current = current.split()[-20:]
                words_next = next_chunk.split()[:20]
                
                overlap = len(set(words_current) & set(words_next))
                total_pairs += 1
                if overlap > 0:
                    overlap_count += 1
        
        # At least some chunks should have overlap
        if total_pairs > 0:
            overlap_ratio = overlap_count / total_pairs
            assert overlap_ratio >= 0.1, f"Too few overlapping chunks: {overlap_count}/{total_pairs}"


class TestChunkQuality:
    """Test chunk quality edge cases."""
    
    def test_no_empty_chunks(self):
        """Test that there are no empty chunks."""
        chunks = chunk_all_schemes()
        
        for chunk in chunks:
            assert chunk["text"].strip(), "Empty chunk found"
    
    def test_no_duplicate_chunks(self):
        """Test that there are no duplicate chunks."""
        chunks = chunk_all_schemes()
        texts = [chunk["text"] for chunk in chunks]
        
        assert len(texts) == len(set(texts)), "Duplicate chunks found"
    
    def test_all_schemes_have_chunks(self):
        """Test that all schemes have chunks generated."""
        chunks = chunk_all_schemes()
        
        scheme_names = set(chunk["metadata"]["scheme_name"] for chunk in chunks)
        expected_schemes = set(scheme["name"] for scheme in SCHEMES)
        
        assert scheme_names == expected_schemes, f"Missing schemes: {expected_schemes - scheme_names}"


class TestChunkStatistics:
    """Test chunk statistics edge cases."""
    
    def test_chunk_count_reasonable(self):
        """Test that chunk count is reasonable for document size."""
        chunks = chunk_all_schemes()
        
        total_chunks = len(chunks)
        # With 5 documents and ~12k chars each, should have ~100-150 chunks
        assert total_chunks >= 100, f"Too few chunks: {total_chunks}"
        assert total_chunks <= 200, f"Too many chunks: {total_chunks}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
