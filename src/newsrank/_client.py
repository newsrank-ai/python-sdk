"""Low-level HTTP transport for the NewsRank API.

This module provides ``SyncClient`` and ``AsyncClient`` wrappers around
``httpx`` that handle authentication, base URL resolution, and error mapping.
Resource classes (articles, stories, etc.) delegate all HTTP work here.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Type, Union

import httpx

from newsrank._exceptions import (
    AuthenticationError,
    NewsRankError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ServerError,
)

DEFAULT_BASE_URL = "https://newsrank.ai/api/v1"
DEFAULT_TIMEOUT = 30.0
USER_AGENT = "newsrank-python/0.1.0"

_STATUS_MAP: Dict[int, Type[NewsRankError]] = {
    401: AuthenticationError,
    403: PermissionError,
    404: NotFoundError,
    429: RateLimitError,
}


def _build_error(response: httpx.Response) -> NewsRankError:
    """Create the appropriate exception for a failed HTTP response."""
    status = response.status_code

    # Try to extract a JSON error message from the body.
    body: Any = None
    message = f"API request failed with status {status}"
    try:
        body = response.json()
        if isinstance(body, dict):
            message = body.get("error", body.get("message", message))
    except Exception:
        body = response.text

    exc_cls = _STATUS_MAP.get(status)
    if exc_cls is not None:
        return exc_cls(message, status_code=status, body=body)
    if 500 <= status < 600:
        return ServerError(message, status_code=status, body=body)
    return NewsRankError(message, status_code=status, body=body)


def _clean_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Remove ``None`` values so they are not sent as query parameters."""
    return {k: v for k, v in params.items() if v is not None}


# ---------------------------------------------------------------------------
# Synchronous client
# ---------------------------------------------------------------------------


class SyncClient:
    """Synchronous HTTP client for the NewsRank API.

    Parameters:
        api_key: Your NewsRank API key (``nrf_...``).
        base_url: Override the default API base URL.
        timeout: Request timeout in seconds.
        httpx_client: An existing ``httpx.Client`` to use.  When provided the
            caller is responsible for closing it.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        httpx_client: Optional[httpx.Client] = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._owns_client = httpx_client is None
        self._client = httpx_client or httpx.Client(
            timeout=timeout,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )

    # -- public helpers -----------------------------------------------------

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        auth: bool = True,
    ) -> Any:
        """Send an HTTP request and return the parsed JSON body.

        Raises a :class:`NewsRankError` subclass on non-2xx responses.
        """
        url = f"{self._base_url}{path}"
        headers: Dict[str, str] = {}
        if auth:
            headers["Authorization"] = f"Bearer {self._api_key}"

        response = self._client.request(
            method,
            url,
            params=_clean_params(params or {}),
            headers=headers,
        )

        if not response.is_success:
            raise _build_error(response)

        # Some endpoints may return 204 No Content.
        if response.status_code == 204 or not response.content:
            return None

        return response.json()

    def get(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        auth: bool = True,
    ) -> Any:
        """Convenience wrapper for ``GET`` requests."""
        return self.request("GET", path, params=params, auth=auth)

    # -- lifecycle ----------------------------------------------------------

    def close(self) -> None:
        """Close the underlying ``httpx.Client`` if we own it."""
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "SyncClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()


# ---------------------------------------------------------------------------
# Asynchronous client
# ---------------------------------------------------------------------------


class AsyncClient:
    """Asynchronous HTTP client for the NewsRank API.

    Parameters:
        api_key: Your NewsRank API key (``nrf_...``).
        base_url: Override the default API base URL.
        timeout: Request timeout in seconds.
        httpx_client: An existing ``httpx.AsyncClient`` to use.  When provided
            the caller is responsible for closing it.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        httpx_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._owns_client = httpx_client is None
        self._client = httpx_client or httpx.AsyncClient(
            timeout=timeout,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )

    # -- public helpers -----------------------------------------------------

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        auth: bool = True,
    ) -> Any:
        """Send an HTTP request and return the parsed JSON body."""
        url = f"{self._base_url}{path}"
        headers: Dict[str, str] = {}
        if auth:
            headers["Authorization"] = f"Bearer {self._api_key}"

        response = await self._client.request(
            method,
            url,
            params=_clean_params(params or {}),
            headers=headers,
        )

        if not response.is_success:
            raise _build_error(response)

        if response.status_code == 204 or not response.content:
            return None

        return response.json()

    async def get(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        auth: bool = True,
    ) -> Any:
        """Convenience wrapper for ``GET`` requests."""
        return await self.request("GET", path, params=params, auth=auth)

    # -- lifecycle ----------------------------------------------------------

    async def close(self) -> None:
        """Close the underlying ``httpx.AsyncClient`` if we own it."""
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()
