"""Soda Core configuration for gaming analytics pipeline."""

from pathlib import Path
from typing import Any

from gaming_pipeline.config import config


class SodaConfiguration:
    """Soda Core configuration manager."""

    def __init__(self):
        self.config_file = config.soda.configuration_file
        self.checks_path = Path(config.soda.checks_path)
        self.data_source_name = "gaming_analytics"

    def get_data_source_config(self) -> dict[str, Any]:
        """Get data source configuration."""
        return {
            "data_source": {
                "gaming_analytics": {
                    "type": "duckdb",
                    "path": str(config.database.path),
                }
            }
        }

    def get_default_variables(self) -> dict[str, Any]:
        """Get default variables for Soda checks."""
        return {
            "schema": "main",
            "table_prefix": "rawg_",
            "date_column": "released",
            "rating_column": "rating",
            "id_column": "id",
        }

    def get_check_paths(self) -> dict[str, str]:
        """Get paths to different check files."""
        return {
            "staging": str(self.checks_path / "staging.yml"),
            "marts": str(self.checks_path / "marts.yml"),
            "all": str(self.checks_path),
        }


# Global configuration instance
soda_config = SodaConfiguration()
