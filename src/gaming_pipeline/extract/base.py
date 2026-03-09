"""Base classes for data extraction.

Note: The extraction logic has been consolidated into dlt_source.py
which uses dlt's built-in REST API source. This module provides
backwards-compatible interface for the orchestration layer.
"""

from abc import ABC, abstractmethod
from typing import Any


class ExtractorBundle(ABC):
    """Protocol for data extractor bundles.

    Note: This interface is maintained for backwards compatibility.
    The actual extraction is now handled by dlt's REST API source
    in dlt_source.py.
    """

    @abstractmethod
    async def extract_genres(self) -> list[dict[str, Any]]:
        """Extract genre data."""
        pass

    @abstractmethod
    async def extract_platforms(self) -> list[dict[str, Any]]:
        """Extract platform data."""
        pass


class DefaultExtractors(ExtractorBundle):
    """Default extractors using dlt REST API source.

    This class provides a simplified interface for the orchestration layer.
    For direct dlt usage, use rawg_source() from dlt_source.py directly.
    """

    async def extract_genres(self) -> list[dict[str, Any]]:
        """Extract genre data using dlt source."""
        from .dlt_source import rawg_source

        source = rawg_source()
        # Access the genres resource and extract data
        genres_data = []
        for resource in source.resources:
            resource_name = getattr(resource, "name", str(resource))
            if resource_name == "rawg_genres":
                for item in resource:
                    genres_data.append(item)
        return genres_data

    async def extract_platforms(self) -> list[dict[str, Any]]:
        """Extract platform data using dlt source."""
        from .dlt_source import rawg_source

        source = rawg_source()
        # Access the platforms resource and extract data
        platforms_data = []
        for resource in source.resources:
            resource_name = getattr(resource, "name", str(resource))
            if resource_name == "rawg_platforms":
                for item in resource:
                    platforms_data.append(item)
        return platforms_data
