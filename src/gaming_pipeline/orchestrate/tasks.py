"""Prefect tasks for gaming analytics pipeline."""

import logging
from typing import TYPE_CHECKING, Any

from pendulum import now as pendulum_now
from prefect import task
from prefect.artifacts import create_markdown_artifact

from gaming_pipeline.config import settings
from gaming_pipeline.extract import extract_rawg_genres, extract_rawg_platforms
from gaming_pipeline.load.pipeline import GamingPipeline

if TYPE_CHECKING:
    import pendulum

logger = logging.getLogger(__name__)


@task(
    name="Extract RAWG Genres",
    description="Extract genre data from RAWG API",
    retries=3,
    retry_delay_seconds=30,
)
async def extract_rawg_genres_task() -> list[dict[str, Any]]:
    """Extract genres from RAWG API."""
    logger.info("Starting RAWG genres extraction")
    genres = await extract_rawg_genres()

    # Create artifact with summary - create_markdown_artifact is sync in newer Prefect
    create_markdown_artifact(
        key="rawg-genres-summary",
        markdown=f"## RAWG Genres Extraction\n\nExtracted {len(genres)} genres",
        description="Summary of RAWG genres extraction",
    )

    logger.info(f"Successfully extracted {len(genres)} genres")
    return genres


@task(
    name="Extract RAWG Platforms",
    description="Extract platform data from RAWG API",
    retries=3,
    retry_delay_seconds=30,
)
async def extract_rawg_platforms_task() -> list[dict[str, Any]]:
    """Extract platforms from RAWG API."""
    logger.info("Starting RAWG platforms extraction")
    platforms = await extract_rawg_platforms()

    # Create artifact with summary - create_markdown_artifact is sync
    create_markdown_artifact(
        key="rawg-platforms-summary",
        markdown=(
            f"## RAWG Platforms Extraction\n\nExtracted {len(platforms)} platforms"
        ),
        description="Summary of RAWG platforms extraction",
    )

    logger.info(f"Successfully extracted {len(platforms)} platforms")
    return platforms


@task(
    name="Load RAWG Data",
    description="Load RAWG data into DuckDB",
    retries=2,
    retry_delay_seconds=60,
)
async def load_rawg_data_task(
    page_size: int = 20,
    max_pages: int = 10,
    updated_after: "pendulum.DateTime | None" = None,
) -> dict[str, Any]:
    """Load RAWG data into pipeline."""
    logger.info("Starting RAWG data load")

    pipeline = GamingPipeline()
    result = await pipeline.load_rawg_data(
        page_size=page_size, max_pages=max_pages, updated_after=updated_after
    )

    # Create artifact with load summary
    markdown_content = f"""
## RAWG Data Load Summary

- **Total Games Loaded**: {result.get("total_games", 0)}
- **Genres Loaded**: {result.get("genres", 0)}
- **Platforms Loaded**: {result.get("platforms", 0)}
- **Load Timestamp**: {pendulum_now().isoformat()}
"""

    # Create artifact with load summary
    create_markdown_artifact(
        key="rawg-load-summary",
        markdown=markdown_content,
        description="Summary of RAWG data load",
    )

    logger.info(f"Successfully loaded RAWG data: {result}")
    return result


@task(
    name="Run Full Pipeline",
    description="Run complete data pipeline",
    retries=1,
    retry_delay_seconds=120,
)
async def run_full_pipeline_task(
    page_size: int = 50, max_pages: int = 10, updated_after_days: int = 30
) -> dict[str, Any]:
    """Run complete gaming analytics pipeline."""
    logger.info("Starting full pipeline execution")

    pipeline = GamingPipeline()
    result = await pipeline.run_full_load()

    # Create comprehensive artifact
    rawg_result = result.get("rawg", {})

    markdown_content = f"""
# Gaming Analytics Pipeline Summary

## Execution Details
- **Pipeline Name**: gaming-analytics
- **Execution Time**: {result.get("timestamp", pendulum_now().isoformat())}
- **Environment**: {"Production" if settings.is_production else "Development"}

## RAWG Data Load Results
- **Total Games**: {rawg_result.get("total_games", 0)}
- **Genres**: {rawg_result.get("genres", 0)}
- **Platforms**: {rawg_result.get("platforms", 0)}

## Performance Notes
- Page Size: {page_size}
- Max Pages: {max_pages}
- Updated After: {updated_after_days} days
"""

    # Create comprehensive artifact
    create_markdown_artifact(
        key="pipeline-execution-summary",
        markdown=markdown_content,
        description="Comprehensive pipeline execution summary",
    )

    logger.info("Pipeline execution completed successfully")
    return result


@task(name="Get Pipeline Schema", description="Get current pipeline schema information")
def get_pipeline_schema_task() -> dict[str, Any]:
    """Get current pipeline schema."""
    logger.info("Retrieving pipeline schema")

    pipeline = GamingPipeline()
    schema = pipeline.get_schema()

    logger.info("Successfully retrieved pipeline schema")
    return schema


@task(
    name="Get Load Information",
    description="Get information about the last pipeline load",
)
def get_load_info_task() -> dict[str, Any]:
    """Get information about last load."""
    logger.info("Retrieving load information")

    pipeline = GamingPipeline()
    load_info = pipeline.get_load_info()

    logger.info("Successfully retrieved load information")
    return load_info


@task(
    name="Refresh Pipeline Schema",
    description="Refresh pipeline schema from destination",
)
def refresh_schema_task() -> None:
    """Refresh pipeline schema."""
    logger.info("Refreshing pipeline schema")

    pipeline = GamingPipeline()
    pipeline.refresh_schema()

    logger.info("Pipeline schema refreshed successfully")
