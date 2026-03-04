"""Configuration settings for the gaming analytics pipeline."""

import os

from pydantic import BaseModel, Field


class DatabaseConfig(BaseModel):
    """Database configuration."""

    type: str = "duckdb"
    path: str = "data/gaming_analytics.duckdb"
    connection_string: str | None = None

    @property
    def connection_uri(self) -> str:
        """Get connection URI for DuckDB."""
        if self.connection_string:
            return self.connection_string
        return f"duckdb:///{self.path}"


class APIConfig(BaseModel):
    """API configuration."""

    rawg_api_key: str | None = Field(default=None)
    rawg_base_url: str = "https://api.rawg.io/api"

    @property
    def rawg_headers(self) -> dict:
        """Get RAWG API headers."""
        headers = {"Accept": "application/json"}
        if self.rawg_api_key:
            headers["Authorization"] = f"Bearer {self.rawg_api_key}"
        return headers


class PipelineConfig(BaseModel):
    """Pipeline configuration."""

    batch_size: int = 100
    max_retries: int = 3
    retry_delay: int = 5
    parallel_requests: int = 5
    data_retention_days: int = 365


class SodaConfig(BaseModel):
    """Soda Core configuration."""

    checks_path: str = "src/gaming_pipeline/quality/checks"
    configuration_file: str = "src/gaming_pipeline/quality/configuration.yml"


class Config:
    """Main configuration class."""

    def __init__(self):
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.pipeline = PipelineConfig()
        self.soda = SodaConfig()

        # Load environment variables
        self._load_env_vars()

    def _load_env_vars(self):
        """Load configuration from environment variables."""
        # Database
        if db_path := os.getenv("DUCKDB_PATH"):
            self.database.path = db_path

        # API
        if rawg_key := os.getenv("RAWG_API_KEY"):
            self.api.rawg_api_key = rawg_key

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return os.getenv("ENVIRONMENT", "development").lower() == "production"


# Global configuration instance
config = Config()
