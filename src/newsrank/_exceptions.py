"""Custom exceptions for the NewsRank SDK."""

from __future__ import annotations

from typing import Any, Optional


class NewsRankError(Exception):
    """Base exception for all NewsRank API errors.

    Attributes:
        status_code: The HTTP status code returned by the API, or None for
            client-side errors (e.g. connection failures).
        message: A human-readable error message.
        body: The raw response body, if available.
    """

    status_code: Optional[int]
    message: str
    body: Optional[Any]

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        body: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.body = body

    def __repr__(self) -> str:
        return (
            f"NewsRankError(message={self.message!r}, "
            f"status_code={self.status_code!r})"
        )


class AuthenticationError(NewsRankError):
    """Raised when the API key is invalid or missing (HTTP 401)."""


class PermissionError(NewsRankError):
    """Raised when the API key lacks the required permissions (HTTP 403)."""


class NotFoundError(NewsRankError):
    """Raised when the requested resource does not exist (HTTP 404)."""


class RateLimitError(NewsRankError):
    """Raised when the rate limit has been exceeded (HTTP 429)."""


class ServerError(NewsRankError):
    """Raised when the API returns a server error (HTTP 5xx)."""
