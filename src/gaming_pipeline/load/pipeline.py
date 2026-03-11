"""dlt pipeline for gaming analytics data loading."""

import logging
from typing import Any

import dlt
from dlt.common.destination import Destination
from pendulum import DateTime
from pendulum import now as pendulum_now

from gaming_pipeline.config import config
from gaming_pipeline.extract.dlt_source import rawg_source

logger = logging.getLogger(__name__)


class GamingPipeline:
    """dlt pipeline for gaming analytics data.

    This class handles loading data from the RAWG API using dlt's
    built-in REST API source. The source provides:
    - Automatic retry with exponential backoff
    - Rate limiting support
    - Pagination handling
    - Schema inference
    """

    def __init__(
        self,
        destination: Destination | None = None,
        dataset_name: str = "gaming_analytics",
    ):
        self.destination = destination or dlt.destinations.duckdb(
            credentials=config.database.connection_uri
        )
        self.dataset_name = dataset_name
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
        updated_after: "DateTime | str | None" = None,
    ) -> dict[str, Any]:
        """Load RAWG data into pipeline using dlt source.

        Args:
            page_size: Number of items per page (max 100).
            max_pages: Maximum number of pages to fetch. None for all.
            updated_after: ISO date string or DateTime for incremental loading.

        Returns:
            Dictionary with load statistics.
        """
        logger.info("Starting RAWG data load via dlt REST API source")

        # Convert DateTime to ISO string if needed
        updated_after_str: str | None = None
        if updated_after:
            if isinstance(updated_after, DateTime):
                updated_after_str = updated_after.to_iso8601_string()
            else:
                updated_after_str = updated_after

        try:
            # Create the dlt source
            source = rawg_source(
                page_size=page_size,
                max_pages=max_pages,
                updated_after=updated_after_str,
            )

            # Run the pipeline with the source
            load_info = self.pipeline.run(source)

            # Extract statistics from load info
            jobs = (
                load_info.load_packages[0].jobs["completed_jobs"]
                if load_info.load_packages
                else []
            )
            stats = {
                "total_games": 0,
                "genres": 0,
                "platforms": 0,
            }
            for job in jobs:
                table_name = job.job_file_info.table_name
                if "games" in table_name:
                    stats["total_games"] += job.job_file_info.rows  # type: ignore[attr-defined]
                elif "genres" in table_name:
                    stats["genres"] = job.job_file_info.rows  # type: ignore[attr-defined]
                elif "platforms" in table_name:
                    stats["platforms"] = job.job_file_info.rows  # type: ignore[attr-defined]

            logger.info(f"RAWG data load complete: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Failed to load RAWG data: {e}")
            return {
                "total_games": 0,
                "genres": 0,
                "platforms": 0,
                "error": str(e),
            }

    async def run_full_load(
        self,
        page_size: int = 50,
        max_pages: int = 10,
        updated_after_days: int = 30,
    ) -> dict[str, Any]:
        """Run full data load for all sources.

        Args:
            page_size: Number of items per page (max 100).
            max_pages: Maximum number of pages to fetch.
            updated_after_days: Number of days to look back for incremental loading.

        Returns:
            Dictionary with load statistics and timestamp.
        """
        logger.info(
            f"Starting full data load (page_size={page_size}, "
            f"max_pages={max_pages}, updated_after_days={updated_after_days})"
        )

        try:
            # Load RAWG data
            rawg_result = await self.load_rawg_data(
                page_size=page_size,
                max_pages=max_pages,
                updated_after=pendulum_now().subtract(days=updated_after_days),
            )

            return {
                "rawg": rawg_result,
                "timestamp": pendulum_now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Full load failed: {e}")
            return {
                "rawg": {"error": str(e)},
                "timestamp": pendulum_now().isoformat(),
                "error": str(e),
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
