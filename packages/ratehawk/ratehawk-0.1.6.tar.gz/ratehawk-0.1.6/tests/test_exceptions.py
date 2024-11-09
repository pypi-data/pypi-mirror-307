## tested complete 

import pytest
from ratehawk.exceptions import RateLimitExceeded, StorageError

def test_rate_limit_exceeded_basic():
    """Test basic RateLimitExceeded exception creation and attributes"""
    with pytest.raises(RateLimitExceeded) as exc_info:
        raise RateLimitExceeded("Rate limit exceeded", retry_after=10)
    assert str(exc_info.value) == "Rate limit exceeded"
    assert exc_info.value.retry_after == 10

def test_rate_limit_exceeded_custom_message():
    """Test RateLimitExceeded with custom message"""
    custom_msg = "Custom rate limit message"
    with pytest.raises(RateLimitExceeded) as exc_info:
        raise RateLimitExceeded(custom_msg, retry_after=30)
    assert str(exc_info.value) == custom_msg
    assert exc_info.value.retry_after == 30

def test_rate_limit_exceeded_no_retry():
    """Test RateLimitExceeded without retry_after"""
    with pytest.raises(RateLimitExceeded) as exc_info:
        raise RateLimitExceeded()
    assert str(exc_info.value) == "Rate limit exceeded"
    assert exc_info.value.retry_after is None

def test_storage_error_basic():
    """Test basic StorageError exception"""
    with pytest.raises(StorageError) as exc_info:
        raise StorageError("Storage backend error")
    assert str(exc_info.value) == "Storage backend error"

def test_storage_error_custom_message():
    """Test StorageError with custom message"""
    custom_msg = "Custom storage error"
    with pytest.raises(StorageError) as exc_info:
        raise StorageError(custom_msg)
    assert str(exc_info.value) == custom_msg

def test_storage_error_with_cause():
    """Test StorageError with underlying cause"""
    try:
        raise ValueError("Original error")
    except ValueError as e:
        with pytest.raises(StorageError) as exc_info:
            raise StorageError("Storage failed") from e
    assert str(exc_info.value) == "Storage failed"
    assert isinstance(exc_info.value.__cause__, ValueError)

def test_exceptions_inheritance():
    """Test exception inheritance"""
    exc = RateLimitExceeded("Test")
    assert isinstance(exc, Exception)
    
    exc = StorageError("Test")
    assert isinstance(exc, Exception)
