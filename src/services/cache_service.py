import time
import hashlib
from typing import Optional, Dict, TypedDict


class CachedData(TypedDict):
    response: str
    timestamp: float


class CacheService:
    """A simple in-memory cache with time-to-live functionality."""

    CACHE_TTL: int = 60  # Time-to-live for cache entries in seconds
    _cache: Dict[str, CachedData] = {}

    def generate_cache_key(self, query: str) -> str:
        """
        Generate a unique cache key using a SHA-256 hash of the query.

        Args:
            query (str): The input query to hash.

        Returns:
            str: A hexadecimal hash string.
        """
        return hashlib.sha256(query.encode()).hexdigest()

    def get_cached_response(self, query: str) -> Optional[str]:
        """
        Retrieve a cached response if it exists and is still valid.

        Args:
            query (str): The input query.

        Returns:
            Optional[str]: The cached response if valid, otherwise None.
        """
        cache_key = self.generate_cache_key(query)
        cached_data = self._cache.get(cache_key)

        if cached_data:
            if time.time() - cached_data['timestamp'] < self.CACHE_TTL:
                return cached_data['response']

        return None

    def set_cache(self, query: str, response: str) -> None:
        """
        Store a response in the cache with the current timestamp.

        Args:
            query (str): The input query.
            response (str): The response to cache.
        """
        cache_key = self.generate_cache_key(query)
        self._cache[cache_key] = {
            "response": response,
            "timestamp": time.time()
        }
