class RecurveException(Exception):
    """Base class for all exceptions in Recurve."""


class APIError(RecurveException):
    """Raised when an API request fails."""

    def __init__(self, message: str = "API request failed."):
        super().__init__(message)


class UnauthorizedError(RecurveException):
    """Raised when an unauthorized request is made."""

    def __init__(self, message: str = "Unauthorized."):
        super().__init__(message)


class MaxRetriesExceededException(RecurveException):
    """Raised when the maximum number of retries is exceeded."""

    def __init__(self, message: str = "Max retries exceeded."):
        super().__init__(message)
