"""Configuration settings for gaming analytics pipeline."""

from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(Path(".env"))


class DatabaseConfig(BaseSettings):
    """Database configuration using local DuckDB."""

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        extra="ignore",
        env_file=None,
    )

    path: str = "data/gaming_analytics.duckdb"

    @property
    def connection_uri(self) -> str:
        """Get connection URI for DuckDB.

        Returns:
            A duckdb:/// connection URI string.
        """
        return f"duckdb:///{self.path}"


class APIConfig(BaseSettings):
    """API configuration."""

    model_config = SettingsConfigDict(
        env_prefix="RAWG_",
        extra="ignore",
    )

    api_key: str | None = Field(default=None)
    base_url: str = "https://api.rawg.io/api"

    @property
    def rawg_api_key(self) -> str | None:
        """Get RAWG API key.

        Returns:
            The configured RAWG API key or None.
        """
        return self.api_key


class PipelineConfig(BaseSettings):
    """Pipeline configuration."""

    model_config = SettingsConfigDict(
        env_prefix="PIPELINE_",
        extra="ignore",
        env_file=None,
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
        env_file=None,
    )

    checks_path: str = "src/gaming_pipeline/quality/checks"


class Settings(BaseSettings):
    """Main settings class using Pydantic Settings."""

    model_config = SettingsConfigDict(
        env_file=Path(".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: str = "development"

    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    pipeline: PipelineConfig = Field(default_factory=PipelineConfig)
    soda: SodaConfig = Field(default_factory=SodaConfig)

    @property
    def is_production(self) -> bool:
        """Check if running in production environment.

        Returns:
            True if environment is production.
        """
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment.

        Returns:
            True if environment is development.
        """
        return self.environment.lower() == "development"

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value.

        Args:
            v: The environment value to validate.

        Returns:
            The validated lowercase environment string.

        Raises:
            ValueError: If environment is not one of development, production, or test.
        """
        allowed = ["development", "production", "test"]
        v_lower = v.lower()
        if v_lower not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v_lower


settings: Settings = Settings()
