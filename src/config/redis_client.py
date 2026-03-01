"""
Redis client configuration for caching
"""
import redis
from typing import Optional, Any
import json
from .settings import settings


class RedisClient:
    """Redis client wrapper for caching operations"""
    
    def __init__(self):
        self.client = redis.from_url(
            settings.redis_url,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
        self.default_ttl = settings.redis_cache_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis GET error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with TTL"""
        try:
            ttl = ttl or self.default_ttl
            serialized = json.dumps(value)
            return self.client.setex(key, ttl, serialized)
        except Exception as e:
            print(f"Redis SET error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            print(f"Redis DELETE error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            print(f"Redis EXISTS error: {e}")
            return False
    
    def increment(self, key: str, amount: int = 1) -> int:
        """Increment counter"""
        try:
            return self.client.incr(key, amount)
        except Exception as e:
            print(f"Redis INCR error: {e}")
            return 0
    
    def expire(self, key: str, ttl: int) -> bool:
        """Set expiration on key"""
        try:
            return bool(self.client.expire(key, ttl))
        except Exception as e:
            print(f"Redis EXPIRE error: {e}")
            return False
    
    def flush_all(self) -> bool:
        """Flush all keys (use with caution!)"""
        try:
            return self.client.flushall()
        except Exception as e:
            print(f"Redis FLUSHALL error: {e}")
            return False


# Global Redis client instance
redis_client = RedisClient()
