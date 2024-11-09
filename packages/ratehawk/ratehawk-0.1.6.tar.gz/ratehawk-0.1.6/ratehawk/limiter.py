from typing import List, Tuple, Dict, Any, Optional
from time import time
import asyncio
from .algorithms.token_bucket import TokenBucket
from .exceptions import RateLimitExceeded

class RateLimiter:
    def __init__(
        self,
        limits: List[Tuple[int, int]],
        algorithm: str = "window",
        bucket_capacity: float = None,
        fill_rate: float = None
    ):
        """
        Initialize rate limiter with specified limits and algorithm
        
        Args:
            limits: List of (max_requests, period_seconds) tuples
            algorithm: "window" or "token_bucket"
            bucket_capacity: Maximum token capacity for token bucket algorithm
            fill_rate: Token fill rate per second for token bucket algorithm
        """
        self.limits = limits
        self.algorithm = algorithm
        self._counters: Dict[str, Dict[int, int]] = {}
        self._last_reset: Dict[str, float] = {}
        
        if algorithm == "token_bucket":
            if bucket_capacity is None or fill_rate is None:
                raise ValueError("bucket_capacity and fill_rate required for token bucket algorithm")
            self._bucket = TokenBucket(
                capacity=float(bucket_capacity),
                fill_rate=float(fill_rate)
            )
        elif algorithm != "window":
            raise ValueError("Unsupported algorithm. Use 'window' or 'token_bucket'")

    async def check(self, key: str = "default") -> bool:
        """Check if request is allowed without incrementing counters"""
        if self.algorithm == "window":
            return await self._check_window(key)
        else:
            allowed, _ = await self.is_allowed(key)
            return allowed

    async def increment(self, key: str = "default") -> None:
        """Increment request counter for the given key"""
        if self.algorithm == "window":
            now = time()
            if key not in self._counters:
                self._counters[key] = {period: 0 for _, period in self.limits}
                self._last_reset[key] = now

            # Reset counters if period has elapsed
            if now - self._last_reset.get(key, 0) >= min(period for _, period in self.limits):
                self._counters[key] = {period: 0 for _, period in self.limits}
                self._last_reset[key] = now

            # Increment all counters
            for _, period in self.limits:
                self._counters[key][period] += 1

    async def _check_window(self, key: str = "default") -> bool:
        """Check if request is allowed using sliding window algorithm"""
        now = time()
        if key not in self._counters:
            return True

        # Check all limits
        for limit, period in self.limits:
            count = self._counters.get(key, {}).get(period, 0)
            if count >= limit and now - self._last_reset.get(key, 0) < period:
                return False
        return True

    async def is_allowed(self, key: str = "default") -> Tuple[bool, Dict[str, float]]:
        """
        Check if request is allowed and return detailed information
        
        Returns:
            Tuple[bool, Dict]: (allowed, info)
            info contains:
                - remaining: remaining tokens/requests
                - reset_after: seconds until reset
        """
        if self.algorithm == "token_bucket":
            success, wait_time = self._bucket.try_consume()
            remaining = self._bucket.get_tokens()
            
            return success, {
                "remaining": remaining,
                "reset_after": wait_time
            }
        else:
            # Window algorithm
            allowed = await self._check_window(key)
            if not allowed:
                # Calculate time until reset
                reset_after = min(
                    period - (time() - self._last_reset.get(key, 0))
                    for _, period in self.limits
                )
            else:
                reset_after = 0

            count = self._counters.get(key, {}).get(self.limits[0][1], 0)
            remaining = max(0, self.limits[0][0] - count)

            return allowed, {
                "remaining": remaining,
                "reset_after": max(0, reset_after)
            }
