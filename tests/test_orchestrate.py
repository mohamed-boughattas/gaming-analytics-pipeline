"""Tests for orchestrate module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from gaming_pipeline.orchestrate import tasks


@pytest.fixture
def mock_settings(monkeypatch):
    """Mock settings for testing."""
    from gaming_pipeline.config.settings import DatabaseConfig, Settings

    mock_db_config = DatabaseConfig(
        path=":memory:",
        connection_uri="duckdb:///:memory:",
    )

    mock_settings = Settings(
        database=mock_db_config,
    )

    monkeypatch.setattr("gaming_pipeline.config.settings.settings", mock_settings)
    return mock_settings


@pytest.mark.asyncio
class TestTasks:
    """Test Prefect tasks."""

    async def test_extract_rawg_genres_task(self):
        """Test genre extraction task."""
        # Mock the extract function
        with patch(
            "gaming_pipeline.orchestrate.tasks.extract_rawg_genres",
            new_callable=AsyncMock,
            return_value=[{"id": 1, "name": "Action"}],
        ):
            result = await tasks.extract_rawg_genres_task()

            assert isinstance(result, list)
            assert len(result) >= 0

    async def test_extract_rawg_platforms_task(self):
        """Test platform extraction task."""
        # Mock the extract function
        with patch(
            "gaming_pipeline.orchestrate.tasks.extract_rawg_platforms",
            new_callable=AsyncMock,
            return_value=[{"id": 1, "name": "PC"}],
        ):
            result = await tasks.extract_rawg_platforms_task()

            assert isinstance(result, list)
            assert len(result) >= 0

    async def test_load_rawg_data_task(self):
        """Test RAWG data loading task."""
        # Mock the pipeline
        mock_pipeline = MagicMock()
        mock_pipeline.load_rawg_data = AsyncMock(
            return_value={"total_games": 100, "genres": 10, "platforms": 5}
        )

        with patch(
            "gaming_pipeline.orchestrate.tasks.GamingPipeline",
            return_value=mock_pipeline,
        ):
            result = await tasks.load_rawg_data_task(
                page_size=10, max_pages=2, updated_after=None
            )

            assert result is not None
            assert "total_games" in result

    async def test_get_pipeline_schema_task(self):
        """Test getting pipeline schema task."""
        mock_pipeline = MagicMock()
        mock_pipeline.get_schema = MagicMock(return_value={"tables": []})

        with patch(
            "gaming_pipeline.orchestrate.tasks.GamingPipeline",
            return_value=mock_pipeline,
        ):
            result = tasks.get_pipeline_schema_task()

            assert result is not None
            assert isinstance(result, dict)

    async def test_get_load_info_task(self):
        """Test getting load info task."""
        mock_pipeline = MagicMock()
        mock_pipeline.get_load_info = MagicMock(return_value={"load_count": 1})

        with patch(
            "gaming_pipeline.orchestrate.tasks.GamingPipeline",
            return_value=mock_pipeline,
        ):
            result = tasks.get_load_info_task()

            assert result is not None
            assert isinstance(result, dict)

    def test_refresh_schema_task(self):
        """Test refresh schema task."""
        mock_pipeline = MagicMock()
        mock_pipeline.refresh_schema = MagicMock()

        with patch(
            "gaming_pipeline.orchestrate.tasks.GamingPipeline",
            return_value=mock_pipeline,
        ):
            # Should not raise an error
            tasks.refresh_schema_task()

            mock_pipeline.refresh_schema.assert_called_once()
