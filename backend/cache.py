import redis
import json
from typing import Optional, Any
from config import REDIS_URL

redis_client = redis.from_url(REDIS_URL)

# Cache TTL in seconds (e.g., 15 minutes)
CACHE_TTL = 900

def get_from_cache(key: str) -> Optional[Any]:
    """Retrieve an item from the cache."""
    cached_value = redis_client.get(key)
    if cached_value:
        return json.loads(cached_value)
    return None

def set_in_cache(key: str, value: Any):
    """Set an item in the cache with a TTL."""
    redis_client.setex(key, CACHE_TTL, json.dumps(value))
