import time
from typing import Optional, Callable, Dict, List, Tuple
from .storage.base import BaseStorage
from .storage.memory import MemoryStorage
from .exceptions import RateLimitExceeded
from .monitoring.metrics import RateLimitMetrics
from .monitoring.events import EventEmitter, RateLimitEvent
from .monitoring.logging import RateLimitLogger

class RateLimiter:
    def __init__(
        self,
        limits: List[Tuple[int, int]],
        burst_limits: Optional[List[Tuple[int, int]]] = None,
        storage: Optional[BaseStorage] = None,
        key_func: Optional[Callable] = None,
        near_limit_threshold: float = 0.8,
        dynamic_limits_func: Optional[Callable] = None,
        quota_limits: Optional[List[Tuple[int, int]]] = None
    ):
        """
        Initialize rate limiter
        
        Args:
            limits: List of tuples representing (limit, window) for rate limiting
            burst_limits: List of tuples representing (burst_limit, burst_window)
            storage: Storage backend (defaults to in-memory storage)
            key_func: Function to generate key for rate limiting (defaults to IP-based)
            near_limit_threshold: Threshold for near-limit condition
            dynamic_limits_func: Function to dynamically determine rate limits
            quota_limits: List of tuples representing (quota_limit, quota_window)
        """
        self.limits = limits
        self.burst_limits = burst_limits or [(limit * 2, window // 4) for limit, window in limits]
        self.storage = storage or MemoryStorage()
        self.key_func = key_func or (lambda: "default")
        self.near_limit_threshold = near_limit_threshold
        self.dynamic_limits_func = dynamic_limits_func
        self.quota_limits = quota_limits or []
        
        # Initialize monitoring components
        self.metrics = RateLimitMetrics()
        self.events = EventEmitter()
        self.logger = RateLimitLogger()
    
    async def check(self, key: Optional[str] = None) -> bool:
        """Check if rate limit is exceeded without incrementing"""
        key = key or self.key_func()
        self.metrics.start_timing(key)
        
        try:
            count = await self.storage.get(key)
            success = all(count < limit for limit, _ in self.limits)
            
            self.metrics.track_request(key, success)
            self.metrics.update_usage(key, count, max(limit for limit, _ in self.limits))
            
            # Check for near-limit condition
            if any(count >= (limit * self.near_limit_threshold) for limit, _ in self.limits):
                self.events.emit(
                    RateLimitEvent.NEAR_LIMIT,
                    key=key,
                    current=count,
                    limit=max(limit for limit, _ in self.limits)
                )
                self.logger.log_near_limit(key, count, max(limit for limit, _ in self.limits))
                
            return success
        finally:
            self.metrics.stop_timing(key)
    
    async def increment(self, key: Optional[str] = None) -> None:
        """Increment rate limit counter and raise exception if limit exceeded"""
        key = key or self.key_func()
        self.metrics.start_timing(key)
        
        try:
            count = await self.storage.increment(key, max(window for _, window in self.limits))
            self.metrics.update_usage(key, count, max(limit for limit, _ in self.limits))
            self.logger.log_request(key, count, max(limit for limit, _ in self.limits))
            
            if any(count > limit for limit, _ in self.limits):
                retry_after = max(window for _, window in self.limits)
                self.metrics.track_exceeded(key)
                self.events.emit(
                    RateLimitEvent.LIMIT_EXCEEDED,
                    key=key,
                    retry_after=retry_after
                )
                self.logger.log_exceeded(key, retry_after)
                raise RateLimitExceeded(retry_after=retry_after)
                
        finally:
            self.metrics.stop_timing(key)
    
    async def reset(self, key: Optional[str] = None) -> None:
        """Reset rate limit counter"""
        key = key or self.key_func()
        await self.storage.reset(key)
        self.metrics.update_usage(key, 0, max(limit for limit, _ in self.limits))
        self.events.emit(RateLimitEvent.RESET, key=key)
    
    async def apply_dynamic_limits(self, key: Optional[str] = None) -> None:
        """Apply dynamic rate limits based on user attributes or time of day"""
        if self.dynamic_limits_func:
            dynamic_limits = self.dynamic_limits_func()
            self.limits = dynamic_limits.get("limits", self.limits)
            self.burst_limits = dynamic_limits.get("burst_limits", self.burst_limits)
            self.quota_limits = dynamic_limits.get("quota_limits", self.quota_limits)
    
    async def check_quota(self, key: Optional[str] = None) -> bool:
        """Check if quota limit is exceeded without incrementing"""
        key = key or self.key_func()
        self.metrics.start_timing(key)
        
        try:
            count = await self.storage.get(key)
            success = all(count < quota for quota, _ in self.quota_limits)
            
            self.metrics.track_request(key, success)
            self.metrics.update_usage(key, count, max(quota for quota, _ in self.quota_limits))
            
            # Check for near-limit condition
            if any(count >= (quota * self.near_limit_threshold) for quota, _ in self.quota_limits):
                self.events.emit(
                    RateLimitEvent.NEAR_LIMIT,
                    key=key,
                    current=count,
                    limit=max(quota for quota, _ in self.quota_limits)
                )
                self.logger.log_near_limit(key, count, max(quota for quota, _ in self.quota_limits))
                
            return success
        finally:
            self.metrics.stop_timing(key)
    
    async def increment_quota(self, key: Optional[str] = None) -> None:
        """Increment quota limit counter and raise exception if limit exceeded"""
        key = key or self.key_func()
        self.metrics.start_timing(key)
        
        try:
            count = await self.storage.increment(key, max(window for _, window in self.quota_limits))
            self.metrics.update_usage(key, count, max(quota for quota, _ in self.quota_limits))
            self.logger.log_request(key, count, max(quota for quota, _ in self.quota_limits))
            
            if any(count > quota for quota, _ in self.quota_limits):
                retry_after = max(window for _, window in self.quota_limits)
                self.metrics.track_exceeded(key)
                self.events.emit(
                    RateLimitEvent.LIMIT_EXCEEDED,
                    key=key,
                    retry_after=retry_after
                )
                self.logger.log_exceeded(key, retry_after)
                raise RateLimitExceeded(retry_after=retry_after)
                
        finally:
            self.metrics.stop_timing(key)
    
    async def reset_quota(self, key: Optional[str] = None) -> None:
        """Reset quota limit counter"""
        key = key or self.key_func()
        await self.storage.reset(key)
        self.metrics.update_usage(key, 0, max(quota for quota, _ in self.quota_limits))
        self.events.emit(RateLimitEvent.RESET, key=key)
