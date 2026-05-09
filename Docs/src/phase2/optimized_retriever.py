"""
Optimized Simple Retriever for Fast Deployment
Implements caching and lazy loading to reduce startup time
"""

import json
import numpy as np
import os
import pickle
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class OptimizedSimpleRetriever:
    """Optimized simple retriever with caching and lazy loading."""
    
    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Lazy loading - don't load until first query
        self.chunks = None
        self.embeddings = None
        self.metadata = None
        self.loaded = False
        
        # Cache file paths
        self.embeddings_cache_file = self.cache_dir / "embeddings_cache.pkl"
        self.chunks_cache_file = self.cache_dir / "chunks_cache.json"
        
        logger.info("Optimized retriever initialized (lazy loading enabled)")
    
    def _get_cache_key(self, chunk_files: List[str]) -> str:
        """Generate cache key based on chunk file modification times."""
        key_data = ""
        for file_path in chunk_files:
            if os.path.exists(file_path):
                mtime = os.path.getmtime(file_path)
                size = os.path.getsize(file_path)
                key_data += f"{file_path}:{mtime}:{size}|"
        
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _load_from_cache(self, cache_key: str) -> bool:
        """Load embeddings from cache if available and valid."""
        try:
            cache_info_file = self.cache_dir / f"cache_info_{cache_key}.json"
            
            if not cache_info_file.exists():
                return False
                
            with open(cache_info_file, 'r') as f:
                cache_info = json.load(f)
            
            # Check if cache is still valid
            if cache_info.get('cache_key') != cache_key:
                return False
            
            # Load cached data
            if self.embeddings_cache_file.exists() and self.chunks_cache_file.exists():
                logger.info("Loading embeddings from cache...")
                
                with open(self.embeddings_cache_file, 'rb') as f:
                    self.embeddings = pickle.load(f)
                
                with open(self.chunks_cache_file, 'r') as f:
                    data = json.load(f)
                    self.chunks = data['chunks']
                    self.metadata = data['metadata']
                
                self.loaded = True
                logger.info(f"Successfully loaded {len(self.chunks)} chunks from cache")
                return True
                
        except Exception as e:
            logger.warning(f"Failed to load from cache: {e}")
        
        return False
    
    def _save_to_cache(self, cache_key: str) -> None:
        """Save embeddings to cache for future use."""
        try:
            logger.info("Saving embeddings to cache...")
            
            # Save embeddings
            with open(self.embeddings_cache_file, 'wb') as f:
                pickle.dump(self.embeddings, f)
            
            # Save chunks and metadata
            data = {
                'chunks': self.chunks,
                'metadata': self.metadata
            }
            with open(self.chunks_cache_file, 'w') as f:
                json.dump(data, f)
            
            # Save cache info
            cache_info_file = self.cache_dir / f"cache_info_{cache_key}.json"
            cache_info = {
                'cache_key': cache_key,
                'timestamp': os.path.getmtime(self.embeddings_cache_file)
            }
            with open(cache_info_file, 'w') as f:
                json.dump(cache_info, f)
            
            logger.info("Successfully saved embeddings to cache")
            
        except Exception as e:
            logger.warning(f"Failed to save to cache: {e}")
    
    def _load_chunks_and_generate_embeddings(self) -> bool:
        """Load chunks and generate embeddings."""
        try:
            # Find chunk files
            chunk_paths_to_try = [
                "data/chunks",
                "./data/chunks",
                "Docs/src/data/chunks",
                "./Docs/src/data/chunks",
                "/app/data/chunks",
            ]
            
            chunks_dir = None
            for path in chunk_paths_to_try:
                if Path(path).exists() and any(Path(path).iterdir()):
                    chunks_dir = Path(path)
                    break
            
            if not chunks_dir:
                logger.error("No chunks directory found!")
                return False
            
            # Load chunks
            all_chunks = []
            texts = []
            metadata = []
            
            chunk_files = []
            for chunk_file in chunks_dir.glob("*_chunks.json"):
                try:
                    with open(chunk_file, 'r', encoding='utf-8') as f:
                        file_chunks = json.load(f)
                        all_chunks.extend(file_chunks)
                        chunk_files.append(str(chunk_file))
                        
                        for chunk in file_chunks:
                            texts.append(chunk['text'])
                            metadata.append(chunk['metadata'])
                            
                except Exception as e:
                    logger.error(f"Error loading {chunk_file}: {e}")
            
            if not all_chunks:
                logger.error("No chunks loaded!")
                return False
            
            # Check cache first
            cache_key = self._get_cache_key(chunk_files)
            if self._load_from_cache(cache_key):
                return True
            
            # Generate embeddings (only if not cached)
            logger.info(f"Generating embeddings for {len(texts)} chunks...")
            from phase1.embeddings import generate_embeddings
            
            # Use larger batch size for faster processing
            batch_size = 100
            embeddings = []
            
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_embeddings = generate_embeddings(batch_texts)
                embeddings.extend(batch_embeddings)
                
                logger.info(f"Processed {i + len(batch_texts)}/{len(texts)} chunks...")
            
            # Store in memory
            self.chunks = all_chunks
            self.embeddings = np.array(embeddings)
            self.metadata = metadata
            self.loaded = True
            
            # Save to cache for future use
            self._save_to_cache(cache_key)
            
            logger.info(f"Successfully loaded {len(all_chunks)} chunks with embeddings")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load chunks: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def _ensure_loaded(self):
        """Ensure data is loaded (lazy loading)."""
        if not self.loaded:
            logger.info("Loading chunks on first query (lazy loading)...")
            self._load_chunks_and_generate_embeddings()
    
    def query(self, query_text: str, top_k: int = 5, similarity_threshold: float = 0.3) -> List[Dict]:
        """Query the vector store."""
        self._ensure_loaded()
        
        if not self.loaded:
            logger.error("Vector store not loaded!")
            return []
        
        try:
            # Generate query embedding
            from phase1.embeddings import generate_embeddings
            query_embedding = generate_embeddings([query_text])[0]
            
            # Calculate similarities
            similarities = np.dot(self.embeddings, query_embedding)
            
            # Get top results above threshold
            top_indices = np.argsort(similarities)[::-1]
            results = []
            
            for idx in top_indices:
                if similarities[idx] >= similarity_threshold and len(results) < top_k:
                    result = {
                        'chunk': self.chunks[idx],
                        'similarity': float(similarities[idx]),
                        'metadata': self.metadata[idx]
                    }
                    results.append(result)
            
            logger.info(f"Retrieved {len(results)} chunks above threshold {similarity_threshold}")
            return results
            
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return []

# Global optimized retriever instance
_optimized_retriever = None

def get_optimized_retriever() -> OptimizedSimpleRetriever:
    """Get singleton optimized retriever instance."""
    global _optimized_retriever
    if _optimized_retriever is None:
        _optimized_retriever = OptimizedSimpleRetriever()
    return _optimized_retriever

def retrieve_optimized(query: str, top_k: int = 5, similarity_threshold: float = 0.3) -> List[Dict]:
    """Optimized retrieval function."""
    retriever = get_optimized_retriever()
    return retriever.query(query, top_k, similarity_threshold)
