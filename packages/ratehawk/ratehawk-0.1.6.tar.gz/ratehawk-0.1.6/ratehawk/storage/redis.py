from redis import Redis
from redis.lock import Lock
from contextlib import asynccontextmanager
from .base import BaseStorage
from ..exceptions import StorageError
from typing import Optional, Tuple
import time

class RedisStorage(BaseStorage):
    def __init__(self, redis_client: Redis = None, **redis_kwargs):
        self.redis = redis_client or Redis(**redis_kwargs)
    
    async def increment(self, key: str, expiry: int) -> int:
        try:
            pipe = self.redis.pipeline()
            pipe.incr(key)
            pipe.expire(key, expiry)
            result = pipe.execute()
            return result[0]
        except Exception as e:
            raise StorageError(f"Redis error: {str(e)}")
    
    async def get(self, key: str) -> int:
        try:
            value = self.redis.get(key)
            return int(value) if value else 0
        except Exception as e:
            raise StorageError(f"Redis error: {str(e)}")
    
    async def reset(self, key: str) -> None:
        try:
            self.redis.delete(key)
        except Exception as e:
            raise StorageError(f"Redis error: {str(e)}")
    
    @asynccontextmanager
    async def distributed_lock(self, key: str, timeout: int = 1):
        lock = Lock(
            self.redis,
            f"ratelimit_lock:{key}",
            timeout=timeout,
            blocking_timeout=0.5
        )
        try:
            if lock.acquire():
                yield
            else:
                raise StorageError("Could not acquire lock")
        finally:
            if lock.locked():
                lock.release()

    async def get_tokens(self, key: str) -> Tuple[int, float]:
        try:
            hash_key = f"tokens:{key}"
            value = self.redis.hgetall(hash_key)
            if not value:
                return 0, 0.0
            tokens = value.get(b'tokens', value.get('tokens', 0))
            last_update = value.get(b'last_update', value.get('last_update', 0.0))
            return int(tokens), float(last_update)
        except Exception as e:
            raise StorageError(f"Redis error: {str(e)}")

    async def set_tokens(self, key: str, tokens: int, timestamp: float) -> None:
        try:
            hash_key = f"tokens:{key}"
            self.redis.hset(hash_key, mapping={'tokens': tokens, 'last_update': timestamp})
        except Exception as e:
            raise StorageError(f"Redis error: {str(e)}")
