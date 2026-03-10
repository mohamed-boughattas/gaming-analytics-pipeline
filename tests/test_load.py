"""Tests for load module - simplified for dlt source."""

import pytest

from gaming_pipeline.load.pipeline import GamingPipeline


@pytest.fixture
def mock_settings(monkeypatch):
    """Mock settings for testing."""
    from gaming_pipeline.config.settings import APIConfig, DatabaseConfig, Settings

    mock_db_config = DatabaseConfig(
        path=":memory:",
        connection_string="duckdb:///:memory:",
    )
    mock_api_config = APIConfig()
    mock_settings = Settings(database=mock_db_config, api=mock_api_config)

    # Directly set the test values
    mock_db_config.path = ":memory:"
    mock_api_config.api_key = "test_key"

    yield mock_settings


@pytest.mark.asyncio
class TestGamingPipeline:
    """Test GamingPipeline class."""

    async def test_pipeline_creation(self, mock_settings):
        """Test pipeline can be created."""
        # Just test that we can create a pipeline without errors
        pipeline = GamingPipeline()
        assert pipeline is not None
        assert pipeline.dataset_name == "gaming_analytics"

    async def test_get_load_info_when_empty(self, mock_settings):
        """Test getting load info when no loads have happened."""
        pipeline = GamingPipeline()
        # This should not raise an exception even if no load has happened
        info = pipeline.get_load_info()
        # Should return empty dict or valid result
        assert info is not None

    async def test_get_schema_when_empty(self, mock_settings):
        """Test getting schema when no loads have happened."""
        pipeline = GamingPipeline()
        # This should not raise an exception even if no load has happened
        schema = pipeline.get_schema()
        # Should return empty dict or valid result
        assert schema is not None
