"""Data extraction module for gaming analytics pipeline."""

from .base import DefaultExtractors
from .dlt_source import rawg_source

# For backwards compatibility
extract_rawg_genres = DefaultExtractors().extract_genres
extract_rawg_platforms = DefaultExtractors().extract_platforms

__all__ = [
    "rawg_source",
    "DefaultExtractors",
    "extract_rawg_genres",
    "extract_rawg_platforms",
]
