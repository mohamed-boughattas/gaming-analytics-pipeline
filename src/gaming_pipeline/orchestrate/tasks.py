"""Prefect tasks for gaming analytics pipeline."""

import logging
import secrets
from typing import Any

from pendulum import now as pendulum_now
from prefect import task
from prefect.artifacts import create_markdown_artifact

from gaming_pipeline.config import settings
from gaming_pipeline.load.pipeline import GamingPipeline

logger = logging.getLogger(__name__)


def exponential_backoff_with_jitter(attempt: int) -> list[float]:
    """Calculate exponential backoff with jitter for retries.

    Args:
        attempt: The attempt number (0-indexed).

    Returns:
        List of delay in seconds.
    """
    base_delay = 30
    max_delay = 300
    delay = min(base_delay * (2**attempt), max_delay)
    jitter = secrets.randbelow(11)
    return [delay + jitter]


@task(
    name="Run Full Pipeline",
    description="Run complete data pipeline",
    retries=1,
    retry_delay_seconds=120,
)
def run_full_pipeline_task(page_size: int = 50, max_pages: int = 10) -> dict[str, Any]:
    """Run complete gaming analytics pipeline (full reload every run).

    Args:
        page_size: Number of items per page.
        max_pages: Maximum number of pages to fetch.

    Returns:
        Dictionary with load statistics and timestamp.
    """
    logger.info(
        "Starting full pipeline execution "
        f"(page_size={page_size}, max_pages={max_pages})"
    )

    pipeline = GamingPipeline()
    result = pipeline.run_full_load(
        page_size=page_size,
        max_pages=max_pages,
    )

    rawg_result = result.get("rawg", {})
    markdown_content = f"""
# Gaming Analytics Pipeline Summary

## Execution Details
- **Pipeline Name**: gaming-analytics
- **Execution Time**: {result.get("timestamp", pendulum_now().isoformat())}
- **Environment**: {"Production" if settings.is_production else "Development"}
- **Load Type**: Full Reload (replace)

## RAWG Data Load Results
- **Total Games**: {rawg_result.get("total_games", 0)}
- **Genres**: {rawg_result.get("genres", 0)}
- **Platforms**: {rawg_result.get("platforms", 0)}

## Performance Notes
- Page Size: {page_size}
- Max Pages: {max_pages}
"""

    create_markdown_artifact(
        key="pipeline-execution-summary",
        markdown=markdown_content,
        description="Comprehensive pipeline execution summary",
    )

    logger.info("Pipeline execution completed successfully")
    return result


@task(name="Get Pipeline Schema", description="Get current pipeline schema information")
def get_pipeline_schema_task() -> dict[str, Any]:
    """Get current pipeline schema.

    Returns:
        Dictionary with pipeline schema information.
    """
    logger.info("Retrieving pipeline schema")

    pipeline = GamingPipeline()
    schema = pipeline.get_schema()

    logger.info("Successfully retrieved pipeline schema")
    return schema


@task(
    name="Get Load Information",
    description="Get information about last pipeline load",
)
def get_load_info_task() -> dict[str, Any]:
    """Get information about last load.

    Returns:
        Dictionary with load information.
    """
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
    """Refresh pipeline schema from destination."""
    logger.info("Refreshing pipeline schema")

    pipeline = GamingPipeline()
    pipeline.refresh_schema()

    logger.info("Pipeline schema refreshed successfully")


@task(
    name="Run SQLMesh Transformations",
    description="Run SQLMesh transformations to create staging and marts",
    retries=2,
    retry_delay_seconds=60,
)
def run_sqlmesh_task() -> dict[str, Any]:
    """Run SQLMesh transformations.

    Returns:
        Dictionary with return code, stdout, and stderr from SQLMesh.
    """
    import subprocess

    logger.info("Starting SQLMesh transformations")

    try:
        result = subprocess.run(  # noqa: S603,S607
            ["sqlmesh", "plan", "--auto-apply"],  # noqa: S603,S607
            capture_output=True,
            text=True,
            timeout=300,
            cwd="sqlmesh",
        )
        returncode = result.returncode
        stdout = result.stdout
        stderr = result.stderr
    except subprocess.TimeoutExpired:
        logger.error("SQLMesh apply timed out")
        return {"returncode": -1, "stdout": "", "stderr": "Timed out"}
    except Exception as e:
        logger.error(f"SQLMesh apply error: {e}")
        return {"returncode": 1, "stdout": "", "stderr": str(e)}

    result = {"returncode": returncode, "stdout": stdout, "stderr": stderr}

    markdown_content = f"""
## SQLMesh Transformations Summary

- **Status**: {"Success" if result.get("returncode") == 0 else "Failed"}
- **Return Code**: {result.get("returncode", "N/A")}
- **Execution Time**: {pendulum_now().isoformat()}
"""

    create_markdown_artifact(
        key="sqlmesh-transformation-summary",
        markdown=markdown_content,
        description="Summary of SQLMesh transformations",
    )

    logger.info(f"SQLMesh transformations completed: {result}")
    return result
