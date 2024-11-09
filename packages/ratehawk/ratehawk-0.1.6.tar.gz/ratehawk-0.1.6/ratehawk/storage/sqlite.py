import asyncio
import time
from typing import Optional, Tuple
import aiosqlite
from contextlib import asynccontextmanager

from ..exceptions import StorageError
from .base import BaseStorage


class SQLiteStorage(BaseStorage):
    def __init__(self, db_path: str = "ratehawk.db"):
        self.db_path = db_path
        self._db: Optional[aiosqlite.Connection] = None
        self._lock = asyncio.Lock()

    async def _ensure_connection(self):
        if self._db is None:
            try:
                self._db = await aiosqlite.connect(self.db_path)
                await self._db.execute("""
                    CREATE TABLE IF NOT EXISTS rate_limits (
                        key TEXT PRIMARY KEY,
                        tokens INTEGER NOT NULL,
                        last_update REAL NOT NULL
                    )
                """)
                await self._db.commit()
            except Exception as e:
                raise StorageError(f"Failed to connect to SQLite database: {str(e)}")

    async def get_tokens(self, key: str) -> Tuple[int, float]:
        await self._ensure_connection()
        async with self._lock:
            try:
                async with self._db.execute(
                    "SELECT tokens, last_update FROM rate_limits WHERE key = ?",
                    (key,)
                ) as cursor:
                    row = await cursor.fetchone()
                    if row is None:
                        return 0, 0.0
                    return row[0], row[1]
            except Exception as e:
                raise StorageError(f"Failed to get tokens from SQLite: {str(e)}")

    async def set_tokens(self, key: str, tokens: int, timestamp: float) -> None:
        await self._ensure_connection()
        async with self._lock:
            try:
                await self._db.execute("""
                    INSERT INTO rate_limits (key, tokens, last_update)
                    VALUES (?, ?, ?)
                    ON CONFLICT(key) DO UPDATE SET
                        tokens = excluded.tokens,
                        last_update = excluded.last_update
                """, (key, tokens, timestamp))
                await self._db.commit()
            except Exception as e:
                raise StorageError(f"Failed to set tokens in SQLite: {str(e)}")

    async def reset(self, key: str) -> None:
        await self._ensure_connection()
        async with self._lock:
            try:
                await self._db.execute("DELETE FROM rate_limits WHERE key = ?", (key,))
                await self._db.commit()
            except Exception as e:
                raise StorageError(f"Failed to reset tokens in SQLite: {str(e)}")

    async def close(self) -> None:
        if self._db is not None:
            try:
                await self._db.close()
                self._db = None
            except Exception as e:
                raise StorageError(f"Failed to close SQLite connection: {str(e)}")

    async def increment(self, key: str, expiry: int) -> int:
        await self._ensure_connection()
        async with self._lock:
            try:
                current_time = time.time()
                await self._db.execute("""
                    DELETE FROM rate_limits WHERE key = ? AND ? - last_update >= ?
                """, (key, current_time, expiry))
                await self._db.execute("""
                    INSERT INTO rate_limits (key, tokens, last_update)
                    VALUES (?, 1, ?)
                    ON CONFLICT(key) DO UPDATE SET
                        tokens = rate_limits.tokens + 1,
                        last_update = excluded.last_update
                """, (key, current_time))
                await self._db.commit()
                async with self._db.execute(
                    "SELECT tokens FROM rate_limits WHERE key = ?",
                    (key,)
                ) as cursor:
                    row = await cursor.fetchone()
                    return row[0] if row else 0
            except Exception as e:
                raise StorageError(f"Failed to increment tokens in SQLite: {str(e)}")

    async def get(self, key: str) -> int:
        await self._ensure_connection()
        async with self._lock:
            try:
                async with self._db.execute(
                    "SELECT tokens FROM rate_limits WHERE key = ?",
                    (key,)
                ) as cursor:
                    row = await cursor.fetchone()
                    return row[0] if row else 0
            except Exception as e:
                raise StorageError(f"Failed to get tokens from SQLite: {str(e)}")

    @asynccontextmanager
    async def distributed_lock(self, key: str, timeout: int = 1):
        """
        A simple distributed lock implementation using SQLite.
        While not truly distributed, it provides basic locking functionality.
        """
        lock_key = f"lock_{key}"
        try:
            await self._ensure_connection()
            async with self._lock:
                # Try to acquire lock
                await self._db.execute("""
                    CREATE TABLE IF NOT EXISTS locks (
                        lock_key TEXT PRIMARY KEY,
                        acquired_at REAL NOT NULL
                    )
                """)
                
                # Clean up old locks
                current_time = time.time()
                await self._db.execute(
                    "DELETE FROM locks WHERE ? - acquired_at >= ?",
                    (current_time, timeout)
                )
                
                # Try to acquire the lock
                try:
                    await self._db.execute(
                        "INSERT INTO locks (lock_key, acquired_at) VALUES (?, ?)",
                        (lock_key, current_time)
                    )
                    await self._db.commit()
                    yield
                except aiosqlite.IntegrityError:
                    # Lock is already held
                    raise StorageError("Failed to acquire lock")
        finally:
            # Release the lock
            async with self._lock:
                await self._db.execute("DELETE FROM locks WHERE lock_key = ?", (lock_key,))
                await self._db.commit()
