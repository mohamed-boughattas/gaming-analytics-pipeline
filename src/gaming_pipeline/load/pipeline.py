"""dlt pipeline for gaming analytics data loading."""

import logging
from typing import Any

import dlt
import duckdb
from dlt.common.destination import Destination
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

    Uses local DuckDB as the destination.
    """

    def __init__(
        self,
        destination: Destination | None = None,
        dataset_name: str = "raw",
    ) -> None:
        """Initialize the pipeline.

        Args:
            destination: Optional dlt destination. Defaults to local DuckDB.
            dataset_name: Name of the dataset schema in the destination.
        """
        if destination is None:
            self.destination = dlt.destinations.duckdb(credentials=config.database.path)
        else:
            self.destination = destination
        self.dataset_name = dataset_name
        self.pipeline = self._create_pipeline()

    def _create_pipeline(self) -> dlt.Pipeline:
        """Create dlt pipeline instance.

        Returns:
            Configured dlt Pipeline instance.
        """
        return dlt.pipeline(
            pipeline_name="gaming_analytics",
            destination=self.destination,
            dataset_name=self.dataset_name,
            progress="log",
            dev_mode=False,
        )

    def load_rawg_data(
        self,
        page_size: int = 20,
        max_pages: int = 10,
    ) -> dict[str, Any]:
        """Load RAWG data into pipeline using dlt source.

        Args:
            page_size: Number of items per page (max 100).
            max_pages: Maximum number of pages to fetch.

        Returns:
            Dictionary with load statistics.
        """
        logger.info("Starting RAWG data load via dlt REST API source")

        try:
            source = rawg_source(
                page_size=page_size,
                max_pages=max_pages,
            )

            self.pipeline.run(source)

            try:
                with duckdb.connect(config.database.path, read_only=True) as conn:
                    games_query = "SELECT COUNT(*) FROM raw.games"
                    genres_query = "SELECT COUNT(*) FROM raw.genres"
                    platforms_query = "SELECT COUNT(*) FROM raw.platforms"
                    games_row = conn.execute(games_query).fetchone()
                    genres_row = conn.execute(genres_query).fetchone()
                    platforms_row = conn.execute(platforms_query).fetchone()
                    stats = {
                        "total_games": games_row[0] if games_row else 0,
                        "genres": genres_row[0] if genres_row else 0,
                        "platforms": platforms_row[0] if platforms_row else 0,
                    }
            except Exception:
                stats = {
                    "total_games": 0,
                    "genres": 0,
                    "platforms": 0,
                    "note": "Row count read failed",
                }

            logger.info("RAWG data load complete")
            return stats

        except Exception as e:
            logger.error(f"Failed to load RAWG data: {e}")
            return {
                "total_games": 0,
                "genres": 0,
                "platforms": 0,
                "error": str(e),
            }

    def run_full_load(
        self,
        page_size: int = 50,
        max_pages: int = 10,
    ) -> dict[str, Any]:
        """Run full data load for all sources.

        Args:
            page_size: Number of items per page (max 100).
            max_pages: Maximum number of pages to fetch.

        Returns:
            Dictionary with load statistics and timestamp.
        """
        logger.info(
            f"Starting full data load (page_size={page_size}, max_pages={max_pages})"
        )

        try:
            rawg_result = self.load_rawg_data(
                page_size=page_size,
                max_pages=max_pages,
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
        """Get information about last load.

        Returns:
            Dictionary with last load trace or empty dict.
        """
        try:
            trace = self.pipeline.last_trace
            return trace if trace is not None else {}
        except Exception as e:
            logger.error(f"Failed to get load info: {e}")
            return {}

    def get_schema(self) -> Any:
        """Get current schema.

        Returns:
            Dictionary representation of the pipeline schema.
        """
        try:
            return self.pipeline.default_schema.to_dict()
        except Exception as e:
            logger.error(f"Failed to get schema: {e}")
            return {}

    def refresh_schema(self) -> None:
        """Refresh schema from destination."""
        try:
            refresh = getattr(self.pipeline, "refresh", None)
            if callable(refresh):
                refresh()
            else:
                logger.debug("Pipeline refresh not available, skipping")
        except Exception as e:
            logger.debug(f"Failed to refresh schema: {e}")


def create_pipeline_instance() -> GamingPipeline:
    """Create a pipeline instance for use in Prefect flows.

    Returns:
        A new GamingPipeline instance.
    """
    return GamingPipeline()
