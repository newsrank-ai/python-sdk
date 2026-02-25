"""NewsRank — Official Python client for the NewsRank API.

Quick start::

    from newsrank import NewsRank

    nr = NewsRank("nrf_your_api_key")

    # List top stories
    stories = nr.stories.ranked(limit=5)
    for s in stories["items"]:
        print(s["title"])

    # Search articles
    results = nr.search.articles(q="climate change")

For async usage::

    import asyncio
    from newsrank import AsyncNewsRank

    async def main():
        nr = AsyncNewsRank("nrf_your_api_key")
        stories = await nr.stories.ranked(limit=5)
        await nr.close()

    asyncio.run(main())
"""

from __future__ import annotations

from typing import Any, Optional

import httpx

from newsrank._client import AsyncClient, SyncClient
from newsrank._exceptions import (
    AuthenticationError,
    NewsRankError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ServerError,
)
from newsrank._types import (
    Article,
    ArticleContent,
    ArticleList,
    Category,
    Entity,
    EntityList,
    FullSearchResults,
    Graph,
    GraphEdge,
    GraphNode,
    PoliticianList,
    RankedStoryList,
    RelatedArticle,
    SearchResult,
    SearchResults,
    SearchSuggestion,
    SearchSuggestions,
    Source,
    SourceRanking,
    Stats,
    Story,
    StoryDevelopment,
    StoryList,
    StoryUpdate,
    Tag,
    TrendingEntityList,
    UsageRecord,
    VersionInfo,
)
from newsrank.articles import ArticlesResource, AsyncArticlesResource
from newsrank.entities import AsyncEntitiesResource, EntitiesResource
from newsrank.graph import AsyncGraphResource, GraphResource
from newsrank.meta import AsyncMetaResource, MetaResource
from newsrank.search import AsyncSearchResource, SearchResource
from newsrank.sources import AsyncSourcesResource, SourcesResource
from newsrank.stories import AsyncStoriesResource, StoriesResource

__version__ = "0.1.0"
__all__ = [
    # Main clients
    "NewsRank",
    "AsyncNewsRank",
    # Exceptions
    "NewsRankError",
    "AuthenticationError",
    "PermissionError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    # Response types
    "Article",
    "ArticleContent",
    "ArticleList",
    "Category",
    "Entity",
    "EntityList",
    "FullSearchResults",
    "Graph",
    "GraphEdge",
    "GraphNode",
    "PoliticianList",
    "RankedStoryList",
    "RelatedArticle",
    "SearchResult",
    "SearchResults",
    "SearchSuggestion",
    "SearchSuggestions",
    "Source",
    "SourceRanking",
    "Stats",
    "Story",
    "StoryDevelopment",
    "StoryList",
    "StoryUpdate",
    "Tag",
    "TrendingEntityList",
    "UsageRecord",
    "VersionInfo",
]


class NewsRank:
    """Synchronous client for the NewsRank API.

    Args:
        api_key: Your NewsRank API key (``nrf_...``).
        base_url: Override the default API base URL
            (``https://newsrank.ai/api/v1``).
        timeout: Request timeout in seconds (default: 30).
        httpx_client: An existing :class:`httpx.Client` instance.  When
            provided, the caller is responsible for closing it.

    Usage::

        nr = NewsRank("nrf_...")
        stories = nr.stories.list(limit=5)
        nr.close()

    Or as a context manager::

        with NewsRank("nrf_...") as nr:
            stories = nr.stories.list(limit=5)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        httpx_client: Optional[httpx.Client] = None,
    ) -> None:
        self._client = SyncClient(
            api_key,
            base_url=base_url,
            timeout=timeout,
            httpx_client=httpx_client,
        )

        self.articles: ArticlesResource = ArticlesResource(self._client)
        """Access the :doc:`articles` API."""

        self.stories: StoriesResource = StoriesResource(self._client)
        """Access the :doc:`stories` API."""

        self.search: SearchResource = SearchResource(self._client)
        """Access the :doc:`search` API."""

        self.entities: EntitiesResource = EntitiesResource(self._client)
        """Access the :doc:`entities` API."""

        self.sources: SourcesResource = SourcesResource(self._client)
        """Access the :doc:`sources` API."""

        self.graph: GraphResource = GraphResource(self._client)
        """Access the :doc:`graph` API."""

        self.meta: MetaResource = MetaResource(self._client)
        """Access the :doc:`meta` API."""

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._client.close()

    def __enter__(self) -> "NewsRank":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"NewsRank(base_url={self._client._base_url!r})"


class AsyncNewsRank:
    """Asynchronous client for the NewsRank API.

    Args:
        api_key: Your NewsRank API key (``nrf_...``).
        base_url: Override the default API base URL
            (``https://newsrank.ai/api/v1``).
        timeout: Request timeout in seconds (default: 30).
        httpx_client: An existing :class:`httpx.AsyncClient` instance.  When
            provided, the caller is responsible for closing it.

    Usage::

        async with AsyncNewsRank("nrf_...") as nr:
            stories = await nr.stories.list(limit=5)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        httpx_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self._client = AsyncClient(
            api_key,
            base_url=base_url,
            timeout=timeout,
            httpx_client=httpx_client,
        )

        self.articles: AsyncArticlesResource = AsyncArticlesResource(self._client)
        """Access the :doc:`articles` API."""

        self.stories: AsyncStoriesResource = AsyncStoriesResource(self._client)
        """Access the :doc:`stories` API."""

        self.search: AsyncSearchResource = AsyncSearchResource(self._client)
        """Access the :doc:`search` API."""

        self.entities: AsyncEntitiesResource = AsyncEntitiesResource(self._client)
        """Access the :doc:`entities` API."""

        self.sources: AsyncSourcesResource = AsyncSourcesResource(self._client)
        """Access the :doc:`sources` API."""

        self.graph: AsyncGraphResource = AsyncGraphResource(self._client)
        """Access the :doc:`graph` API."""

        self.meta: AsyncMetaResource = AsyncMetaResource(self._client)
        """Access the :doc:`meta` API."""

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._client.close()

    async def __aenter__(self) -> "AsyncNewsRank":
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()

    def __repr__(self) -> str:
        return f"AsyncNewsRank(base_url={self._client._base_url!r})"
