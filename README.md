# NewsRank Python SDK

The official Python client for the [NewsRank API](https://newsrank.ai/docs).

## Installation

```bash
pip install newsrank
```

Requires Python 3.9+.

## Quick start

```python
from newsrank import NewsRank

nr = NewsRank("nrf_your_api_key")

# List top stories
stories = nr.stories.ranked(limit=5)
for story in stories["items"]:
    print(story["title"])

# Search articles
results = nr.search.articles(q="climate change")

# Get trending entities
trending = nr.entities.trending(limit=10)

# Close when done
nr.close()
```

### Context manager

```python
with NewsRank("nrf_...") as nr:
    stats = nr.meta.stats()
    print(f"Total articles: {stats['total_articles']}")
```

## Async usage

```python
import asyncio
from newsrank import AsyncNewsRank

async def main():
    async with AsyncNewsRank("nrf_...") as nr:
        stories = await nr.stories.ranked(limit=5)
        articles = await nr.articles.list(category="politics", limit=10)

asyncio.run(main())
```

## Resources

The client is organized into namespaced resources:

| Resource | Description |
|---|---|
| `nr.articles` | List, get, and fetch content for news articles |
| `nr.stories` | List, get, and track developments for stories |
| `nr.search` | Search articles, full-text search, suggestions |
| `nr.entities` | Named entities, trending, politicians |
| `nr.sources` | News sources, categories, tags, rankings |
| `nr.graph` | Entity networks, story-entity, topic clusters |
| `nr.meta` | Related articles, stats, version, usage |

## Articles

```python
# List articles with filters
articles = nr.articles.list(
    category="politics",
    source="reuters.com",
    limit=20,
    sort_by="published_at",
    sort_order="desc",
)

# Get a single article
article = nr.articles.get(url_hash="abc123")

# Get full extracted content
content = nr.articles.content("abc123", max_chars=5000)
```

## Stories

```python
# List stories
stories = nr.stories.list(category="technology", limit=10)

# Get ranked stories
ranked = nr.stories.ranked(limit=5)

# Get by ID or slug
story = nr.stories.get(42)
story = nr.stories.get("supreme-court-climate-ruling")

# Get timeline developments
devs = nr.stories.developments(42)

# Check for updates since a timestamp
updates = nr.stories.updates(42, since_ms=1700000000000)
```

## Search

```python
# Basic search
results = nr.search.articles(q="election", limit=10)

# Full-text search (articles + stories)
full = nr.search.full(q="climate policy")

# Autocomplete suggestions
suggestions = nr.search.suggest(q="clim")
```

## Entities

```python
# List entities
entities = nr.entities.list(type="person", limit=20)

# Trending entities
trending = nr.entities.trending(limit=10)

# Politicians
pols = nr.entities.politicians(limit=50)

# Get entity details
entity = nr.entities.get("joe-biden")

# Entity's articles
articles = nr.entities.articles(42, limit=10)
```

## Graph

```python
# Entity co-occurrence network
network = nr.graph.entity_network(entity_id=42, depth=2, limit=50)

# Story-entity graph
story_graph = nr.graph.story_entity(story_id=7)

# Topic cluster graph
topic_graph = nr.graph.topic_cluster(topic_id=3, limit=30)
```

## Error handling

```python
from newsrank import NewsRank, NewsRankError, NotFoundError, RateLimitError

nr = NewsRank("nrf_...")

try:
    story = nr.stories.get("nonexistent-slug")
except NotFoundError:
    print("Story not found")
except RateLimitError:
    print("Rate limit exceeded — slow down")
except NewsRankError as e:
    print(f"API error {e.status_code}: {e.message}")
```

All exceptions inherit from `NewsRankError` and include:
- `status_code` — HTTP status code (or `None` for connection errors)
- `message` — Human-readable error message
- `body` — Raw response body

Exception hierarchy:
- `NewsRankError` — base class
  - `AuthenticationError` — 401
  - `PermissionError` — 403
  - `NotFoundError` — 404
  - `RateLimitError` — 429
  - `ServerError` — 5xx

## Configuration

```python
import httpx
from newsrank import NewsRank

# Custom base URL (for testing)
nr = NewsRank("nrf_...", base_url="http://localhost:8080/api/v1")

# Custom timeout
nr = NewsRank("nrf_...", timeout=60.0)

# Bring your own httpx client
client = httpx.Client(
    verify=False,
    proxies="http://proxy:8080",
)
nr = NewsRank("nrf_...", httpx_client=client)
```

## License

MIT
