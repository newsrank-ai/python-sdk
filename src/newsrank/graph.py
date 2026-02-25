"""Graph resource — entity networks, story-entity, and topic cluster graphs."""

from __future__ import annotations

from typing import Optional

from newsrank._client import AsyncClient, SyncClient
from newsrank._types import Graph


class GraphResource:
    """Synchronous graph API.

    Usage::

        network = nr.graph.entity_network(entity_id=42, depth=2)
        story_g = nr.graph.story_entity(story_id=7)
        topic_g = nr.graph.topic_cluster(topic_id=3)
    """

    def __init__(self, client: SyncClient) -> None:
        self._client = client

    def entity_network(
        self,
        *,
        entity_id: int,
        depth: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Graph:
        """Get the entity co-occurrence network graph.

        Args:
            entity_id: The root entity ID (required).
            depth: How many hops from the root entity to include.
            limit: Maximum number of connected entities.
        """
        return self._client.get(
            "/graph/entity-network",
            params={"entity_id": entity_id, "depth": depth, "limit": limit},
        )

    def story_entity(
        self,
        *,
        story_id: int,
        limit: Optional[int] = None,
    ) -> Graph:
        """Get the entity graph for a story.

        Args:
            story_id: The story ID (required).
            limit: Maximum number of entities.
        """
        return self._client.get(
            "/graph/story-entity",
            params={"story_id": story_id, "limit": limit},
        )

    def topic_cluster(
        self,
        *,
        topic_id: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Graph:
        """Get the topic cluster graph.

        Args:
            topic_id: A specific topic to center the graph on.
            limit: Maximum number of nodes.
        """
        return self._client.get(
            "/graph/topic-cluster",
            params={"topic_id": topic_id, "limit": limit},
        )


class AsyncGraphResource:
    """Asynchronous graph API."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def entity_network(
        self,
        *,
        entity_id: int,
        depth: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Graph:
        """Get the entity co-occurrence network graph."""
        return await self._client.get(
            "/graph/entity-network",
            params={"entity_id": entity_id, "depth": depth, "limit": limit},
        )

    async def story_entity(
        self,
        *,
        story_id: int,
        limit: Optional[int] = None,
    ) -> Graph:
        """Get the entity graph for a story."""
        return await self._client.get(
            "/graph/story-entity",
            params={"story_id": story_id, "limit": limit},
        )

    async def topic_cluster(
        self,
        *,
        topic_id: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Graph:
        """Get the topic cluster graph."""
        return await self._client.get(
            "/graph/topic-cluster",
            params={"topic_id": topic_id, "limit": limit},
        )
