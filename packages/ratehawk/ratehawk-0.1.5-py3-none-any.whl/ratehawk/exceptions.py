class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded"""
    def __init__(self, message="Rate limit exceeded", retry_after=None):
        self.retry_after = retry_after
        super().__init__(message)


class StorageError(Exception):
    """Raised when storage backend encounters an error"""
    pass 