from abc import ABC, abstractmethod
from typing import Tuple

class BaseStorage(ABC):
    """Base storage interface for rate limiting"""
    
    @abstractmethod
    async def increment(self, key: str, expiry: int) -> int:
        """Increment the counter for the given key"""
        pass
    
    @abstractmethod
    async def get(self, key: str) -> int:
        """Get the current count for the given key"""
        pass
    
    @abstractmethod
    async def reset(self, key: str) -> None:
        """Reset the counter for the given key"""
        pass

    @abstractmethod
    async def get_tokens(self, key: str) -> Tuple[int, float]:
        """Get the current tokens and last update time for the given key"""
        pass

    @abstractmethod
    async def set_tokens(self, key: str, tokens: int, timestamp: float) -> None:
        """Set the tokens and last update time for the given key"""
        pass

    @abstractmethod
    async def distributed_lock(self, key: str, timeout: int = 1):
        """Acquire a distributed lock for the given key"""
        pass
