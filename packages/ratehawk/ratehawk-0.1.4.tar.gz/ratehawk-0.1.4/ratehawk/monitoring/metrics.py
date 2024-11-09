from prometheus_client import Counter, Gauge, Histogram
from typing import Dict, Optional
from datetime import datetime

# Prometheus metrics
REQUESTS_TOTAL = Counter(
    'ratehawk_requests_total',
    'Total number of requests processed',
    ['key', 'status']
)

CURRENT_USAGE = Gauge(
    'ratehawk_current_usage',
    'Current rate limit usage',
    ['key']
)

LIMIT_EXCEEDED = Counter(
    'ratehawk_limit_exceeded_total',
    'Number of times rate limit was exceeded',
    ['key']
)

RESPONSE_TIME = Histogram(
    'ratehawk_response_time_seconds',
    'Time spent processing rate limit checks',
    ['key']
)

class RateLimitMetrics:
    def __init__(self):
        self.start_time: Dict[str, float] = {}
        
    def track_request(self, key: str, success: bool):
        status = 'success' if success else 'exceeded'
        REQUESTS_TOTAL.labels(key=key, status=status).inc()
        
    def update_usage(self, key: str, current: int, limit: int):
        usage_percentage = (current / limit) * 100
        CURRENT_USAGE.labels(key=key).set(usage_percentage)
        
    def track_exceeded(self, key: str):
        LIMIT_EXCEEDED.labels(key=key).inc()
        
    def start_timing(self, key: str):
        self.start_time[key] = datetime.now().timestamp()
        
    def stop_timing(self, key: str):
        if key in self.start_time:
            duration = datetime.now().timestamp() - self.start_time[key]
            RESPONSE_TIME.labels(key=key).observe(duration)
            del self.start_time[key] 