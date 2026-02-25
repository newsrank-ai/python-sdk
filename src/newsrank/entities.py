"""Entities resource — named entities, trending, politicians, and related articles."""

from __future__ import annotations

from typing import Optional, Union

from newsrank._client import AsyncClient, SyncClient
from newsrank._types import (
    ArticleList,
    Entity,
    EntityList,
    PoliticianList,
    TrendingEntityList,
)


class EntitiesResource:
    """Synchronous entities API.

    Usage::

        entities   = nr.entities.list(type="person", limit=20)
        trending   = nr.entities.trending(limit=10)
        pols       = nr.entities.politicians(limit=50)
        entity     = nr.entities.get(42)
        articles   = nr.entities.articles(42, limit=10)
    """

    def __init__(self, client: SyncClient) -> None:
        self._client = client

    def list(
        self,
        *,
        q: Optional[str] = None,
        type: Optional[str] = None,
        subcategory: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> EntityList:
        """List entities with optional filtering.

        Args:
            q: Search query to filter entities by name.
            type: Entity type (e.g. ``person``, ``organization``, ``location``).
            subcategory: Entity subcategory filter.
            limit: Maximum number of entities to return.
            offset: Number of entities to skip.
        """
        return self._client.get(
            "/entities",
            params={
                "q": q,
                "type": type,
                "subcategory": subcategory,
                "limit": limit,
                "offset": offset,
            },
        )

    def trending(self, *, limit: Optional[int] = None) -> TrendingEntityList:
        """List currently trending entities.

        Args:
            limit: Maximum number of entities to return.
        """
        return self._client.get(
            "/entities/trending",
            params={"limit": limit},
        )

    def politicians(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PoliticianList:
        """List politician entities.

        Args:
            limit: Maximum number of politicians to return.
            offset: Number of politicians to skip.
        """
        return self._client.get(
            "/entities/politicians",
            params={"limit": limit, "offset": offset},
        )

    def get(self, id: Union[int, str]) -> Entity:
        """Get a single entity by numeric ID or slug.

        Args:
            id: The entity ID (integer) or slug (string).
        """
        return self._client.get(f"/entities/{id}")

    def articles(
        self,
        id: Union[int, str],
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> ArticleList:
        """List articles associated with an entity.

        Args:
            id: The entity ID (integer) or slug (string).
            limit: Maximum number of articles to return.
            offset: Number of articles to skip.
        """
        return self._client.get(
            f"/entities/{id}/articles",
            params={"limit": limit, "offset": offset},
        )


class AsyncEntitiesResource:
    """Asynchronous entities API."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        q: Optional[str] = None,
        type: Optional[str] = None,
        subcategory: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> EntityList:
        """List entities with optional filtering."""
        return await self._client.get(
            "/entities",
            params={
                "q": q,
                "type": type,
                "subcategory": subcategory,
                "limit": limit,
                "offset": offset,
            },
        )

    async def trending(self, *, limit: Optional[int] = None) -> TrendingEntityList:
        """List currently trending entities."""
        return await self._client.get(
            "/entities/trending",
            params={"limit": limit},
        )

    async def politicians(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> PoliticianList:
        """List politician entities."""
        return await self._client.get(
            "/entities/politicians",
            params={"limit": limit, "offset": offset},
        )

    async def get(self, id: Union[int, str]) -> Entity:
        """Get a single entity by numeric ID or slug."""
        return await self._client.get(f"/entities/{id}")

    async def articles(
        self,
        id: Union[int, str],
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> ArticleList:
        """List articles associated with an entity."""
        return await self._client.get(
            f"/entities/{id}/articles",
            params={"limit": limit, "offset": offset},
        )
