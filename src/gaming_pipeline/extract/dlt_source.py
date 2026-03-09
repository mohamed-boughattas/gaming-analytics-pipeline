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
from dlt.sources.rest_api import RESTAPIConfig, rest_api_source

from gaming_pipeline.config import config


@dlt.source(name="rawg")
def rawg_source(
    page_size: int = 20,
    max_pages: int | None = None,
    updated_after: str | None = None,
) -> Any:
    """Create dlt source for RAWG API.

    Args:
        page_size: Number of items per page (max 100).
        max_pages: Maximum number of pages to fetch. None for all.
        updated_after: ISO date string for incremental loading (e.g., "2024-01-01").

    Returns:
        dlt Source configured for RAWG API with games, genres, and platforms.

    Example:
        >>> source = rawg_source(page_size=50, max_pages=10)
        >>> pipeline.run(source)
    """
    base_url = config.api.base_url
    headers = {"Accept": "application/json"}

    # Add API key if available
    if config.api.rawg_api_key:
        headers["Authorization"] = f"Bearer {config.api.rawg_api_key}"

    # Configure the REST API source
    config_dict: RESTAPIConfig = {
        "client": {
            "base_url": base_url,
            "headers": headers,
        },
        "resources": [
            {
                "name": "rawg_games",
                "endpoint": {
                    "path": "games",
                    "params": {
                        "page_size": min(page_size, 100),
                        "ordering": "-updated",
                        **({"updated_after": updated_after} if updated_after else {}),
                    },
                },
            },
            {
                "name": "rawg_genres",
                "endpoint": {
                    "path": "genres",
                    "params": {"page_size": 100},
                },
            },
            {
                "name": "rawg_platforms",
                "endpoint": {
                    "path": "platforms",
                    "params": {"page_size": 100},
                },
            },
        ],
    }

    # Add pagination configuration
    if max_pages is not None:
        config_dict["client"]["paginator"] = "page_number"

    return rest_api_source(config_dict)
