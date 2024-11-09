## tested complete 

import pytest
from ratehawk.monitoring.events import EventEmitter, RateLimitEvent

@pytest.fixture
def event_emitter():
    return EventEmitter()

@pytest.mark.asyncio
async def test_on(event_emitter):
    event_triggered = False

    def handler(**kwargs):
        nonlocal event_triggered
        event_triggered = True

    event_emitter.on(RateLimitEvent.LIMIT_EXCEEDED, handler)
    event_emitter.emit(RateLimitEvent.LIMIT_EXCEEDED)

    assert event_triggered

@pytest.mark.asyncio
async def test_emit(event_emitter):
    event_data = {}

    def handler(**kwargs):
        nonlocal event_data
        event_data = kwargs

    event_emitter.on(RateLimitEvent.NEAR_LIMIT, handler)
    event_emitter.emit(RateLimitEvent.NEAR_LIMIT, key="test_key", current=5, limit=10)

    assert event_data == {"key": "test_key", "current": 5, "limit": 10}
