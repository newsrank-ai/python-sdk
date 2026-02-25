"""Stories resource — list, get, and track developments for news stories."""

from __future__ import annotations

from typing import Any, List, Optional, Union

from newsrank._client import AsyncClient, SyncClient
from newsrank._types import (
    RankedStoryList,
    Story,
    StoryDevelopment,
    StoryList,
    StoryUpdate,
)


class StoriesResource:
    """Synchronous stories API.

    Usage::

        stories = nr.stories.list(limit=5)
        ranked  = nr.stories.ranked(limit=10)
        story   = nr.stories.get(42)
        devs    = nr.stories.developments(42)
        updates = nr.stories.updates(42, since_ms=1700000000000)
    """

    def __init__(self, client: SyncClient) -> None:
        self._client = client

    def list(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        category: Optional[str] = None,
    ) -> StoryList:
        """List stories with optional filtering and pagination.

        Args:
            limit: Maximum number of stories to return.
            offset: Number of stories to skip.
            category: Filter by category slug.
        """
        return self._client.get(
            "/stories",
            params={"limit": limit, "offset": offset, "category": category},
        )

    def ranked(self, *, limit: Optional[int] = None) -> RankedStoryList:
        """List stories ranked by importance.

        Args:
            limit: Maximum number of ranked stories to return.
        """
        return self._client.get(
            "/stories/ranked",
            params={"limit": limit},
        )

    def get(self, id: Union[int, str]) -> Story:
        """Get a single story by numeric ID or slug.

        Args:
            id: The story ID (integer) or slug (string).
        """
        return self._client.get(f"/stories/{id}")

    def developments(self, id: Union[int, str]) -> List[StoryDevelopment]:
        """List the timeline developments for a story.

        Args:
            id: The story ID (integer) or slug (string).
        """
        return self._client.get(f"/stories/{id}/developments")

    def updates(
        self,
        id: Union[int, str],
        *,
        since_ms: int,
    ) -> StoryUpdate:
        """Get updates to a story since a given timestamp.

        Args:
            id: The story ID (integer) or slug (string).
            since_ms: Unix timestamp in milliseconds.  Only updates after this
                point are returned.
        """
        return self._client.get(
            f"/stories/{id}/updates",
            params={"since_ms": since_ms},
        )


class AsyncStoriesResource:
    """Asynchronous stories API."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        category: Optional[str] = None,
    ) -> StoryList:
        """List stories with optional filtering and pagination."""
        return await self._client.get(
            "/stories",
            params={"limit": limit, "offset": offset, "category": category},
        )

    async def ranked(self, *, limit: Optional[int] = None) -> RankedStoryList:
        """List stories ranked by importance."""
        return await self._client.get(
            "/stories/ranked",
            params={"limit": limit},
        )

    async def get(self, id: Union[int, str]) -> Story:
        """Get a single story by numeric ID or slug."""
        return await self._client.get(f"/stories/{id}")

    async def developments(self, id: Union[int, str]) -> List[StoryDevelopment]:
        """List the timeline developments for a story."""
        return await self._client.get(f"/stories/{id}/developments")

    async def updates(
        self,
        id: Union[int, str],
        *,
        since_ms: int,
    ) -> StoryUpdate:
        """Get updates to a story since a given timestamp."""
        return await self._client.get(
            f"/stories/{id}/updates",
            params={"since_ms": since_ms},
        )
