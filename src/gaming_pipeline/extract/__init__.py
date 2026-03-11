"""Data extraction module for gaming analytics pipeline."""

from .base import DefaultExtractors
from .dlt_source import rawg_source

__all__ = [
    "rawg_source",
    "DefaultExtractors",
]
