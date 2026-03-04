"""RAWG API extractor for gaming analytics pipeline."""

import asyncio
import logging
from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Any, cast

import httpx
from pendulum import DateTime
from pydantic import BaseModel

from gaming_pipeline.config import config

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class Game(BaseModel):
    """Game model for RAWG API data."""

    id: int
    name: str
    released: str | None = None
    background_image: str | None = None
    rating: float | None = None
    rating_top: int | None = None
    ratings_count: int | None = None
    reviews_text_count: int | None = None
    added: int | None = None
    metacritic: int | None = None
    playtime: int | None = None
    suggestions_count: int | None = None
    updated: str | None = None
    reviews_count: int | None = None
    saturated_color: str | None = None
    dominant_color: str | None = None
    platforms: list[dict[str, Any]] | None = None
    parent_platforms: list[dict[str, Any]] | None = None
    genres: list[dict[str, Any]] | None = None
    stores: list[dict[str, Any]] | None = None
    clip: dict[str, Any] | None = None
    tags: list[dict[str, Any]] | None = None
    short_screenshots: list[dict[str, Any]] | None = None


class RAWGExtractor:
    """Extractor for RAWG API data."""

    def __init__(self):
        self.base_url = config.api.rawg_base_url
        self.headers = config.api.rawg_headers
        self.session: httpx.AsyncClient | None = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = httpx.AsyncClient(
            headers=self.headers,
            timeout=30.0,
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.aclose()

    async def _make_request(
        self, endpoint: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        """Make HTTP request to RAWG API with retry logic."""
        if self.session is None:
            raise RuntimeError("Session not initialized. Use async context manager.")

        for attempt in range(config.pipeline.max_retries):
            try:
                response = await self.session.get(
                    f"{self.base_url}/{endpoint}", params=params
                )
                response.raise_for_status()
                return cast(dict[str, Any], response.json())
            except httpx.HTTPError as e:
                logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt == config.pipeline.max_retries - 1:
                    raise
                await asyncio.sleep(config.pipeline.retry_delay * (attempt + 1))

        # This should never be reached but satisfies type checker
        raise RuntimeError("Max retries exceeded")

    def extract_games(
        self,
        page_size: int = 20,
        max_pages: int | None = None,
        updated_after: "DateTime | None" = None,
    ) -> AsyncGenerator[list[Game], None]:
        """Extract games from RAWG API."""
        return self._extract_games_impl(page_size, max_pages, updated_after)

    async def _extract_games_impl(
        self,
        page_size: int,
        max_pages: int | None,
        updated_after: "DateTime | None",
    ) -> AsyncGenerator[list[Game], None]:
        """Implementation of game extraction."""
        page = 1
        total_pages = max_pages or 100  # Default to 100 pages if not specified

        while page <= total_pages:
            params = {
                "page": page,
                "page_size": min(page_size, config.pipeline.batch_size),
                "ordering": "-updated",
                "key": config.api.rawg_api_key,
            }

            # Add date filter if provided
            if updated_after:
                params["updated_after"] = updated_after.to_iso8601_string()

            try:
                data = await self._make_request("games", params)
                games_data = data.get("results", [])

                if not games_data:
                    logger.info(f"No more games found at page {page}")
                    break

                # Convert to Game models
                games = [Game(**game_data) for game_data in games_data]
                yield games

                logger.info(f"Extracted {len(games)} games from page {page}")
                page += 1

            except Exception as e:
                logger.error(f"Failed to extract games from page {page}: {e}")
                break

    async def extract_game_details(self, game_id: int) -> Game | None:
        """Extract detailed information for a specific game."""
        try:
            data = await self._make_request(f"games/{game_id}", {})
            return Game(**data)
        except Exception as e:
            logger.error(f"Failed to extract details for game {game_id}: {e}")
            return None

    async def extract_genres(self) -> list[dict[str, Any]]:
        """Extract available genres from RAWG API."""
        try:
            data = await self._make_request("genres", {})
            results = data.get("results", [])
            return cast(list[dict[str, Any]], results)
        except Exception as e:
            logger.error(f"Failed to extract genres: {e}")
            return []

    async def extract_platforms(self) -> list[dict[str, Any]]:
        """Extract available platforms from RAWG API."""
        try:
            data = await self._make_request("platforms", {})
            results = data.get("results", [])
            return cast(list[dict[str, Any]], results)
        except Exception as e:
            logger.error(f"Failed to extract platforms: {e}")
            return []


async def extract_rawg_games(
    page_size: int = 20,
    max_pages: int | None = None,
    updated_after: "DateTime | None" = None,
) -> AsyncGenerator[list[Game]]:
    """Convenience function to extract RAWG games."""
    async with RAWGExtractor() as extractor:
        async for games in extractor.extract_games(page_size, max_pages, updated_after):
            yield games


async def extract_rawg_genres() -> list[dict[str, Any]]:
    """Convenience function to extract RAWG genres."""
    async with RAWGExtractor() as extractor:
        result = await extractor.extract_genres()
        return cast(list[dict[str, Any]], result)


async def extract_rawg_platforms() -> list[dict[str, Any]]:
    """Convenience function to extract RAWG platforms."""
    async with RAWGExtractor() as extractor:
        result = await extractor.extract_platforms()
        return cast(list[dict[str, Any]], result)
