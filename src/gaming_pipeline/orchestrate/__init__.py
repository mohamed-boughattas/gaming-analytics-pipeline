"""Orchestration module for gaming analytics pipeline."""

from .flows import (
    create_all_deployments,
    create_daily_deployment,
    create_extract_only_deployment,
    create_full_load_deployment,
    create_load_only_deployment,
    daily_pipeline_flow,
    deploy_all,
    extract_only_flow,
    full_load_pipeline_flow,
    load_only_flow,
    run_daily_pipeline,
    run_extract_only_pipeline,
    run_full_load_pipeline,
    run_load_only_pipeline,
)
from .tasks import (
    extract_rawg_genres_task,
    extract_rawg_platforms_task,
    get_load_info_task,
    get_pipeline_schema_task,
    load_rawg_data_task,
    load_steam_data_task,
    refresh_schema_task,
    run_full_pipeline_task,
)

__all__ = [
    # Flows
    "daily_pipeline_flow",
    "full_load_pipeline_flow",
    "extract_only_flow",
    "load_only_flow",
    "create_daily_deployment",
    "create_full_load_deployment",
    "create_extract_only_deployment",
    "create_load_only_deployment",
    "create_all_deployments",
    "deploy_all",
    "run_daily_pipeline",
    "run_full_load_pipeline",
    "run_extract_only_pipeline",
    "run_load_only_pipeline",
    # Tasks
    "extract_rawg_genres_task",
    "extract_rawg_platforms_task",
    "load_rawg_data_task",
    "load_steam_data_task",
    "run_full_pipeline_task",
    "get_pipeline_schema_task",
    "get_load_info_task",
    "refresh_schema_task",
]
