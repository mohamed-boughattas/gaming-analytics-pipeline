"""Prefect flows for gaming analytics pipeline."""

from typing import Any

from pendulum import now as pendulum_now
from prefect import flow, get_run_logger

from gaming_pipeline.orchestrate.tasks import (
    get_load_info_task,
    get_pipeline_schema_task,
    refresh_schema_task,
    run_full_pipeline_task,
    run_sqlmesh_task,
)


@flow(
    name="gaming-analytics-pipeline",
    description="Full load pipeline for gaming analytics",
    log_prints=True,
)
def pipeline_flow(
    page_size: int = 50,
    max_pages: int = 10,
) -> dict[str, Any]:
    """Run full load pipeline for gaming analytics (full reload every run).

    Loads data from RAWG API and transforms with SQLMesh.

    Args:
        page_size: Number of items per page (max 100).
        max_pages: Maximum number of pages to fetch.

    Returns:
        Dictionary with pipeline results.
    """
    logger = get_run_logger()
    logger.info("Starting gaming analytics pipeline")

    load_result = run_full_pipeline_task(
        page_size=page_size,
        max_pages=max_pages,
    )

    sqlmesh_result = run_sqlmesh_task()
    if sqlmesh_result.get("returncode", 0) != 0:
        logger.error(f"SQLMesh transformation failed: {sqlmesh_result}")
        raise ValueError(f"SQLMesh transformation failed: {sqlmesh_result}")

    schema = get_pipeline_schema_task()
    load_info = get_load_info_task()
    refresh_schema_task()

    final_result = {
        "pipeline_result": load_result,
        "sqlmesh_result": sqlmesh_result,
        "schema": schema,
        "load_info": load_info,
        "execution_time": pendulum_now().isoformat(),
    }

    logger.info("Pipeline completed successfully")
    return final_result
