# Ratehawk

Ratehawk is a flexible API rate limiting library for Python. It allows you to easily implement rate limiting in your applications to prevent abuse and ensure fair usage of your APIs.

## Installation

You can install Ratehawk using pip:

```sh
pip install ratehawk
```

## Usage

Here are some examples of how to use Ratehawk in your Python applications:

### Basic Usage

```python
from ratehawk import RateLimiter

# Create a rate limiter with a limit of 10 requests per minute
rate_limiter = RateLimiter(limits=[(10, 60)])

# Check if the rate limit is exceeded
if await rate_limiter.check():
    print("Rate limit not exceeded")
else:
    print("Rate limit exceeded")

# Increment the rate limit counter
try:
    await rate_limiter.increment()
    print("Request allowed")
except RateLimitExceeded:
    print("Rate limit exceeded, try again later")
```

### Using Redis Storage

```python
from ratehawk import RateLimiter
from ratehawk.storage.redis import RedisStorage
from redis import Redis

# Create a Redis client
redis_client = Redis(host='localhost', port=6379, db=0)

# Create a rate limiter with Redis storage
rate_limiter = RateLimiter(limits=[(10, 60)], storage=RedisStorage(redis_client))

# Check if the rate limit is exceeded
if await rate_limiter.check():
    print("Rate limit not exceeded")
else:
    print("Rate limit exceeded")

# Increment the rate limit counter
try:
    await rate_limiter.increment()
    print("Request allowed")
except RateLimitExceeded:
    print("Rate limit exceeded, try again later")
```

### Using Postgres Storage

```python
from ratehawk import RateLimiter
from ratehawk.storage.postgres import PostgresStorage

# Create a rate limiter with Postgres storage
rate_limiter = RateLimiter(limits=[(10, 60)], storage=PostgresStorage(dsn="postgresql://localhost/ratehawk"))

# Check if the rate limit is exceeded
if await rate_limiter.check():
    print("Rate limit not exceeded")
else:
    print("Rate limit exceeded")

# Increment the rate limit counter
try:
    await rate_limiter.increment()
    print("Request allowed")
except RateLimitExceeded:
    print("Rate limit exceeded, try again later")
```

### Using SQLite Storage

```python
from ratehawk import RateLimiter
from ratehawk.storage.sqlite import SQLiteStorage

# Create a rate limiter with SQLite storage
rate_limiter = RateLimiter(limits=[(10, 60)], storage=SQLiteStorage(db_path="ratehawk.db"))

# Check if the rate limit is exceeded
if await rate_limiter.check():
    print("Rate limit not exceeded")
else:
    print("Rate limit exceeded")

# Increment the rate limit counter
try:
    await rate_limiter.increment()
    print("Request allowed")
except RateLimitExceeded:
    print("Rate limit exceeded, try again later")
```

### Using RateLimitMetrics

```python
from ratehawk import RateLimiter
from ratehawk.monitoring.metrics import RateLimitMetrics

# Create a rate limiter with metrics monitoring
rate_limiter = RateLimiter(limits=[(10, 60)])
rate_limiter.metrics = RateLimitMetrics()

# Check if the rate limit is exceeded
if await rate_limiter.check():
    print("Rate limit not exceeded")
else:
    print("Rate limit exceeded")

# Increment the rate limit counter
try:
    await rate_limiter.increment()
    print("Request allowed")
except RateLimitExceeded:
    print("Rate limit exceeded, try again later")
```

### Using RateLimitLogger

```python
from ratehawk import RateLimiter
from ratehawk.monitoring.logging import RateLimitLogger

# Create a rate limiter with logging
rate_limiter = RateLimiter(limits=[(10, 60)])
rate_limiter.logger = RateLimitLogger()

# Check if the rate limit is exceeded
if await rate_limiter.check():
    print("Rate limit not exceeded")
else:
    print("Rate limit exceeded")

# Increment the rate limit counter
try:
    await rate_limiter.increment()
    print("Request allowed")
except RateLimitExceeded:
    print("Rate limit exceeded, try again later")
```

### Using RateLimitEvent

```python
from ratehawk import RateLimiter
from ratehawk.monitoring.events import RateLimitEvent, EventEmitter

# Create a rate limiter with event monitoring
rate_limiter = RateLimiter(limits=[(10, 60)])
rate_limiter.events = EventEmitter()

# Register event handlers
def on_limit_exceeded(key, retry_after):
    print(f"Rate limit exceeded for key: {key}, retry after: {retry_after}s")

def on_near_limit(key, current, limit):
    print(f"Near rate limit for key: {key}, current: {current}, limit: {limit}")

def on_reset(key):
    print(f"Rate limit reset for key: {key}")

rate_limiter.events.on(RateLimitEvent.LIMIT_EXCEEDED, on_limit_exceeded)
rate_limiter.events.on(RateLimitEvent.NEAR_LIMIT, on_near_limit)
rate_limiter.events.on(RateLimitEvent.RESET, on_reset)

# Check if the rate limit is exceeded
if await rate_limiter.check():
    print("Rate limit not exceeded")
else:
    print("Rate limit exceeded")

# Increment the rate limit counter
try:
    await rate_limiter.increment()
    print("Request allowed")
except RateLimitExceeded:
    print("Rate limit exceeded, try again later")
```

### Using Multiple Rate Limits per Key

```python
from ratehawk import RateLimiter

# Create a rate limiter with multiple rate limits per key
rate_limiter = RateLimiter(limits=[(10, 60), (100, 3600)])

# Check if the rate limit is exceeded
if await rate_limiter.check():
    print("Rate limit not exceeded")
else:
    print("Rate limit exceeded")

# Increment the rate limit counter
try:
    await rate_limiter.increment()
    print("Request allowed")
except RateLimitExceeded:
    print("Rate limit exceeded, try again later")
```

### Using Rate Limit Groups and Hierarchies

```python
from ratehawk import RateLimiter

# Create a rate limiter with rate limit groups and hierarchies
rate_limiter = RateLimiter(
    limits=[(10, 60)],
    burst_limits=[(20, 15)],
    quota_limits=[(1000, 86400)]
)

# Check if the rate limit is exceeded
if await rate_limiter.check():
    print("Rate limit not exceeded")
else:
    print("Rate limit exceeded")

# Increment the rate limit counter
try:
    await rate_limiter.increment()
    print("Request allowed")
except RateLimitExceeded:
    print("Rate limit exceeded, try again later")
```

### Using Dynamic Rate Limits

```python
from ratehawk import RateLimiter

# Function to dynamically determine rate limits based on user attributes or time of day
def dynamic_limits_func():
    # Example: Different rate limits for different user roles
    user_role = get_user_role()
    if user_role == "premium":
        return {"limits": [(100, 60)], "burst_limits": [(200, 15)], "quota_limits": [(5000, 86400)]}
    else:
        return {"limits": [(10, 60)], "burst_limits": [(20, 15)], "quota_limits": [(1000, 86400)]}

# Create a rate limiter with dynamic rate limits
rate_limiter = RateLimiter(
    limits=[(10, 60)],
    dynamic_limits_func=dynamic_limits_func
)

# Apply dynamic rate limits
await rate_limiter.apply_dynamic_limits()

# Check if the rate limit is exceeded
if await rate_limiter.check():
    print("Rate limit not exceeded")
else:
    print("Rate limit exceeded")

# Increment the rate limit counter
try:
    await rate_limiter.increment()
    print("Request allowed")
except RateLimitExceeded:
    print("Rate limit exceeded, try again later")
```

### Using Rate Limit Quotas

```python
from ratehawk import RateLimiter

# Create a rate limiter with rate limit quotas over longer periods
rate_limiter = RateLimiter(
    limits=[(10, 60)],
    quota_limits=[(1000, 86400)]
)

# Check if the rate limit is exceeded
if await rate_limiter.check():
    print("Rate limit not exceeded")
else:
    print("Rate limit exceeded")

# Increment the rate limit counter
try:
    await rate_limiter.increment()
    print("Request allowed")
except RateLimitExceeded:
    print("Rate limit exceeded, try again later")

# Check if the quota limit is exceeded
if await rate_limiter.check_quota():
    print("Quota limit not exceeded")
else:
    print("Quota limit exceeded")

# Increment the quota limit counter
try:
    await rate_limiter.increment_quota()
    print("Request allowed")
except RateLimitExceeded:
    print("Quota limit exceeded, try again later")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
