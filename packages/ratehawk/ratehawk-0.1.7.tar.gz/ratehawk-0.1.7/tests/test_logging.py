## tested complete 

import pytest
import logging
from ratehawk.monitoring.logging import RateLimitLogger

@pytest.fixture
def rate_limit_logger():
    return RateLimitLogger()

def test_log_request(rate_limit_logger, caplog):
    key = "test_key"
    current = 5
    limit = 10
    with caplog.at_level(logging.INFO):
        rate_limit_logger.log_request(key, current, limit)
    assert "Rate limit request - Key: test_key, Current: 5, Limit: 10" in caplog.text

def test_log_exceeded(rate_limit_logger, caplog):
    key = "test_key"
    retry_after = 60
    with caplog.at_level(logging.WARNING):
        rate_limit_logger.log_exceeded(key, retry_after)
    assert "Rate limit exceeded - Key: test_key, Retry After: 60s" in caplog.text

def test_log_near_limit(rate_limit_logger, caplog):
    key = "test_key"
    current = 8
    limit = 10
    with caplog.at_level(logging.WARNING):
        rate_limit_logger.log_near_limit(key, current, limit)
    assert "Near rate limit - Key: test_key, Usage: 80.0%" in caplog.text
