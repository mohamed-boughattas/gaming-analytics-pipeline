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

    Note: This implementation returns empty lists because dlt sources are
    designed to be run via pipeline.run(), not directly iterated. For actual
    data extraction, use GamingPipeline.load_rawg_data() which handles
    the full extract-load process.
    """

    async def extract_genres(self) -> list[dict[str, Any]]:
        """Extract genre data using dlt source.

        Returns empty list - use GamingPipeline.load_rawg_data() instead.
        """
        return []

    async def extract_platforms(self) -> list[dict[str, Any]]:
        """Extract platform data using dlt source.

        Returns empty list - use GamingPipeline.load_rawg_data() instead.
        """
        return []
