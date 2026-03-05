"""Configuration settings for the gaming analytics pipeline."""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    """Database configuration."""

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        extra="ignore",
    )

    type: str = "duckdb"
    path: str = "data/gaming_analytics.duckdb"
    connection_string: str | None = None

    @property
    def connection_uri(self) -> str:
        """Get connection URI for DuckDB."""
        if self.connection_string:
            return self.connection_string
        return f"duckdb:///{self.path}"


class APIConfig(BaseSettings):
    """API configuration."""

    model_config = SettingsConfigDict(
        env_prefix="RAWG_",
        extra="ignore",
    )

    api_key: str | None = Field(default=None, alias="API_KEY")
    base_url: str = "https://api.rawg.io/api"

    @property
    def rawg_api_key(self) -> str | None:
        """Get RAWG API key."""
        return self.api_key

    @property
    def rawg_headers(self) -> dict:
        """Get RAWG API headers."""
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers


class PipelineConfig(BaseSettings):
    """Pipeline configuration."""

    model_config = SettingsConfigDict(
        env_prefix="PIPELINE_",
        extra="ignore",
    )

    batch_size: int = 100
    max_retries: int = 3
    retry_delay: int = 5
    parallel_requests: int = 5
    data_retention_days: int = 365


class SodaConfig(BaseSettings):
    """Soda Core configuration."""

    model_config = SettingsConfigDict(
        env_prefix="SODA_",
        extra="ignore",
    )

    checks_path: str = "src/gaming_pipeline/quality/checks"
    configuration_file: str = "src/gaming_pipeline/quality/configuration.yml"


class Settings(BaseSettings):
    """Main settings class using Pydantic Settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment
    environment: str = "development"

    # Component configs
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    pipeline: PipelineConfig = Field(default_factory=PipelineConfig)
    soda: SodaConfig = Field(default_factory=SodaConfig)

    # Additional environment variables (for compatibility)
    database_path: str | None = Field(default=None, alias="DATABASE_PATH")
    motherduck_token: str | None = Field(default=None, alias="MOTHERDUCK_TOKEN")
    prefect_api_url: str | None = Field(default=None, alias="PREFECT_API_URL")

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = ["development", "production", "test"]
        v_lower = v.lower()
        if v_lower not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v_lower


# Global settings instance
settings = Settings()
