"""Search resource — search articles, full-text search, and suggestions."""

from __future__ import annotations

from typing import Optional

from newsrank._client import AsyncClient, SyncClient
from newsrank._types import FullSearchResults, SearchResults, SearchSuggestions


class SearchResource:
    """Synchronous search API.

    Usage::

        results     = nr.search.articles(q="climate change", limit=10)
        full        = nr.search.full(q="election")
        suggestions = nr.search.suggest(q="clim")
    """

    def __init__(self, client: SyncClient) -> None:
        self._client = client

    def articles(
        self,
        *,
        q: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> SearchResults:
        """Search articles by keyword.

        Args:
            q: The search query (required).
            limit: Maximum number of results to return.
            offset: Number of results to skip.
        """
        return self._client.get(
            "/search",
            params={"q": q, "limit": limit, "offset": offset},
        )

    def full(
        self,
        *,
        q: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> FullSearchResults:
        """Full-text search across articles and stories.

        Args:
            q: The search query (required).
            limit: Maximum number of results to return.
            offset: Number of results to skip.
        """
        return self._client.get(
            "/search/full",
            params={"q": q, "limit": limit, "offset": offset},
        )

    def suggest(
        self,
        *,
        q: str,
        limit: Optional[int] = None,
    ) -> SearchSuggestions:
        """Get search suggestions / autocomplete.

        Args:
            q: The partial search query (required).
            limit: Maximum number of suggestions to return.
        """
        return self._client.get(
            "/search/suggest",
            params={"q": q, "limit": limit},
        )


class AsyncSearchResource:
    """Asynchronous search API."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def articles(
        self,
        *,
        q: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> SearchResults:
        """Search articles by keyword."""
        return await self._client.get(
            "/search",
            params={"q": q, "limit": limit, "offset": offset},
        )

    async def full(
        self,
        *,
        q: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> FullSearchResults:
        """Full-text search across articles and stories."""
        return await self._client.get(
            "/search/full",
            params={"q": q, "limit": limit, "offset": offset},
        )

    async def suggest(
        self,
        *,
        q: str,
        limit: Optional[int] = None,
    ) -> SearchSuggestions:
        """Get search suggestions / autocomplete."""
        return await self._client.get(
            "/search/suggest",
            params={"q": q, "limit": limit},
        )
