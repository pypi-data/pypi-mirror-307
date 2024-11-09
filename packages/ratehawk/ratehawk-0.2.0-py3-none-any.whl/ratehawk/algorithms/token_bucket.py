from dataclasses import dataclass, asdict
from time import time
from typing import Optional, Tuple, Dict, Any

@dataclass
class TokenBucket:
    capacity: float  # Maximum number of tokens the bucket can hold
    fill_rate: float  # Number of tokens added per second
    current_tokens: float = 0.0
    last_update: float = 0.0

    def __post_init__(self):
        # Validate inputs
        if self.capacity <= 0:
            raise ValueError("Capacity must be positive")
        if self.fill_rate <= 0:
            raise ValueError("Fill rate must be positive")
            
        if self.last_update == 0.0:
            self.last_update = time()
            self.current_tokens = self.capacity

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TokenBucket':
        """Create a TokenBucket instance from a dictionary"""
        if not all(k in data for k in ['capacity', 'fill_rate']):
            raise ValueError("Missing required fields: capacity and fill_rate")
            
        return cls(
            capacity=float(data.get('capacity', 0.0)),
            fill_rate=float(data.get('fill_rate', 0.0)),
            current_tokens=float(data.get('current_tokens', 0.0)),
            last_update=float(data.get('last_update', 0.0))
        )

    def to_dict(self) -> Dict[str, float]:
        """Convert the bucket state to a dictionary"""
        return asdict(self)

    def try_consume(self, tokens: float = 1.0) -> Tuple[bool, float]:
        """
        Attempt to consume tokens from the bucket.
        Returns (success, wait_time_if_failed)
        
        Args:
            tokens (float): Number of tokens to consume
            
        Returns:
            Tuple[bool, float]: (success, wait_time)
                - success: True if tokens were consumed
                - wait_time: Time to wait if consumption failed (0.0 if successful)
        """
        if tokens <= 0:
            raise ValueError("Token consumption must be positive")
            
        now = time()
        # Add new tokens based on time elapsed
        time_passed = max(0, now - self.last_update)  # Ensure non-negative
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
            return False, max(0, wait_time)  # Ensure non-negative wait time

    def get_tokens(self) -> float:
        """Get current number of tokens without consuming any"""
        now = time()
        time_passed = max(0, now - self.last_update)
        new_tokens = time_passed * self.fill_rate
        return min(self.capacity, self.current_tokens + new_tokens)