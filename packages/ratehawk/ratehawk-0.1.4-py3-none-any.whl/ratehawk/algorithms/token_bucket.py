from dataclasses import dataclass
from time import time
from typing import Optional, Tuple

@dataclass
class TokenBucket:
    capacity: float  # Maximum number of tokens the bucket can hold
    fill_rate: float  # Number of tokens added per second
    current_tokens: float = 0.0
    last_update: float = 0.0

    def __post_init__(self):
        if self.last_update == 0.0:
            self.last_update = time()
            self.current_tokens = self.capacity

    def try_consume(self, tokens: float = 1.0) -> Tuple[bool, float]:
        """
        Attempt to consume tokens from the bucket.
        Returns (success, wait_time_if_failed)
        """
        now = time()
        # Add new tokens based on time elapsed
        time_passed = now - self.last_update
        new_tokens = time_passed * self.fill_rate
        self.current_tokens = min(self.capacity, self.current_tokens + new_tokens)
        self.last_update = now

        if self.current_tokens >= tokens:
            self.current_tokens -= tokens
            return True, 0.0
        else:
            # Calculate wait time until enough tokens are available
            additional_tokens_needed = tokens - self.current_tokens
            wait_time = additional_tokens_needed / self.fill_rate
            return False, wait_time 