"""dlt-based RAWG API source using REST API.

This module provides a dlt source for extracting data from the RAWG API.
Using dlt's built-in REST API source provides:
- Automatic retry with exponential backoff
- Rate limiting support
- Pagination handling
- Schema inference
- Type coercion
"""

from typing import Any

import dlt
from dlt.sources.rest_api import rest_api_source

from gaming_pipeline.config import config

RAWG_FIELDS = {
    "games": [
        "id",
        "name",
        "released",
        "rating",
        "ratings_count",
        "metacritic",
        "platforms",
        "genres",
        "background_image",
        "short_description",
    ],
    "genres": ["id", "name", "slug"],
    "platforms": ["id", "name", "slug"],
}


@dlt.source(
    name="rawg",
    schema_contract={
        "tables": "evolve",
        "columns": "freeze",
    },
)
def rawg_source(
    page_size: int = 20,
    max_pages: int | None = None,
    updated_after: str | None = None,
    include_fields: bool = True,
) -> Any:
    """Create dlt source for extracting data from the RAWG API.

    This function uses dlt's REST API source which provides:
    - Automatic retry with exponential backoff (default 5 retries)
    - Configurable timeout (30 seconds default)
    - Pagination handling
    - Schema inference
    - Type coercion
    - Schema contract for controlled evolution

    Args:
        page_size: Number of items per page (max 100).
        max_pages: Maximum number of pages to fetch per resource. None for all.
        updated_after: ISO date string for incremental loading (e.g., "2024-01-01").
        include_fields: Whether to request only specific fields for games.

    Returns:
        dlt Source configured for RAWG API with games, genres, and platforms.

    Example:
        >>> source = rawg_source(page_size=50, max_pages=10)
        >>> pipeline = dlt.pipeline(
        ...     "gaming_analytics",
        ...     destination=dlt.destinations.duckdb()
        ... )
        >>> pipeline.run(source)
    """
    base_url = config.api.base_url
    headers = {"Accept": "application/json"}

    if config.api.rawg_api_key:
        headers["Authorization"] = f"Bearer {config.api.rawg_api_key}"

    api_key_param = {"key": config.api.rawg_api_key} if config.api.rawg_api_key else {}

    resources: list[dict[str, Any]] = [
        {
            "name": "rawg_games",
            "endpoint": {
                "path": "games",
                "params": {
                    **api_key_param,
                    "page_size": min(page_size, 100),
                    "ordering": "-updated",
                    **({"updated_after": updated_after} if updated_after else {}),
                },
                "response_actions": [
                    {"status_code": 404, "action": "ignore"},
                ],
            },
        },
        {
            "name": "rawg_genres",
            "endpoint": {
                "path": "genres",
                "params": {**api_key_param, "page_size": 100},
                "response_actions": [
                    {"status_code": 404, "action": "ignore"},
                ],
            },
        },
        {
            "name": "rawg_platforms",
            "endpoint": {
                "path": "platforms",
                "params": {**api_key_param, "page_size": 100},
                "response_actions": [
                    {"status_code": 404, "action": "ignore"},
                ],
            },
        },
    ]

    if include_fields:
        for resource in resources:
            if resource["name"] == "rawg_games":
                fields = RAWG_FIELDS["games"]
                resource["endpoint"]["params"]["fields"] = ",".join(fields)

    config_dict: dict[str, Any] = {
        "client": {
            "base_url": base_url,
            "headers": headers,
            "paginator": "page_number",
        },
        "resources": resources,
    }

    if max_pages is not None:
        for resource in config_dict["resources"]:
            resource["endpoint"]["params"]["max_pages"] = max_pages

    return rest_api_source(config_dict)  # type: ignore[arg-type]
