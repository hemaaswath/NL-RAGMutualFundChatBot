"""
Caching Layer for Phase 2: RAG Pipeline
Implements query-result caching with TTL
"""

import hashlib
import json
import time
from pathlib import Path
from typing import Optional
from .config import CACHE_ENABLED, CACHE_TTL, CACHE_DIR
from .utils import setup_logging

logger = setup_logging("cache")


class QueryCache:
    """Simple file-based cache for query results."""
    
    def __init__(self, cache_dir: Path = CACHE_DIR, ttl: int = CACHE_TTL):
        self.cache_dir = Path(cache_dir)
        self.ttl = ttl
        self.enabled = CACHE_ENABLED
        
        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Cache enabled: {self.cache_dir} (TTL: {ttl}s)")
        else:
            logger.info("Cache disabled")
    
    def _get_cache_key(self, query: str, scheme: Optional[str] = None) -> str:
        """Generate cache key from query and optional scheme filter."""
        key_data = f"{query}|{scheme}" if scheme else query
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get file path for cache entry."""
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, query: str, scheme: Optional[str] = None) -> Optional[dict]:
        """
        Get cached result for a query.
        
        Args:
            query: User query
            scheme: Optional scheme filter
        
        Returns:
            Cached result dict or None if not found/expired
        """
        if not self.enabled:
            return None
        
        cache_key = self._get_cache_key(query, scheme)
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists():
            logger.debug(f"Cache miss: {query[:50]}...")
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cache_entry = json.load(f)
            
            # Check if expired
            if time.time() - cache_entry["timestamp"] > self.ttl:
                logger.debug(f"Cache expired: {query[:50]}...")
                cache_path.unlink()
                return None
            
            logger.info(f"Cache hit: {query[:50]}...")
            return cache_entry["data"]
        
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
            return None
    
    def set(self, query: str, data: dict, scheme: Optional[str] = None) -> bool:
        """
        Cache result for a query.
        
        Args:
            query: User query
            data: Result data to cache
            scheme: Optional scheme filter
        
        Returns:
            True if cached successfully, False otherwise
        """
        if not self.enabled:
            return False
        
        cache_key = self._get_cache_key(query, scheme)
        cache_path = self._get_cache_path(cache_key)
        
        cache_entry = {
            "timestamp": time.time(),
            "query": query,
            "scheme": scheme,
            "data": data
        }
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(cache_entry, f)
            
            logger.debug(f"Cached result: {query[:50]}...")
            return True
        
        except Exception as e:
            logger.error(f"Error writing cache: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache entries."""
        if not self.enabled:
            return False
        
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            
            logger.info("Cache cleared")
            return True
        
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
    
    def invalidate_scheme(self, scheme: str) -> bool:
        """Invalidate cache entries for a specific scheme."""
        if not self.enabled:
            return False
        
        try:
            cleared = 0
            for cache_file in self.cache_dir.glob("*.json"):
                with open(cache_file, 'r') as f:
                    cache_entry = json.load(f)
                
                if cache_entry.get("scheme") == scheme:
                    cache_file.unlink()
                    cleared += 1
            
            logger.info(f"Invalidated {cleared} cache entries for scheme: {scheme}")
            return True
        
        except Exception as e:
            logger.error(f"Error invalidating scheme cache: {e}")
            return False
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        if not self.enabled:
            return {"enabled": False}
        
        try:
            cache_files = list(self.cache_dir.glob("*.json"))
            total_entries = len(cache_files)
            
            # Count expired entries
            expired = 0
            for cache_file in cache_files:
                with open(cache_file, 'r') as f:
                    cache_entry = json.load(f)
                
                if time.time() - cache_entry["timestamp"] > self.ttl:
                    expired += 1
            
            return {
                "enabled": True,
                "total_entries": total_entries,
                "expired_entries": expired,
                "valid_entries": total_entries - expired,
                "ttl": self.ttl
            }
        
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"enabled": True, "error": str(e)}


# Global cache instance
_cache_instance = None


def get_cache() -> QueryCache:
    """Get global cache instance (singleton)."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = QueryCache()
    return _cache_instance


if __name__ == "__main__":
    # Test cache
    cache = QueryCache()
    
    # Test set and get
    test_query = "What is the expense ratio?"
    test_data = {"answer": "1.25%", "source": "test"}
    
    cache.set(test_query, test_data)
    result = cache.get(test_query)
    
    print(f"Set data: {test_data}")
    print(f"Got data: {result}")
    
    # Test stats
    stats = cache.get_stats()
    print(f"\nCache stats: {stats}")
