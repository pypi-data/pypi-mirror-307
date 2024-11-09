import asyncio
import time
from typing import Optional, Tuple
import asyncpg

from ..exceptions import StorageError
from .base import BaseStorage


class PostgresStorage(BaseStorage):
    def __init__(
        self,
        dsn: str = "postgresql://localhost/ratehawk",
        pool_size: int = 10,
        **kwargs
    ):
        self.dsn = dsn
        self.pool_size = pool_size
        self.pool_kwargs = kwargs
        self._pool: Optional[asyncpg.Pool] = None
        self._lock = asyncio.Lock()

    async def _ensure_pool(self):
        if self._pool is None:
            try:
                self._pool = await asyncpg.create_pool(
                    self.dsn,
                    min_size=1,
                    max_size=self.pool_size,
                    **self.pool_kwargs
                )
                
                # Create the rate limits table if it doesn't exist
                async with self._pool.acquire() as conn:
                    await conn.execute("""
                        CREATE TABLE IF NOT EXISTS rate_limits (
                            key TEXT PRIMARY KEY,
                            tokens INTEGER NOT NULL,
                            last_update DOUBLE PRECISION NOT NULL
                        )
                    """)
            except Exception as e:
                raise StorageError(f"Failed to connect to PostgreSQL: {str(e)}")

    async def get_tokens(self, key: str) -> Tuple[int, float]:
        await self._ensure_pool()
        async with self._lock:
            try:
                async with self._pool.acquire() as conn:
                    row = await conn.fetchrow(
                        "SELECT tokens, last_update FROM rate_limits WHERE key = $1",
                        key
                    )
                    if row is None:
                        return 0, 0.0
                    return row['tokens'], row['last_update']
            except Exception as e:
                raise StorageError(f"Failed to get tokens from PostgreSQL: {str(e)}")

    async def set_tokens(self, key: str, tokens: int, timestamp: float) -> None:
        await self._ensure_pool()
        async with self._lock:
            try:
                async with self._pool.acquire() as conn:
                    await conn.execute("""
                        INSERT INTO rate_limits (key, tokens, last_update)
                        VALUES ($1, $2, $3)
                        ON CONFLICT (key) DO UPDATE SET
                            tokens = EXCLUDED.tokens,
                            last_update = EXCLUDED.last_update
                    """, key, tokens, timestamp)
            except Exception as e:
                raise StorageError(f"Failed to set tokens in PostgreSQL: {str(e)}")

    async def reset(self, key: str) -> None:
        await self._ensure_pool()
        async with self._lock:
            try:
                async with self._pool.acquire() as conn:
                    await conn.execute(
                        "DELETE FROM rate_limits WHERE key = $1",
                        key
                    )
            except Exception as e:
                raise StorageError(f"Failed to reset tokens in PostgreSQL: {str(e)}")

    async def close(self) -> None:
        if self._pool is not None:
            try:
                await self._pool.close()
                self._pool = None
            except Exception as e:
                raise StorageError(f"Failed to close PostgreSQL connection pool: {str(e)}")

    async def increment(self, key: str, expiry: int) -> int:
        await self._ensure_pool()
        async with self._lock:
            try:
                current_time = time.time()
                async with self._pool.acquire() as conn:
                    await conn.execute("""
                        DELETE FROM rate_limits WHERE key = $1 AND $2 - last_update >= $3
                    """, key, current_time, expiry)
                    await conn.execute("""
                        INSERT INTO rate_limits (key, tokens, last_update)
                        VALUES ($1, 1, $2)
                        ON CONFLICT (key) DO UPDATE SET
                            tokens = rate_limits.tokens + 1,
                            last_update = EXCLUDED.last_update
                    """, key, current_time)
                    row = await conn.fetchrow(
                        "SELECT tokens FROM rate_limits WHERE key = $1",
                        key
                    )
                    return row['tokens'] if row else 0
            except Exception as e:
                raise StorageError(f"Failed to increment tokens in PostgreSQL: {str(e)}")

    async def get(self, key: str) -> int:
        await self._ensure_pool()
        async with self._lock:
            try:
                async with self._pool.acquire() as conn:
                    row = await conn.fetchrow(
                        "SELECT tokens FROM rate_limits WHERE key = $1",
                        key
                    )
                    return row['tokens'] if row else 0
            except Exception as e:
                raise StorageError(f"Failed to get tokens from PostgreSQL: {str(e)}")

    def distributed_lock(self, key: str, timeout: int = 1):
        """Implement a proper distributed lock using PostgreSQL advisory locks"""
        # Convert the key string to a consistent integer for advisory lock
        lock_key = hash(f"ratehawk:{key}") & 0xffffffff  # Ensure it fits in 32 bits
        
        class PostgresLock:
            def __init__(self, storage, lock_key):
                self.storage = storage
                self.lock_key = lock_key
                self.conn = None

            async def __aenter__(self):
                await self.storage._ensure_pool()
                self.conn = await self.storage._pool.acquire()
                # Try to acquire advisory lock
                await self.conn.execute('SELECT pg_advisory_lock($1)', self.lock_key)
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                if self.conn:
                    # Release advisory lock
                    await self.conn.execute('SELECT pg_advisory_unlock($1)', self.lock_key)
                    await self.storage._pool.release(self.conn)
                    self.conn = None

        return PostgresLock(self, lock_key)
