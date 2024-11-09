import sqlite3
import time
from typing import Optional, Tuple, Dict
import aiosqlite
from .base import BaseStorage


class SQLiteStorage(BaseStorage):
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS rate_limits (
                    key TEXT PRIMARY KEY,
                    count INTEGER,
                    window_start REAL,
                    last_update REAL,
                    expire_at REAL
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_expire_at 
                ON rate_limits(expire_at)
            """)
    
    async def get(self, key: str) -> Optional[int]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT count FROM rate_limits WHERE key = ? AND expire_at > ?",
                (key, time.time())
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None
    
    async def set(self, key: str, value: any, expire: Optional[int] = None) -> None:
        expire_at = time.time() + (expire or 3600)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT OR REPLACE INTO rate_limits 
                (key, count, window_start, last_update, expire_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (key, value, time.time(), time.time(), expire_at)
            )
            await db.commit()
    
    async def increment(self, key: str, window: int) -> int:
        current_time = time.time()
        expire_at = current_time + window
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                """
                INSERT INTO rate_limits 
                (key, count, window_start, last_update, expire_at)
                VALUES (?, 1, ?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                count = count + 1,
                last_update = ?,
                expire_at = ?
                RETURNING count
                """,
                (key, current_time, current_time, expire_at, current_time, expire_at)
            ) as cursor:
                row = await cursor.fetchone()
                await db.commit()
                return row[0]
    
    async def reset(self, key: str) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM rate_limits WHERE key = ?", (key,))
            await db.commit()
    
    async def get_last_update(self, key: str) -> Optional[float]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT last_update FROM rate_limits WHERE key = ?",
                (key,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None
    
    async def get_window_info(self, key: str) -> Optional[Tuple[int, float]]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                """
                SELECT count, window_start 
                FROM rate_limits 
                WHERE key = ? AND expire_at > ?
                """,
                (key, time.time())
            ) as cursor:
                row = await cursor.fetchone()
                return (row[0], row[1]) if row else None
    
    async def reset_window(self, key: str) -> None:
        current_time = time.time()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                UPDATE rate_limits 
                SET count = 0, 
                    window_start = ?,
                    last_update = ?
                WHERE key = ?
                """,
                (current_time, current_time, key)
            )
            await db.commit()
    
    async def get_storage_stats(self) -> Dict:
        async with aiosqlite.connect(self.db_path) as db:
            stats = {}
            
            # Get total keys
            async with db.execute("SELECT COUNT(*) FROM rate_limits") as cursor:
                row = await cursor.fetchone()
                stats["total_keys"] = row[0]
            
            # Get expired keys
            async with db.execute(
                "SELECT COUNT(*) FROM rate_limits WHERE expire_at <= ?",
                (time.time(),)
            ) as cursor:
                row = await cursor.fetchone()
                stats["expired_keys"] = row[0]
            
            # Get average requests per key
            async with db.execute(
                "SELECT AVG(count) FROM rate_limits WHERE expire_at > ?",
                (time.time(),)
            ) as cursor:
                row = await cursor.fetchone()
                stats["avg_requests_per_key"] = float(row[0]) if row[0] else 0
            
            return stats
