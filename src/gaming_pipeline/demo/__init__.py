"""Demo utilities for gaming analytics pipeline.

This module provides demo functionality including sample data seeding
for testing and evaluation without requiring API keys.
"""

from .seed_database import seed_database

__all__ = ["seed_database"]
