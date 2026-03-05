"""Configuration module for the gaming analytics pipeline."""

from .settings import (
    APIConfig,
    DatabaseConfig,
    PipelineConfig,
    Settings,
    SodaConfig,
    settings,
)

# Maintain backward compatibility with old name
config = settings

__all__ = [
    "config",
    "settings",
    "Settings",
    "DatabaseConfig",
    "APIConfig",
    "PipelineConfig",
    "SodaConfig",
]
