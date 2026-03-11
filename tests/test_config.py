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
        assert config.type == "duckdb"

    def test_connection_uri_from_path(self):
        """Test connection URI is derived from path."""
        config = DatabaseConfig(path="data/test.duckdb")
        assert config.connection_uri == "duckdb:///data/test.duckdb"

    def test_connection_uri_from_string(self):
        """Test connection URI uses explicit value when provided."""
        config = DatabaseConfig(connection_string="duckdb:///:memory:")
        assert config.connection_uri == "duckdb:///:memory:"


class TestAPIConfig:
    """Test APIConfig class."""

    def test_default_base_url(self):
        """Test default RAWG API URL."""
        config = APIConfig()
        assert config.base_url == "https://api.rawg.io/api"

    def test_rawg_api_key_property_no_key(self):
        """Test rawg_api_key property returns None when no key."""
        config = APIConfig()
        assert config.rawg_api_key is None

    def test_rawg_headers_without_key(self):
        """Test headers without API key."""
        config = APIConfig()
        headers = config.rawg_headers
        assert headers == {"Accept": "application/json"}
        assert "Authorization" not in headers


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

    def test_default_paths(self):
        """Test default Soda configuration paths."""
        config = SodaConfig()
        assert config.checks_path == "src/gaming_pipeline/quality/checks"
        assert (
            config.configuration_file == "src/gaming_pipeline/quality/configuration.yml"
        )


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
