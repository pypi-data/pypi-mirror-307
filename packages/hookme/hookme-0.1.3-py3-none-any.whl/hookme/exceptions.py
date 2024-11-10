from typing import Optional

class WebhookError(Exception):
    """Base exception for webhook-related errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_text: Optional[str] = None):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(message)

class WebhookTimeoutError(WebhookError):
    """Raised when webhook request times out."""
    pass

class WebhookRateLimitError(WebhookError):
    """Raised when hitting Discord's rate limits."""
    def __init__(self, message: str, retry_after: float):
        self.retry_after = retry_after
        super().__init__(message)

class WebhookConnectionError(WebhookError):
    """Raised when connection to Discord fails."""
    pass

class WebhookValidationError(WebhookError):
    """Raised when payload validation fails."""
    pass 