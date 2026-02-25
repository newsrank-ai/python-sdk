"""Sources resource — news sources, categories, tags, and rankings."""

from __future__ import annotations

from typing import Any, List

from newsrank._client import AsyncClient, SyncClient
from newsrank._types import Category, Source, SourceRanking, Tag


class SourcesResource:
    """Synchronous sources API.

    Usage::

        sources    = nr.sources.list()
        categories = nr.sources.categories()
        tags       = nr.sources.tags()
        rankings   = nr.sources.rankings()
    """

    def __init__(self, client: SyncClient) -> None:
        self._client = client

    def list(self) -> List[Source]:
        """List all news sources."""
        return self._client.get("/sources")

    def categories(self) -> List[Category]:
        """List all news categories."""
        return self._client.get("/categories")

    def tags(self) -> List[Tag]:
        """List all content tags."""
        return self._client.get("/tags")

    def rankings(self) -> List[SourceRanking]:
        """List source rankings."""
        return self._client.get("/source-rankings")


class AsyncSourcesResource:
    """Asynchronous sources API."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(self) -> List[Source]:
        """List all news sources."""
        return await self._client.get("/sources")

    async def categories(self) -> List[Category]:
        """List all news categories."""
        return await self._client.get("/categories")

    async def tags(self) -> List[Tag]:
        """List all content tags."""
        return await self._client.get("/tags")

    async def rankings(self) -> List[SourceRanking]:
        """List source rankings."""
        return await self._client.get("/source-rankings")
