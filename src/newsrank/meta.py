"""Meta resource — related articles, stats, version, and usage."""

from __future__ import annotations

from typing import List, Optional

from newsrank._client import AsyncClient, SyncClient
from newsrank._types import RelatedArticle, Stats, UsageRecord, VersionInfo


class MetaResource:
    """Synchronous meta/utility API.

    Usage::

        related = nr.meta.related(url_hash="abc123", limit=5)
        stats   = nr.meta.stats()
        version = nr.meta.version()
        usage   = nr.meta.usage()
    """

    def __init__(self, client: SyncClient) -> None:
        self._client = client

    def related(
        self,
        *,
        url_hash: str,
        limit: Optional[int] = None,
    ) -> List[RelatedArticle]:
        """Get articles related to a given article.

        Args:
            url_hash: The article's URL hash (required).
            limit: Maximum number of related articles.
        """
        return self._client.get(
            "/related",
            params={"url_hash": url_hash, "limit": limit},
        )

    def stats(self) -> Stats:
        """Get platform-wide statistics."""
        return self._client.get("/stats")

    def version(self) -> VersionInfo:
        """Get API version information.

        This endpoint does **not** require authentication.
        """
        return self._client.get("/version", auth=False)

    def usage(
        self,
        *,
        from_ms: Optional[int] = None,
        to_ms: Optional[int] = None,
    ) -> UsageRecord:
        """Get your API usage statistics.

        Args:
            from_ms: Start of the period as a Unix timestamp in milliseconds.
            to_ms: End of the period as a Unix timestamp in milliseconds.
        """
        return self._client.get(
            "/usage",
            params={"from_ms": from_ms, "to_ms": to_ms},
        )


class AsyncMetaResource:
    """Asynchronous meta/utility API."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def related(
        self,
        *,
        url_hash: str,
        limit: Optional[int] = None,
    ) -> List[RelatedArticle]:
        """Get articles related to a given article."""
        return await self._client.get(
            "/related",
            params={"url_hash": url_hash, "limit": limit},
        )

    async def stats(self) -> Stats:
        """Get platform-wide statistics."""
        return await self._client.get("/stats")

    async def version(self) -> VersionInfo:
        """Get API version information (no auth required)."""
        return await self._client.get("/version", auth=False)

    async def usage(
        self,
        *,
        from_ms: Optional[int] = None,
        to_ms: Optional[int] = None,
    ) -> UsageRecord:
        """Get your API usage statistics."""
        return await self._client.get(
            "/usage",
            params={"from_ms": from_ms, "to_ms": to_ms},
        )
