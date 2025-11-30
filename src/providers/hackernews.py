"""Hacker News provider for fetching best stories with pagination.

Fetches 50 best stories from Hacker News API, caches them, and provides
paginated access with automatic page rotation.
"""

import asyncio
import logging

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import Config
from src.core.cache import cached
from src.core.state import StateManager
from src.exceptions import ProviderError
from src.types import HackerNewsData, HackerNewsStory

logger = logging.getLogger(__name__)

# Hacker News API endpoints
HN_BEST_STORIES_URL = "https://hacker-news.firebaseio.com/v0/beststories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# State manager instance
_state_manager = StateManager(Config.DATA_DIR)


@cached(ttl=Config.display.hackernews_refresh_minutes * 60, maxsize=1)
async def _fetch_all_stories(client: httpx.AsyncClient) -> list[HackerNewsStory]:
    """Fetch all Hacker News stories (cached).

    Args:
        client: HTTP client instance

    Returns:
        List of story dictionaries

    Raises:
        ProviderError: If API request fails
    """
    try:
        logger.info("Fetching Hacker News best stories...")

        # Fetch ALL story IDs
        response = await client.get(HN_BEST_STORIES_URL, timeout=10.0)
        response.raise_for_status()
        story_ids = response.json()

        # Limit to top 50 stories to avoid fetching too much data
        # 50 stories = 10 pages of 5 stories each, which is plenty
        limit = 50
        story_ids = story_ids[:limit]

        logger.info(f"Fetching details for top {len(story_ids)} HN stories...")

        # Use a semaphore to limit concurrent requests
        sem = asyncio.Semaphore(10)

        async def fetch_with_sem(sid: int) -> dict | None:
            async with sem:
                return await _fetch_story(client, sid)

        # Fetch stories concurrently
        results = await asyncio.gather(*[fetch_with_sem(sid) for sid in story_ids])

        # Process results
        stories: list[HackerNewsStory] = []
        for i, story in enumerate(results):
            if not story:
                continue

            stories.append(
                {
                    "id": story_ids[i],
                    "title": story.get("title", ""),
                    "score": story.get("score", 0),
                }
            )

        if not stories:
            logger.warning("No HN stories found")
            return []

        logger.info(f"Fetched {len(stories)} HN stories")
        return stories

    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch Hacker News: {e}")
        raise ProviderError("hackernews", "Failed to fetch stories", e) from e
    except Exception as e:
        logger.error(f"Unexpected error fetching Hacker News: {e}")
        raise ProviderError("hackernews", "Unexpected error", e) from e


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def _fetch_story(client: httpx.AsyncClient, story_id: int) -> dict | None:
    """Fetch a single story from Hacker News API.

    Args:
        client: HTTP client instance
        story_id: Story ID to fetch

    Returns:
        Story data or None if failed
    """
    try:
        response = await client.get(HN_ITEM_URL.format(story_id), timeout=10.0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.warning(f"Failed to fetch HN story {story_id}: {e}")
        return None


async def get_hackernews(
    client: httpx.AsyncClient, advance_page: bool = False, reset_to_first: bool = False
) -> HackerNewsData:
    """Fetch paginated Hacker News stories.

    Args:
        client: HTTP client for making requests
        advance_page: If True, advance to next page
        reset_to_first: If True, reset to page 1 (useful on startup)

    Returns:
        Dictionary with:
        - stories: List of stories for current page
        - page: Current page number (1-indexed)
        - total_pages: Total number of pages
        - start_idx: Starting index (1-indexed)
        - end_idx: Ending index (1-indexed)

    Raises:
        ProviderError: If fetching stories fails
    """
    # Read current page from state
    current_page = await _state_manager.get("hackernews_page", default=1)

    # Reset to first page if requested
    if reset_to_first:
        current_page = 1

    # Advance page if requested
    if advance_page:
        current_page += 1

    # Fetch stories (uses cache decorator)
    try:
        stories = await _fetch_all_stories(client)
    except ProviderError:
        # Return empty result on error
        return {
            "stories": [],
            "page": 1,
            "total_pages": 1,
            "start_idx": 1,
            "end_idx": 0,
        }

    if not stories:
        return {
            "stories": [],
            "page": 1,
            "total_pages": 1,
            "start_idx": 1,
            "end_idx": 0,
        }

    # Calculate pagination
    per_page = Config.display.hackernews_stories_per_page
    total_pages = (len(stories) + per_page - 1) // per_page  # Ceiling division

    # Wrap around if exceeded (cycle back to page 1)
    if current_page > total_pages:
        current_page = 1
        logger.info("Cycled through all HN pages")

    # Calculate indices
    start_idx = (current_page - 1) * per_page + 1
    end_idx = min(current_page * per_page, len(stories))

    # Get current page stories
    page_stories = stories[start_idx - 1 : end_idx]

    # Save state
    await _state_manager.set("hackernews_page", current_page)

    return {
        "stories": page_stories,
        "page": current_page,
        "total_pages": total_pages,
        "start_idx": start_idx,
        "end_idx": end_idx,
    }
