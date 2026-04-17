"""Tests for configuration settings module."""

import pytest

from gaming_pipeline.config.settings import (
    APIConfig,
    DatabaseConfig,
    PipelineConfig,
    Settings,
    SodaConfig,
)


class TestDatabaseConfig:
    """Test DatabaseConfig class."""

    def test_default_path(self):
        """Test default database path."""
        config = DatabaseConfig()
        assert config.path == "data/gaming_analytics.duckdb"

    def test_connection_uri(self):
        """Test connection URI uses duckdb scheme."""
        config = DatabaseConfig(path="data/test.duckdb")
        assert config.connection_uri == "duckdb:///data/test.duckdb"


class TestAPIConfig:
    """Test APIConfig class."""

    def test_default_base_url(self):
        """Test default RAWG API URL."""
        config = APIConfig()
        assert config.base_url == "https://api.rawg.io/api"

    def test_rawg_api_key_property_no_key(self, monkeypatch):
        """Test rawg_api_key property returns None when no key."""
        monkeypatch.delenv("RAWG_API_KEY", raising=False)
        config = APIConfig(api_key=None)
        assert config.rawg_api_key is None


class TestPipelineConfig:
    """Test PipelineConfig class."""

    def test_default_values(self):
        """Test default pipeline configuration."""
        config = PipelineConfig()
        assert config.batch_size == 100
        assert config.max_retries == 3
        assert config.retry_delay == 5
        assert config.parallel_requests == 5
        assert config.data_retention_days == 365


class TestSodaConfig:
    """Test SodaConfig class."""

    def test_default_checks_path(self):
        """Test default Soda checks path."""
        config = SodaConfig()
        assert config.checks_path == "src/gaming_pipeline/quality/checks"


class TestSettings:
    """Test main Settings class."""

    def test_default_environment(self):
        """Test default environment is development."""
        settings = Settings()
        assert settings.environment == "development"

    def test_environment_case_insensitive(self):
        """Test environment is normalized to lowercase."""
        settings = Settings(environment="PRODUCTION")
        assert settings.environment == "production"

    def test_is_production_property(self):
        """Test is_production property."""
        settings = Settings(environment="production")
        assert settings.is_production is True

    def test_is_development_property(self):
        """Test is_development property."""
        settings = Settings(environment="development")
        assert settings.is_development is True

    def test_validate_environment_rejects_invalid(self):
        """Test environment validator rejects invalid values."""
        with pytest.raises(ValueError) as exc_info:
            Settings(environment="invalid")
        assert "Environment must be one of" in str(exc_info.value)

    def test_validate_environment_accepts_valid(self):
        """Test environment validator accepts all valid values."""
        for env in ["development", "production", "test"]:
            settings = Settings(environment=env)
            assert settings.environment == env

    def test_database_config_is_factory(self):
        """Test database config uses factory."""
        settings = Settings()
        assert isinstance(settings.database, DatabaseConfig)

    def test_api_config_is_factory(self):
        """Test api config uses factory."""
        settings = Settings()
        assert isinstance(settings.api, APIConfig)
