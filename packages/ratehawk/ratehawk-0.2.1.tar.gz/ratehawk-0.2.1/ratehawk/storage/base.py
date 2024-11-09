from typing import Optional, Tuple, Dict
from abc import ABC, abstractmethod

class BaseStorage(ABC):
    """Base storage interface for rate limiting"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[int]:
        """Get the current count for the given key"""
        pass
    
    @abstractmethod
    async def set(self, key: str, value: any, expire: Optional[int] = None) -> None:
        """Set the value for the given key"""
        pass
    
    @abstractmethod
    async def increment(self, key: str, window: int) -> int:
        """Increment the counter for the given key"""
        pass
    
    @abstractmethod
    async def reset(self, key: str) -> None:
        """Reset the counter for the given key"""
        pass
    
    @abstractmethod
    async def get_last_update(self, key: str) -> Optional[float]:
        """Get the timestamp of the last update for a key"""
        pass
    
    @abstractmethod
    async def get_window_info(self, key: str) -> Optional[Tuple[int, float]]:
        """Get the current window count and start time"""
        pass
    
    @abstractmethod
    async def reset_window(self, key: str) -> None:
        """Reset the window for a key"""
        pass
    
    @abstractmethod
    async def get_storage_stats(self) -> Dict:
        """Get storage statistics"""
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
