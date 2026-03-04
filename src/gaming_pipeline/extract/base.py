"""Base classes and protocols for data extractors."""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Any

from pendulum import DateTime

if TYPE_CHECKING:
    pass


class ExtractorBundle(ABC):
    """Protocol for data extractor bundles."""

    @abstractmethod
    async def extract_genres(self) -> list[dict[str, Any]]:
        """Extract genre data."""
        pass

    @abstractmethod
    async def extract_platforms(self) -> list[dict[str, Any]]:
        """Extract platform data."""
        pass

    @abstractmethod
    def extract_games(
        self, page_size: int, max_pages: int | None, updated_after: "DateTime | None"
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        """Extract game data as batches."""
        pass


class DefaultExtractors(ExtractorBundle):
    """Default extractors using actual API calls."""

    async def extract_genres(self) -> list[dict[str, Any]]:
        """Extract genre data using default extractor."""
        from .rawg import extract_rawg_genres

        genres = await extract_rawg_genres()
        # Convert to dict (handle both Pydantic model and dict)
        result = []
        for genre in genres:
            if hasattr(genre, "model_dump"):
                result.append(genre.model_dump())  # type: ignore[attr-defined]
            elif isinstance(genre, dict):
                result.append(genre)
        return result

    async def extract_platforms(self) -> list[dict[str, Any]]:
        """Extract platform data using default extractor."""
        from .rawg import extract_rawg_platforms

        platforms = await extract_rawg_platforms()
        # Convert to dict (handle both Pydantic model and dict)
        result = []
        for platform in platforms:
            if hasattr(platform, "model_dump"):
                result.append(platform.model_dump())  # type: ignore[attr-defined]
            elif isinstance(platform, dict):
                result.append(platform)
        return result

    def extract_games(
        self, page_size: int, max_pages: int | None, updated_after: "DateTime | None"
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        """Extract game data using default extractor."""
        return self._extract_games_impl(page_size, max_pages, updated_after)

    async def _extract_games_impl(
        self, page_size: int, max_pages: int | None, updated_after: "DateTime | None"
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        """Implementation of game extraction."""
        from .rawg import extract_rawg_games

        async for games_batch in extract_rawg_games(
            page_size, max_pages, updated_after
        ):
            if games_batch:
                # Convert to dict (handle both Pydantic model and dict)
                result = []
                for game in games_batch:
                    if hasattr(game, "model_dump"):
                        result.append(game.model_dump())
                    elif isinstance(game, dict):
                        result.append(game)
                yield result
