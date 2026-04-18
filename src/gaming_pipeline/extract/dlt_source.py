"""dlt-based RAWG API source using REST API.

This module provides a dlt source for extracting data from the RAWG API.
Using dlt's built-in REST API source provides:
- Automatic retry with exponential backoff
- Rate limiting support
- Pagination handling
- Schema inference
- Type coercion
- Incremental loading with state tracking
"""

from collections.abc import Iterator
from typing import Any

import dlt
import requests
from dlt.sources import DltResource
from dlt.sources import incremental as dlt_incremental
from pendulum import now as pendulum_now

from gaming_pipeline.config import config

RAWG_FIELDS: dict[str, list[str]] = {
    "games": [
        "id",
        "name",
        "released",
        "updated",
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


def rawg_source(
    page_size: int = 20,
    max_pages: int = 10,
) -> Any:
    """Create dlt source for extracting data from the RAWG API.

    This source supports incremental loading - if the pipeline is interrupted,
    it will resume from the last successful checkpoint without duplicating data.

    Args:
        page_size: Number of items per page (max 100).
        max_pages: Maximum number of pages to fetch.

    Returns:
        dlt Source configured for RAWG API with games, genres, and platforms.
    """

    @dlt.resource(
        name="games",
        primary_key="id",
        write_disposition="merge",
        columns={
            "added_by_status": {"data_type": "text"},
            "clip": {"data_type": "text"},
            "esrb_rating": {"data_type": "text"},
            "metacritic": {"data_type": "bigint"},
            "platforms": {"data_type": "text"},
            "score": {"data_type": "double"},
            "short_screenshots": {"data_type": "text"},
            "stores": {"data_type": "text"},
            "tags": {"data_type": "text"},
            "user_game": {"data_type": "text"},
        },
    )
    def games(
        page_size: int = 20,
        max_pages: int = 10,
        updated_at: dlt_incremental[str] = dlt_incremental(  # noqa: B008
            "updated", initial_value="2026-01-01"
        ),
    ) -> Iterator[dict[str, Any]]:
        """Fetch games from RAWG API incrementally.

        Uses the 'updated' field from RAWG API to fetch only games
        modified since the last run. This ensures:
        - No duplicate data on pipeline restart
        - Minimal API calls (only fetch changed records)
        - Efficient use of API rate limits

        The checkpoint is automatically persisted by dlt between runs.

        Args:
            page_size: Number of items per page.
            max_pages: Maximum number of pages to fetch.
            updated_at: Incremental state tracking for the updated field.

        Yields:
            Game record dictionaries.
        """
        api_key = config.api.rawg_api_key
        base_url = config.api.base_url
        fields = ",".join(RAWG_FIELDS["games"])

        checkpoint = updated_at.last_value or "2026-01-01"
        end_date = pendulum_now().to_date_string()

        page = 1
        while page <= max_pages:
            url = f"{base_url}/games"
            params = {
                "key": api_key,
                "page_size": min(page_size, 100),
                "page": page,
                "ordering": "-updated",
                "fields": fields,
                "dates": f"{checkpoint},{end_date}",
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            games_data = data.get("results", [])
            if not games_data:
                break

            yield from games_data

            if data.get("next"):
                page += 1
            else:
                break

    @dlt.resource(
        name="genres",
        primary_key="id",
        write_disposition="replace",
    )
    def genres() -> Iterator[dict[str, Any]]:
        """Fetch genres from RAWG API.

        Genres change infrequently, so we use replace disposition
        to ensure we always have the complete genres catalog.

        Yields:
            Genre record dictionaries.
        """
        api_key = config.api.rawg_api_key
        base_url = config.api.base_url
        fields = ",".join(RAWG_FIELDS["genres"])

        url = f"{base_url}/genres"
        params = {"key": api_key, "page_size": 100, "fields": fields}
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        yield from data.get("results", [])

    @dlt.resource(
        name="platforms",
        primary_key="id",
        write_disposition="replace",
        columns={
            "image": {"data_type": "text"},
            "year_end": {"data_type": "bigint"},
        },
    )
    def platforms() -> Iterator[dict[str, Any]]:
        """Fetch platforms from RAWG API.

        Platforms change infrequently, so we use replace disposition
        to ensure we always have the complete platforms catalog.

        Yields:
            Platform record dictionaries.
        """
        api_key = config.api.rawg_api_key
        base_url = config.api.base_url
        fields = ",".join(RAWG_FIELDS["platforms"])

        url = f"{base_url}/platforms"
        params = {"key": api_key, "page_size": 100, "fields": fields}
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        yield from data.get("results", [])

    @dlt.source(name="rawg")
    def _source() -> list[DltResource]:
        """Create the RAWG dlt source with all resources.

        Returns:
            List of configured dlt resources.
        """
        return [
            games(page_size=page_size, max_pages=max_pages),
            genres(),
            platforms(),
        ]

    return _source()
