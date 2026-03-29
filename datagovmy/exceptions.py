class DataGovMyError(Exception):
    """Base exception for all SDK errors."""


class APIError(DataGovMyError):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, status_code: int = 0, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class RateLimitError(APIError):
    """Raised when the API rate limit is exceeded (HTTP 429)."""

    def __init__(self, message: str = "Rate limit exceeded", response=None):
        super().__init__(message, status_code=429, response=response)


class NotFoundError(APIError):
    """Raised when the requested resource is not found (HTTP 404)."""

    def __init__(self, message: str = "Resource not found", response=None):
        super().__init__(message, status_code=404, response=response)


class AuthenticationError(APIError):
    """Raised when authentication fails (HTTP 401/403)."""

    def __init__(self, message: str = "Authentication failed", status_code: int = 401, response=None):
        super().__init__(message, status_code=status_code, response=response)
