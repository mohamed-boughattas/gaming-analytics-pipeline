"""Tests for the load module."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from gaming_pipeline.load.pipeline import GamingPipeline


@pytest.fixture
def mock_settings(monkeypatch):
    """Mock settings for testing."""
    from gaming_pipeline.config import config
    from gaming_pipeline.config.settings import DatabaseConfig, Settings

    mock_db_config = DatabaseConfig(
        path=":memory:",  # In-memory DuckDB
        connection_uri="duckdb:///:memory:",
    )

    mock_settings = Settings(
        database=mock_db_config,
    )

    # Patch the config module's database path
    original_path = config.database.path
    config.database.path = ":memory:"

    yield mock_settings

    # Restore original path
    config.database.path = original_path


@pytest.fixture
def pipeline(mock_settings):
    """Create a test pipeline instance."""
    # Mock the pipeline creation to avoid actual dlt connection
    with pytest.MonkeyPatch().context() as m:
        mock_dlt_pipeline = MagicMock()
        mock_dlt_pipeline.last_trace = None
        mock_dlt_pipeline.default_schema = MagicMock()
        mock_dlt_pipeline.default_schema.to_dict.return_value = {}

        m.setattr("dlt.pipeline", MagicMock(return_value=mock_dlt_pipeline))

        return GamingPipeline()


class TestGamingPipeline:
    """Test GamingPipeline class."""

    def test_pipeline_initialization(self, pipeline):
        """Test pipeline initialization."""
        assert pipeline is not None
        assert pipeline.dataset_name == "gaming_analytics"

    def test_get_load_info_empty(self, pipeline):
        """Test getting load info when no loads have occurred."""
        info = pipeline.get_load_info()
        assert info is not None

    def test_get_schema_empty(self, pipeline):
        """Test getting schema when pipeline is empty."""
        schema = pipeline.get_schema()
        assert schema is not None
        assert isinstance(schema, dict)

    def test_refresh_schema(self, pipeline):
        """Test refreshing schema."""
        # Should not raise an error
        pipeline.refresh_schema()


@pytest.mark.asyncio
class TestGamingPipelineAsync:
    """Test async methods of GamingPipeline."""

    async def test_load_rawg_data_with_empty_response(self, pipeline):
        """Test loading RAWG data with empty extractor response."""
        # Mock extractors to return empty data
        pipeline.extractors.extract_genres = AsyncMock(return_value=[])
        pipeline.extractors.extract_platforms = AsyncMock(return_value=[])

        # Mock extract_games to return an async generator
        async def empty_generator(*args, **kwargs):
            return
            yield  # pragma: no cover

        pipeline.extractors.extract_games = empty_generator

        result = await pipeline.load_rawg_data(
            page_size=10, max_pages=1, updated_after=None
        )

        assert result is not None
        assert "total_games" in result
        assert "genres" in result
        assert "platforms" in result

    async def test_run_full_load(self, pipeline):
        """Test running full load."""
        # Mock extractors
        pipeline.extractors.extract_genres = AsyncMock(return_value=[])
        pipeline.extractors.extract_platforms = AsyncMock(return_value=[])

        # Mock extract_games to return an async generator
        async def empty_generator(*args, **kwargs):
            return
            yield  # pragma: no cover

        pipeline.extractors.extract_games = empty_generator

        result = await pipeline.run_full_load()

        assert result is not None
        assert "rawg" in result
        assert "timestamp" in result
