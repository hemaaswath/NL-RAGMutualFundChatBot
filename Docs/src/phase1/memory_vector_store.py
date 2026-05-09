"""
In-memory vector store fallback for deployment when ChromaDB fails.
"""

import os
import json
import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path
from .embeddings import generate_embeddings
from .utils import setup_logging

logger = setup_logging("memory_vector_store")

class MemoryVectorStore:
    """Simple in-memory vector store as fallback when ChromaDB fails."""
    
    def __init__(self):
        self.chunks = []
        self.embeddings = []
        self.metadata = []
        self.is_loaded = False
    
    def load_from_chunks(self, chunk_paths: List[str]) -> bool:
        """Load chunks and embeddings from JSON files."""
        try:
            all_chunks = []
            
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
            embeddings = generate_embeddings(texts)
            
            # Store in memory
            self.chunks = all_chunks
            self.embeddings = embeddings
            self.metadata = metadata
            self.is_loaded = True
            
            logger.info(f"Successfully loaded {len(all_chunks)} chunks with embeddings")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load chunks: {e}")
            return False
    
    def query(self, query_text: str, top_k: int = 5, similarity_threshold: float = 0.5) -> List[Dict]:
        """Query the in-memory vector store."""
        if not self.is_loaded:
            logger.error("Vector store not loaded!")
            return []
        
        try:
            # Generate query embedding
            query_embedding = generate_embeddings([query_text])[0]
            
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
        return len(self.chunks) if self.is_loaded else 0

# Global instance
_memory_store = None

def get_memory_store() -> MemoryVectorStore:
    """Get or create the global memory store instance."""
    global _memory_store
    if _memory_store is None:
        _memory_store = MemoryVectorStore()
    return _memory_store

def initialize_memory_store() -> bool:
    """Initialize the memory store from committed chunks."""
    store = get_memory_store()
    
    # Try multiple paths for chunks
    chunk_paths = [
        "data/chunks",
        "./data/chunks",
        "Docs/src/data/chunks",
        "./Docs/src/data/chunks",
        "/app/data/chunks",
    ]
    
    return store.load_from_chunks(chunk_paths)
