"""dlt pipeline for gaming analytics data loading."""

import logging
from typing import TYPE_CHECKING, Any

import dlt
from dlt.common.destination import Destination
from pendulum import DateTime
from pendulum import now as pendulum_now

from gaming_pipeline.config import config
from gaming_pipeline.extract.base import DefaultExtractors, ExtractorBundle

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class GamingPipeline:
    """dlt pipeline for gaming analytics data."""

    def __init__(
        self,
        destination: Destination | None = None,
        dataset_name: str = "gaming_analytics",
        extractors: ExtractorBundle | None = None,
    ):
        self.destination = destination or dlt.destinations.duckdb(
            credentials=config.database.connection_uri
        )
        self.dataset_name = dataset_name
        self.extractors = extractors or DefaultExtractors()
        self.pipeline = self._create_pipeline()

    def _create_pipeline(self) -> dlt.Pipeline:
        """Create dlt pipeline instance."""
        return dlt.pipeline(
            pipeline_name="gaming_analytics",
            destination=self.destination,
            dataset_name=self.dataset_name,
            progress="log",
            dev_mode=config.is_production is False,
        )

    async def load_rawg_data(
        self,
        page_size: int = 20,
        max_pages: int | None = None,
        updated_after: "DateTime | None" = None,
    ) -> dict[str, Any]:
        """Load RAWG data into pipeline."""
        logger.info("Starting RAWG data load")

        # Load genres
        genres = await self.extractors.extract_genres()
        if genres:
            load_info = self.pipeline.run(
                genres, table_name="rawg_genres", write_disposition="replace"
            )
            logger.info(f"Loaded {len(genres)} genres: {load_info}")

        # Load platforms
        platforms = await self.extractors.extract_platforms()
        if platforms:
            load_info = self.pipeline.run(
                platforms, table_name="rawg_platforms", write_disposition="replace"
            )
            logger.info(f"Loaded {len(platforms)} platforms: {load_info}")

        # Load games in batches
        total_games = 0
        games_generator = self.extractors.extract_games(
            page_size, max_pages, updated_after
        )
        async for games_batch in games_generator:
            if games_batch:
                load_info = self.pipeline.run(
                    games_batch, table_name="rawg_games", write_disposition="append"
                )
                total_games += len(games_batch)
                logger.info(f"Loaded batch of {len(games_batch)} games: {load_info}")

        return {
            "total_games": total_games,
            "genres": len(genres) if genres else 0,
            "platforms": len(platforms) if platforms else 0,
        }

    async def run_full_load(self) -> dict[str, Any]:
        """Run full data load for all sources."""
        logger.info("Starting full data load")

        # Load RAWG data
        rawg_result = await self.load_rawg_data(
            page_size=50,  # Load more per page for initial load
            max_pages=10,  # Limit for demo
            updated_after=pendulum_now().subtract(days=30),  # Last 30 days
        )

        return {
            "rawg": rawg_result,
            "timestamp": pendulum_now().isoformat(),
        }

    def get_load_info(self) -> Any:
        """Get information about last load."""
        try:
            trace = self.pipeline.last_trace
            return trace if trace is not None else {}
        except Exception as e:
            logger.error(f"Failed to get load info: {e}")
            return {}

    def get_schema(self) -> Any:
        """Get current schema."""
        try:
            return self.pipeline.default_schema.to_dict()
        except Exception as e:
            logger.error(f"Failed to get schema: {e}")
            return {}

    def refresh_schema(self) -> None:
        """Refresh schema from destination."""
        try:
            self.pipeline.refresh()  # type: ignore[misc]
        except Exception as e:
            logger.error(f"Failed to refresh schema: {e}")


async def run_gaming_pipeline() -> dict[str, Any]:
    """Convenience function to run full gaming pipeline."""
    pipeline = GamingPipeline()
    return await pipeline.run_full_load()


def create_pipeline_instance() -> GamingPipeline:
    """Create a pipeline instance for use in Prefect flows."""
    return GamingPipeline()
