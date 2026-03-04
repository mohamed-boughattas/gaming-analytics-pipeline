"""Data extraction module for gaming analytics pipeline."""

from .rawg import (
    Game,
    RAWGExtractor,
    extract_rawg_games,
    extract_rawg_genres,
    extract_rawg_platforms,
)

__all__ = [
    "Game",
    "RAWGExtractor",
    "extract_rawg_games",
    "extract_rawg_genres",
    "extract_rawg_platforms",
]
