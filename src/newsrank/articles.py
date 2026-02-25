"""Articles resource — list, get, and fetch full content for news articles."""

from __future__ import annotations

from typing import Any, Optional, Union

from newsrank._client import AsyncClient, SyncClient
from newsrank._types import Article, ArticleContent, ArticleList


class ArticlesResource:
    """Synchronous articles API.

    Usage::

        articles = nr.articles.list(limit=10, category="politics")
        article  = nr.articles.get(url_hash="abc123")
        content  = nr.articles.content(url_hash="abc123")
    """

    def __init__(self, client: SyncClient) -> None:
        self._client = client

    def list(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        category: Optional[str] = None,
        keyword: Optional[str] = None,
        source: Optional[str] = None,
        content_status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> ArticleList:
        """List articles with optional filtering and pagination.

        Args:
            limit: Maximum number of articles to return.
            offset: Number of articles to skip.
            category: Filter by category slug.
            keyword: Filter by keyword.
            source: Filter by source domain.
            content_status: Filter by content extraction status.
            date_from: Filter articles published after this date (ISO 8601).
            date_to: Filter articles published before this date (ISO 8601).
            sort_by: Field to sort by (e.g. ``published_at``).
            sort_order: Sort direction: ``asc`` or ``desc``.
        """
        return self._client.get(
            "/items",
            params={
                "limit": limit,
                "offset": offset,
                "category": category,
                "keyword": keyword,
                "source": source,
                "content_status": content_status,
                "date_from": date_from,
                "date_to": date_to,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
        )

    def get(
        self,
        *,
        url_hash: Optional[str] = None,
        slug: Optional[str] = None,
    ) -> Article:
        """Get a single article by URL hash or slug.

        You must provide at least one of ``url_hash`` or ``slug``.
        """
        return self._client.get(
            "/item",
            params={"url_hash": url_hash, "slug": slug},
        )

    def content(
        self,
        url_hash: str,
        *,
        max_chars: Optional[int] = None,
    ) -> ArticleContent:
        """Get the full extracted content for an article.

        Args:
            url_hash: The article's URL hash (required).
            max_chars: Truncate the content to this many characters.
        """
        return self._client.get(
            "/content",
            params={"url_hash": url_hash, "max_chars": max_chars},
        )


class AsyncArticlesResource:
    """Asynchronous articles API."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        category: Optional[str] = None,
        keyword: Optional[str] = None,
        source: Optional[str] = None,
        content_status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> ArticleList:
        """List articles with optional filtering and pagination."""
        return await self._client.get(
            "/items",
            params={
                "limit": limit,
                "offset": offset,
                "category": category,
                "keyword": keyword,
                "source": source,
                "content_status": content_status,
                "date_from": date_from,
                "date_to": date_to,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
        )

    async def get(
        self,
        *,
        url_hash: Optional[str] = None,
        slug: Optional[str] = None,
    ) -> Article:
        """Get a single article by URL hash or slug."""
        return await self._client.get(
            "/item",
            params={"url_hash": url_hash, "slug": slug},
        )

    async def content(
        self,
        url_hash: str,
        *,
        max_chars: Optional[int] = None,
    ) -> ArticleContent:
        """Get the full extracted content for an article."""
        return await self._client.get(
            "/content",
            params={"url_hash": url_hash, "max_chars": max_chars},
        )
