"""TypedDict response types for the NewsRank API.

These types provide IDE autocompletion and type-checking for API responses.
All fields use ``total=False`` so that missing keys from the API do not
cause runtime errors.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict


# ---------------------------------------------------------------------------
# Articles
# ---------------------------------------------------------------------------

class Article(TypedDict, total=False):
    """A news article."""
    id: int
    url: str
    url_hash: str
    slug: str
    title: str
    description: str
    author: str
    source_name: str
    source_domain: str
    image_url: str
    published_at: str
    created_at: str
    updated_at: str
    category: str
    subcategory: str
    content_status: str
    story_id: Optional[int]
    sentiment_score: Optional[float]
    sentiment_label: Optional[str]
    word_count: Optional[int]
    reading_time_minutes: Optional[int]


class ArticleContent(TypedDict, total=False):
    """Full extracted content for an article."""
    url_hash: str
    content: str
    content_html: str
    word_count: int
    reading_time_minutes: int
    extracted_at: str


class ArticleList(TypedDict, total=False):
    """Paginated list of articles."""
    items: List[Article]
    total: int
    limit: int
    offset: int


# ---------------------------------------------------------------------------
# Stories
# ---------------------------------------------------------------------------

class Story(TypedDict, total=False):
    """A clustered news story."""
    id: int
    slug: str
    title: str
    summary: str
    category: str
    subcategory: str
    image_url: str
    article_count: int
    source_count: int
    first_seen: str
    last_updated: str
    importance_score: float
    trending_score: float
    entities: List[Dict[str, Any]]


class StoryDevelopment(TypedDict, total=False):
    """A development within a story timeline."""
    id: int
    story_id: int
    title: str
    summary: str
    timestamp: str
    article_count: int
    articles: List[Article]


class StoryUpdate(TypedDict, total=False):
    """Recent updates to a story since a given timestamp."""
    new_articles: List[Article]
    new_developments: List[StoryDevelopment]
    updated_summary: Optional[str]


class StoryList(TypedDict, total=False):
    """Paginated list of stories."""
    items: List[Story]
    total: int
    limit: int
    offset: int


class RankedStoryList(TypedDict, total=False):
    """Ranked list of stories."""
    items: List[Story]


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

class SearchResult(TypedDict, total=False):
    """A search result item."""
    id: int
    url_hash: str
    slug: str
    title: str
    description: str
    source_name: str
    published_at: str
    category: str
    score: float


class SearchResults(TypedDict, total=False):
    """Search response."""
    items: List[SearchResult]
    total: int
    limit: int
    offset: int
    query: str


class FullSearchResults(TypedDict, total=False):
    """Full-text search response with articles and stories."""
    articles: List[SearchResult]
    stories: List[Dict[str, Any]]
    total: int
    query: str


class SearchSuggestion(TypedDict, total=False):
    """A search suggestion."""
    text: str
    type: str
    id: Optional[int]


class SearchSuggestions(TypedDict, total=False):
    """Search suggestions response."""
    suggestions: List[SearchSuggestion]


# ---------------------------------------------------------------------------
# Entities
# ---------------------------------------------------------------------------

class Entity(TypedDict, total=False):
    """A named entity (person, organization, place, etc.)."""
    id: int
    name: str
    slug: str
    type: str
    subcategory: str
    description: str
    image_url: str
    wikipedia_url: str
    article_count: int
    story_count: int
    first_seen: str
    last_seen: str
    trending_score: float


class EntityList(TypedDict, total=False):
    """Paginated list of entities."""
    items: List[Entity]
    total: int
    limit: int
    offset: int


class TrendingEntityList(TypedDict, total=False):
    """List of trending entities."""
    items: List[Entity]


class PoliticianList(TypedDict, total=False):
    """Paginated list of politician entities."""
    items: List[Entity]
    total: int
    limit: int
    offset: int


# ---------------------------------------------------------------------------
# Sources & Categories
# ---------------------------------------------------------------------------

class Source(TypedDict, total=False):
    """A news source."""
    id: int
    name: str
    domain: str
    url: str
    feed_url: str
    category: str
    language: str
    country: str
    reliability_score: Optional[float]
    bias_label: Optional[str]
    article_count: int
    active: bool


class Category(TypedDict, total=False):
    """A news category."""
    name: str
    slug: str
    article_count: int
    story_count: int


class Tag(TypedDict, total=False):
    """A content tag."""
    name: str
    count: int


class SourceRanking(TypedDict, total=False):
    """A ranked news source."""
    source_name: str
    source_domain: str
    article_count: int
    avg_sentiment: Optional[float]
    reliability_score: Optional[float]


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------

class GraphNode(TypedDict, total=False):
    """A node in a graph visualization."""
    id: str
    label: str
    type: str
    size: float
    metadata: Dict[str, Any]


class GraphEdge(TypedDict, total=False):
    """An edge in a graph visualization."""
    source: str
    target: str
    weight: float
    label: str


class Graph(TypedDict, total=False):
    """A graph of nodes and edges."""
    nodes: List[GraphNode]
    edges: List[GraphEdge]


# ---------------------------------------------------------------------------
# Meta
# ---------------------------------------------------------------------------

class RelatedArticle(TypedDict, total=False):
    """A related article."""
    url_hash: str
    slug: str
    title: str
    source_name: str
    published_at: str
    similarity: float


class Stats(TypedDict, total=False):
    """Platform-wide statistics."""
    total_articles: int
    total_stories: int
    total_sources: int
    total_entities: int
    articles_today: int
    stories_today: int
    last_updated: str


class VersionInfo(TypedDict, total=False):
    """API version information."""
    version: str
    build: str
    go_version: str
    uptime: str


class UsageRecord(TypedDict, total=False):
    """API usage statistics."""
    total_requests: int
    period_start: str
    period_end: str
    endpoints: Dict[str, int]
    daily_breakdown: List[Dict[str, Any]]
