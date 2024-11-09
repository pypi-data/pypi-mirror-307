from dataclasses import dataclass, asdict
from time import time
from typing import Optional, Tuple, Dict, Any
from queue import Queue
import threading

@dataclass
class LeakyBucket:
    capacity: float  # Maximum number of requests the bucket can hold
    leak_rate: float  # Number of requests processed per second
    current_size: float = 0.0
    last_leak: float = 0.0
    
    def __post_init__(self):
        if self.capacity <= 0:
            raise ValueError("Capacity must be positive")
        if self.leak_rate <= 0:
            raise ValueError("Leak rate must be positive")
            
        if self.last_leak == 0.0:
            self.last_leak = time()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LeakyBucket':
        """Create a LeakyBucket instance from a dictionary"""
        if not all(k in data for k in ['capacity', 'leak_rate']):
            raise ValueError("Missing required fields: capacity and leak_rate")
            
        return cls(
            capacity=float(data.get('capacity', 0.0)),
            leak_rate=float(data.get('leak_rate', 0.0)),
            current_size=float(data.get('current_size', 0.0)),
            last_leak=float(data.get('last_leak', 0.0))
        )

    def to_dict(self) -> Dict[str, float]:
        """Convert the bucket state to a dictionary"""
        return asdict(self)

    def try_add(self, request_size: float = 1.0) -> Tuple[bool, float]:
        """
        Attempt to add a request to the bucket
        
        Args:
            request_size: Size of the request to add (default: 1.0)
            
        Returns:
            Tuple[bool, float]: (success, wait_time)
                - success: True if request was added
                - wait_time: Time to wait if addition failed (0.0 if successful)
        """
        if request_size <= 0:
            raise ValueError("Request size must be positive")

        now = time()
        # Calculate leaked requests since last update
        time_passed = max(0, now - self.last_leak)
        leaked = time_passed * self.leak_rate
        
        # Update current bucket size
        self.current_size = max(0, self.current_size - leaked)
        self.last_leak = now

        # Check if request can be added
        if self.current_size + request_size <= self.capacity:
            self.current_size += request_size
            return True, 0.0
        else:
            # Calculate wait time until enough space is available
            space_needed = (self.current_size + request_size) - self.capacity
            wait_time = space_needed / self.leak_rate
            return False, max(0, wait_time)

    def get_current_size(self) -> float:
        """Get current size of the bucket without adding requests"""
        now = time()
        time_passed = max(0, now - self.last_leak)
        leaked = time_passed * self.leak_rate
        return max(0, self.current_size - leaked) 