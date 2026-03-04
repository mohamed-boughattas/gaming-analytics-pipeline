"""Tests for data loading module."""

import pytest

from gaming_pipeline.load.pipeline import GamingPipeline


@pytest.mark.asyncio
class TestGamingPipeline:
    """Test GamingPipeline class."""

    def test_pipeline_creation(self, temp_duckdb_path):
        """Test pipeline creation with custom database path."""
        pipeline = GamingPipeline()
        assert pipeline.pipeline is not None
        assert pipeline.dataset_name == "gaming_analytics"

    def test_pipeline_with_custom_destination(self, temp_duckdb_path):
        """Test pipeline creation with custom destination."""
        import dlt

        destination = dlt.destinations.duckdb(credentials=temp_duckdb_path)

        pipeline = GamingPipeline(destination=destination)
        assert pipeline.destination is not None
        assert pipeline.pipeline is not None

    def test_get_schema(self, temp_duckdb_path):
        """Test getting pipeline schema."""
        pipeline = GamingPipeline()
        schema = pipeline.get_schema()
        assert isinstance(schema, dict)

    def test_get_load_info(self, temp_duckdb_path):
        """Test getting load information."""
        pipeline = GamingPipeline()
        load_info = pipeline.get_load_info()
        # load_info returns None if no data has been loaded yet
        assert load_info is None or isinstance(load_info, dict)

    def test_refresh_schema(self, temp_duckdb_path):
        """Test refreshing schema."""
        pipeline = GamingPipeline()
        # Should not raise an exception
        pipeline.refresh_schema()


@pytest.mark.asyncio
class TestGamingPipelineWithMocks:
    """Test GamingPipeline with mocked extractors."""

    async def test_load_rawg_data_with_mocks(
        self, temp_duckdb_path, mock_rawg_extractor
    ):
        """Test loading RAWG data with mocked extractor."""
        # Create pipeline with mocked extractors
        pipeline = GamingPipeline(extractors=mock_rawg_extractor)

        result = await pipeline.load_rawg_data(
            page_size=5, max_pages=2, updated_after=None
        )

        assert isinstance(result, dict)
        assert result["genres"] == 2  # From mock
        assert result["platforms"] == 2  # From mock
        assert result["total_games"] == 2  # From mock

    async def test_run_full_load_with_mocks(
        self, temp_duckdb_path, mock_rawg_extractor
    ):
        """Test running full load with mocked extractors."""
        # Create pipeline with mocked extractors
        pipeline = GamingPipeline(extractors=mock_rawg_extractor)

        result = await pipeline.run_full_load()

        assert isinstance(result, dict)
        assert "rawg" in result
        assert "steam" in result
        assert "timestamp" in result

        # Check RAWG results
        rawg_result = result["rawg"]
        assert rawg_result["genres"] == 2
        assert rawg_result["platforms"] == 2
        assert rawg_result["total_games"] == 2


class TestPipelineUtils:
    """Test pipeline utility functions."""

    def test_create_pipeline_instance(self, temp_duckdb_path):
        """Test creating pipeline instance."""
        from gaming_pipeline.load.pipeline import create_pipeline_instance

        pipeline = create_pipeline_instance()
        assert isinstance(pipeline, GamingPipeline)
