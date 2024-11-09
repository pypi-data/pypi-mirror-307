import pytest
from ratehawk.limiter import RateLimiter
from ratehawk.storage.memory import MemoryStorage
from ratehawk.exceptions import RateLimitExceeded

@pytest.fixture
def rate_limiter():
    limits = [(10, 60)]
    return RateLimiter(limits=limits, storage=MemoryStorage())

@pytest.mark.asyncio
async def test_check(rate_limiter):
    assert await rate_limiter.check() is True

@pytest.mark.asyncio
async def test_increment(rate_limiter):
    await rate_limiter.increment()
    assert await rate_limiter.check() is True

@pytest.mark.asyncio
async def test_reset(rate_limiter):
    await rate_limiter.increment()
    await rate_limiter.reset()
    assert await rate_limiter.check() is True

@pytest.mark.asyncio
async def test_apply_dynamic_limits(rate_limiter):
    async def dynamic_limits_func():
        return {"limits": [(5, 60)]}
    rate_limiter.dynamic_limits_func = dynamic_limits_func
    await rate_limiter.apply_dynamic_limits()
    assert rate_limiter.limits == [(5, 60)]

@pytest.mark.asyncio
async def test_check_quota(rate_limiter):
    rate_limiter.quota_limits = [(100, 86400)]
    assert await rate_limiter.check_quota() is True

@pytest.mark.asyncio
async def test_increment_quota(rate_limiter):
    rate_limiter.quota_limits = [(100, 86400)]
    await rate_limiter.increment_quota()
    assert await rate_limiter.check_quota() is True
