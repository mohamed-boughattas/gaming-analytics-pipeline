"""Prefect flows for gaming analytics pipeline."""

import logging
from typing import TYPE_CHECKING, Any

from pendulum import now as pendulum_now
from prefect import flow, get_run_logger

if TYPE_CHECKING:
    pass

from gaming_pipeline.orchestrate.tasks import (
    extract_rawg_genres_task,
    extract_rawg_platforms_task,
    get_load_info_task,
    get_pipeline_schema_task,
    load_rawg_data_task,
    refresh_schema_task,
    run_full_pipeline_task,
)

logger = logging.getLogger(__name__)


@flow(
    name="gaming-analytics-daily",
    description="Daily gaming analytics data pipeline",
    log_prints=True,
)
async def daily_pipeline_flow(
    page_size: int = 50, max_pages: int = 10, updated_after_days: int = 1
) -> dict[str, Any]:
    """Daily pipeline flow for gaming analytics."""
    logger = get_run_logger()
    logger.info("Starting daily gaming analytics pipeline")

    # Run full pipeline
    result = await run_full_pipeline_task(
        page_size=page_size, max_pages=max_pages, updated_after_days=updated_after_days
    )

    # Get schema and load info
    schema = get_pipeline_schema_task()
    load_info = get_load_info_task()

    # Refresh schema
    refresh_schema_task()

    final_result = {
        "pipeline_result": result,
        "schema": schema,
        "load_info": load_info,
        "execution_time": pendulum_now().isoformat(),
    }

    logger.info("Daily pipeline completed successfully")
    return final_result


@flow(
    name="gaming-analytics-full-load",
    description="Full load gaming analytics pipeline",
    log_prints=True,
)
async def full_load_pipeline_flow(
    page_size: int = 100, max_pages: int = 50
) -> dict[str, Any]:
    """Full load pipeline flow for gaming analytics."""
    logger = get_run_logger()
    logger.info("Starting full load gaming analytics pipeline")

    # Run full pipeline with larger batch sizes
    result = await run_full_pipeline_task(
        page_size=page_size,
        max_pages=max_pages,
        updated_after_days=365,  # Full year of data
    )

    # Get schema and load info
    schema = get_pipeline_schema_task()
    load_info = get_load_info_task()

    # Refresh schema
    refresh_schema_task()

    final_result = {
        "pipeline_result": result,
        "schema": schema,
        "load_info": load_info,
        "execution_time": pendulum_now().isoformat(),
    }

    logger.info("Full load pipeline completed successfully")
    return final_result


@flow(
    name="gaming-analytics-extract-only",
    description="Extract only flow for gaming analytics",
    log_prints=True,
)
async def extract_only_flow() -> dict[str, Any]:
    """Extract only flow for gaming analytics."""
    logger = get_run_logger()
    logger.info("Starting extract-only gaming analytics pipeline")

    # Extract genres and platforms
    genres = await extract_rawg_genres_task()
    platforms = await extract_rawg_platforms_task()

    result = {
        "genres_extracted": len(genres),
        "platforms_extracted": len(platforms),
        "execution_time": pendulum_now().isoformat(),
    }

    logger.info("Extract-only pipeline completed successfully")
    return result


@flow(
    name="gaming-analytics-load-only",
    description="Load only flow for gaming analytics",
    log_prints=True,
)
async def load_only_flow(
    page_size: int = 50, max_pages: int = 10, updated_after_days: int = 7
) -> dict[str, Any]:
    """Load only flow for gaming analytics."""
    logger = get_run_logger()
    logger.info("Starting load-only gaming analytics pipeline")

    # Calculate updated_after date
    updated_after = pendulum_now().subtract(days=updated_after_days)

    # Load RAWG data
    rawg_result = await load_rawg_data_task(
        page_size=page_size, max_pages=max_pages, updated_after=updated_after
    )

    result = {
        "rawg_load": rawg_result,
        "execution_time": pendulum_now().isoformat(),
    }

    logger.info("Load-only pipeline completed successfully")
    return result


# Note: Prefect 3.x deployments are created using the CLI:
# prefect deploy <flow_name> --name <deployment_name> --cron <schedule>
#
# For local development, use the run_*_pipeline() functions below.
# For production deployment, see Prefect documentation for deployment commands.


# Example usage functions
async def run_daily_pipeline() -> dict[str, Any]:
    """Run daily pipeline."""
    return await daily_pipeline_flow()


async def run_full_load_pipeline() -> dict[str, Any]:
    """Run full load pipeline."""
    return await full_load_pipeline_flow()


async def run_extract_only_pipeline() -> dict[str, Any]:
    """Run extract-only pipeline."""
    return await extract_only_flow()


async def run_load_only_pipeline() -> dict[str, Any]:
    """Run load-only pipeline."""
    return await load_only_flow()
