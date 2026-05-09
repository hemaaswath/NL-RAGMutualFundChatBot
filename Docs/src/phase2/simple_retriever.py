"""
Simple retrieval system for Streamlit deployment.
Bypasses ChromaDB entirely and uses direct file-based retrieval.
"""

import os
import json
import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path
from phase1.embeddings import generate_single_embedding
from .config import TOP_K, SIMILARITY_THRESHOLD
from .utils import setup_logging

logger = setup_logging("simple_retriever")

class SimpleVectorStore:
    """Simple file-based vector store for Streamlit deployment."""
    
    def __init__(self):
        self.chunks = []
        self.embeddings = []
        self.metadata = []
        self.loaded = False
    
    def load_chunks(self) -> bool:
        """Load chunks and embeddings from JSON files."""
        try:
            # Try multiple paths for chunks
            chunk_paths = [
                "data/chunks",
                "./data/chunks",
                "Docs/src/data/chunks",
                "./Docs/src/data/chunks",
                "/app/data/chunks",
                str(Path.cwd() / "data" / "chunks"),
            ]
            
            all_chunks = []
            chunks_found = False
            
            for chunk_path in chunk_paths:
                chunks_dir = Path(chunk_path)
                if chunks_dir.exists() and any(chunks_dir.iterdir()):
                    logger.info(f"Loading chunks from: {chunk_path}")
                    for chunk_file in chunks_dir.glob("*_chunks.json"):
                        try:
                            with open(chunk_file, 'r', encoding='utf-8') as f:
                                file_chunks = json.load(f)
                                all_chunks.extend(file_chunks)
                                logger.info(f"Loaded {len(file_chunks)} chunks from {chunk_file.name}")
                        except Exception as e:
                            logger.error(f"Error loading {chunk_file}: {e}")
                    chunks_found = True
                    break
            
            if not chunks_found:
                logger.error("No chunks directory found!")
                return False
            
            if not all_chunks:
                logger.error("No chunks loaded!")
                return False
            
            # Extract texts and metadata
            texts = []
            metadata = []
            for chunk in all_chunks:
                texts.append(chunk['text'])
                metadata.append(chunk['metadata'])
            
            # Generate embeddings
            logger.info(f"Generating embeddings for {len(texts)} chunks...")
            from phase1.embeddings import generate_embeddings
            embeddings = generate_embeddings(texts)
            
            # Store in memory
            self.chunks = all_chunks
            self.embeddings = np.array(embeddings)
            self.metadata = metadata
            self.loaded = True
            
            logger.info(f"Successfully loaded {len(all_chunks)} chunks with embeddings")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load chunks: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def query(self, query_text: str, top_k: int = 5, similarity_threshold: float = 0.5) -> List[Dict]:
        """Query the vector store."""
        if not self.loaded:
            logger.error("Vector store not loaded!")
            return []
        
        try:
            # Generate query embedding
            query_embedding = generate_single_embedding(query_text)
            if query_embedding is None:
                logger.error("Failed to generate query embedding")
                return []
            
            # Calculate similarities
            similarities = []
            for chunk_embedding in self.embeddings:
                # Cosine similarity
                similarity = np.dot(query_embedding, chunk_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(chunk_embedding)
                )
                similarities.append(similarity)
            
            # Sort by similarity
            sorted_indices = np.argsort(similarities)[::-1]
            
            # Filter and return results
            results = []
            for idx in sorted_indices[:top_k]:
                if similarities[idx] >= similarity_threshold:
                    result = {
                        'text': self.chunks[idx]['text'],
                        'metadata': self.chunks[idx]['metadata'],
                        'similarity': float(similarities[idx]),
                        'distance': 1 - float(similarities[idx])
                    }
                    results.append(result)
            
            logger.info(f"Retrieved {len(results)} chunks above threshold {similarity_threshold}")
            return results
            
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return []
    
    def count(self) -> int:
        """Return number of vectors in store."""
        return len(self.chunks) if self.loaded else 0

# Global instance
_simple_store = None

def get_simple_store() -> SimpleVectorStore:
    """Get or create the global simple store instance."""
    global _simple_store
    if _simple_store is None:
        _simple_store = SimpleVectorStore()
    return _simple_store

def initialize_simple_store() -> bool:
    """Initialize the simple store from committed chunks."""
    store = get_simple_store()
    return store.load_chunks()

def retrieve_simple(
    query: str,
    top_k: int = TOP_K,
    similarity_threshold: float = SIMILARITY_THRESHOLD,
    where: Optional[dict] = None,
    scheme: Optional[str] = None,
) -> List[dict]:
    """
    Retrieve relevant chunks using simple vector store.
    
    Args:
        query: User query text
        top_k: Number of results to retrieve
        similarity_threshold: Minimum similarity score (0-1)
        where: Additional metadata filters (not implemented in simple version)
        scheme: Filter by specific scheme name (not implemented in simple version)
    
    Returns:
        List of retrieved chunks with metadata and scores
    """
    try:
        # Get store
        store = get_simple_store()
        if not store.loaded:
            logger.info("Initializing simple store...")
            if not initialize_simple_store():
                logger.error("Failed to initialize simple store!")
                return []
        
        # Query the store
        results = store.query(query, top_k, similarity_threshold)
        
        # Apply filters if provided (simple implementation)
        if scheme and results:
            filtered_results = []
            for result in results:
                if result['metadata'].get('scheme_name') == scheme:
                    filtered_results.append(result)
            results = filtered_results
        
        return results
        
    except Exception as e:
        logger.error(f"Simple retrieval failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return []
