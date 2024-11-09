from typing import Dict, Any, Optional
import time
from ..storage import BaseStorage

class MemoryStorage(BaseStorage):
    def __init__(self):
        self._storage: Dict[str, Any] = {}
        self._expiry: Dict[str, float] = {}

    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        if key in self._expiry and time.time() > self._expiry[key]:
            del self._storage[key]
            del self._expiry[key]
            return None
        return self._storage.get(key)

    async def set(self, key: str, value: Dict[str, Any], expire: Optional[int] = None) -> None:
        self._storage[key] = value
        if expire is not None:
            self._expiry[key] = time.time() + expire

    async def increment(self, key: str, amount: int = 1) -> int:
        if key not in self._storage:
            self._storage[key] = 0
        self._storage[key] += amount
        return self._storage[key]

    async def delete(self, key: str) -> None:
        self._storage.pop(key, None)
        self._expiry.pop(key, None)
