from typing import Callable, Dict, List, Optional
from enum import Enum

class RateLimitEvent(Enum):
    LIMIT_EXCEEDED = "limit_exceeded"
    NEAR_LIMIT = "near_limit"
    RESET = "reset"

class EventEmitter:
    def __init__(self):
        self.handlers: Dict[RateLimitEvent, List[Callable]] = {
            event: [] for event in RateLimitEvent
        }
        
    def on(self, event: RateLimitEvent, handler: Callable):
        """Register an event handler"""
        self.handlers[event].append(handler)
        
    def emit(self, event: RateLimitEvent, **kwargs):
        """Emit an event to all registered handlers"""
        for handler in self.handlers[event]:
            handler(**kwargs) 