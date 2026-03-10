"""Configuration module for the gaming analytics pipeline."""

import warnings  # noqa: E402

from .settings import (
    APIConfig,
    DatabaseConfig,
    PipelineConfig,
    Settings,
    SodaConfig,
    settings,
)

# Suppress harmless Pydantic Settings warnings about deprecated config keys
warnings.filterwarnings(  # noqa: E402
    "ignore",
    message=".*pyproject_toml_table_header.*will be ignored.*",
    category=UserWarning,
)
warnings.filterwarnings(  # noqa: E402
    "ignore",
    message=".*toml_file.*will be ignored.*",
    category=UserWarning,
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
