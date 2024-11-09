from collections import deque
from contextlib import asynccontextmanager
import time
from typing import Tuple, Dict, Deque

class MemoryStorage:
    def __init__(self):
        self._storage: Dict[str, Tuple[int, float, Deque]] = {}
        self._locks: Dict[str, bool] = {}

    async def increment(self, key: str, window: int) -> int:
        if key not in self._storage:
            self._storage[key] = (0, time.time(), deque())
        count, last_update, history = self._storage[key]
        current_time = time.time()
        
        # Add new request to history
        history.append(current_time)
        count += 1
        
        # Remove expired entries
        while history and current_time - history[0] > window:
            history.popleft()
            count -= 1
            
        self._storage[key] = (count, current_time, history)
        return count

    async def get(self, key: str) -> int:
        if key not in self._storage:
            return 0
        count, _, _ = self._storage[key]
        return count

    async def reset(self, key: str) -> None:
        self._storage[key] = (0, time.time(), deque())

    async def get_tokens(self, key: str) -> Tuple[int, float]:
        if key not in self._storage:
            return (0, time.time())
        count, last_update, _ = self._storage[key]
        return (count, last_update)

    async def set_tokens(self, key: str, tokens: int, last_update: float) -> None:
        if key not in self._storage:
            self._storage[key] = (tokens, last_update, deque())
        else:
            _, _, history = self._storage[key]
            self._storage[key] = (tokens, last_update, history)

    @asynccontextmanager
    async def distributed_lock(self, key: str):
        lock_key = f"lock:{key}"
        if self._locks.get(lock_key):
            raise RuntimeError(f"Lock already acquired for {key}")
        
        try:
            self._locks[lock_key] = True
            yield
        finally:
            self._locks[lock_key] = False
