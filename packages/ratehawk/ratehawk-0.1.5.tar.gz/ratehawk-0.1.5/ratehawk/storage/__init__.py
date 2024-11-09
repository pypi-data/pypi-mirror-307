from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseStorage(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Dict[str, Any], expire: Optional[int] = None) -> None:
        pass

    @abstractmethod
    async def increment(self, key: str, amount: int = 1) -> int:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass 