import time
from typing import Optional, Callable, Dict, List, Tuple, Union
from .storage.base import BaseStorage
from .storage.memory import MemoryStorage
from .exceptions import RateLimitExceeded
from .monitoring.metrics import RateLimitMetrics
from .monitoring.events import EventEmitter, RateLimitEvent
from .monitoring.logging import RateLimitLogger
from .algorithms.token_bucket import TokenBucket
from .algorithms.leaky_bucket import LeakyBucket

class RateLimiter:
    def __init__(
        self,
        limits: List[Tuple[int, int]],
        burst_limits: Optional[List[Tuple[int, int]]] = None,
        storage: Optional[BaseStorage] = None,
        key_func: Optional[Callable] = None,
        near_limit_threshold: float = 0.8,
        dynamic_limits_func: Optional[Callable] = None,
        quota_limits: Optional[List[Tuple[int, int]]] = None,
        algorithm: str = "window",
        window_size: int = 60,
        max_requests: int = 100,
        bucket_capacity: float = None,
        fill_rate: float = None,
        leak_rate: float = None,
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
            algorithm: Rate limiting algorithm (defaults to "window")
            window_size: Size of the rate limiting window (defaults to 60 seconds)
            max_requests: Maximum number of requests allowed within the window (defaults to 100)
            bucket_capacity: Capacity of the token bucket (defaults to max_requests)
            fill_rate: Fill rate of the token bucket (defaults to max_requests / window_size)
            leak_rate: Leak rate of the leaky bucket (defaults to max_requests / window_size)
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
        
        self.algorithm = algorithm
        self.window_size = window_size
        self.max_requests = max_requests
        
        # Token bucket specific parameters
        self.bucket_capacity = bucket_capacity or max_requests
        self.fill_rate = fill_rate or (max_requests / window_size)
        
        # Leaky bucket specific parameters
        self.leak_rate = leak_rate or (max_requests / window_size)
        
        if algorithm not in ["window", "token_bucket", "leaky_bucket"]:
            raise ValueError("Unsupported algorithm. Use 'window', 'token_bucket', or 'leaky_bucket'")
    
    async def check(self, key: Optional[str] = None) -> bool:
        """Check if rate limit is exceeded without incrementing"""
        key = key or self.key_func()
        self.metrics.start_timing(key)
        
        try:
            count = await self.storage.get(key)
            count = 0 if count is None else count
            
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
            count = 1 if count is None else count
            
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
            dynamic_limits = await self.dynamic_limits_func()
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
    
    async def is_allowed(self, key: str) -> Tuple[bool, Dict]:
        if self.algorithm == "window":
            return await self._check_window(key)
        elif self.algorithm == "token_bucket":
            return await self._check_token_bucket(key)
        else:
            return await self._check_leaky_bucket(key)
    
    async def _check_token_bucket(self, key: str) -> Tuple[bool, Dict]:
        bucket_key = f"bucket:{key}"
        stored_bucket = await self.storage.get(bucket_key)
        
        if stored_bucket is None:
            bucket = TokenBucket(
                capacity=self.bucket_capacity,
                fill_rate=self.fill_rate
            )
        else:
            try:
                # Handle both dictionary and raw data cases
                if isinstance(stored_bucket, dict):
                    bucket = TokenBucket.from_dict(stored_bucket)
                else:
                    # Create new bucket if stored data is invalid
                    bucket = TokenBucket(
                        capacity=self.bucket_capacity,
                        fill_rate=self.fill_rate
                    )
            except (ValueError, TypeError):
                # Fallback to new bucket if conversion fails
                bucket = TokenBucket(
                    capacity=self.bucket_capacity,
                    fill_rate=self.fill_rate
                )
        
        allowed, wait_time = bucket.try_consume()
        
        # Store updated bucket state
        await self.storage.set(
            bucket_key,
            bucket.to_dict(),
            expire=int(self.window_size * 2)
        )
        
        return allowed, {
            "remaining": bucket.current_tokens,
            "reset_after": wait_time,
            "limit": bucket.capacity
        }
    
    async def _check_leaky_bucket(self, key: str) -> Tuple[bool, Dict]:
        """Check if request is allowed using leaky bucket algorithm"""
        bucket_key = f"leaky:{key}"
        stored_bucket = await self.storage.get(bucket_key)
        
        if stored_bucket is None:
            bucket = LeakyBucket(
                capacity=self.bucket_capacity,
                leak_rate=self.leak_rate
            )
        else:
            try:
                if isinstance(stored_bucket, dict):
                    bucket = LeakyBucket.from_dict(stored_bucket)
                else:
                    bucket = LeakyBucket(
                        capacity=self.bucket_capacity,
                        leak_rate=self.leak_rate
                    )
            except (ValueError, TypeError):
                bucket = LeakyBucket(
                    capacity=self.bucket_capacity,
                    leak_rate=self.leak_rate
                )
        
        allowed, wait_time = bucket.try_add()
        
        # Store updated bucket state
        await self.storage.set(
            bucket_key,
            bucket.to_dict(),
            expire=int(self.window_size * 2)
        )
        
        return allowed, {
            "remaining": self.bucket_capacity - bucket.get_current_size(),
            "reset_after": wait_time,
            "limit": self.bucket_capacity
        }
