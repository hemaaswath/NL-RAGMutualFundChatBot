"""
RAG Service for Phase 3 API
Integrates with Phase 2 RAG pipeline
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from phase2.pipeline import rag_pipeline, get_available_schemes, get_cache_stats


class RAGService:
    """Service layer for RAG operations."""
    
    @staticmethod
    def process_query(query: str, scheme: str = None, use_cache: bool = True):
        """
        Process a query through the RAG pipeline.
        
        Args:
            query: User query
            scheme: Optional scheme filter
            use_cache: Whether to use cache
        
        Returns:
            RAG pipeline result
        """
        return rag_pipeline(query, scheme=scheme, use_cache=use_cache)
    
    @staticmethod
    def get_schemes():
        """
        Get list of available schemes.
        
        Returns:
            List of scheme names
        """
        return get_available_schemes()
    
    @staticmethod
    def get_cache_statistics():
        """
        Get cache statistics.
        
        Returns:
            Cache statistics dictionary
        """
        return get_cache_stats()
