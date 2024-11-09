import logging
from datetime import datetime
from typing import Optional

class RateLimitLogger:
    def __init__(self, logger_name: str = "ratehawk"):
        self.logger = logging.getLogger(logger_name)
        self._setup_logger()
        
    def _setup_logger(self):
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
    def log_request(self, key: str, current: int, limit: int):
        self.logger.info(
            f"Rate limit request - Key: {key}, Current: {current}, Limit: {limit}"
        )
        
    def log_exceeded(self, key: str, retry_after: Optional[int]):
        self.logger.warning(
            f"Rate limit exceeded - Key: {key}, Retry After: {retry_after}s"
        )
        
    def log_near_limit(self, key: str, current: int, limit: int):
        usage_percent = (current / limit) * 100
        self.logger.warning(
            f"Near rate limit - Key: {key}, Usage: {usage_percent:.1f}%"
        ) 