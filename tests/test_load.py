"""Tests for load module."""

from unittest.mock import MagicMock, patch

import pytest

from gaming_pipeline.load.pipeline import GamingPipeline, create_pipeline_instance


class TestGamingPipelineInit:
    """Test GamingPipeline initialization."""

    def test_pipeline_has_dataset_name(self) -> None:
        pipeline = GamingPipeline()
        assert pipeline.dataset_name == "raw"

    def test_pipeline_accepts_custom_dataset_name(self) -> None:
        pipeline = GamingPipeline(dataset_name="custom_dataset")
        assert pipeline.dataset_name == "custom_dataset"

    def test_pipeline_has_destination(self) -> None:
        pipeline = GamingPipeline()
        assert hasattr(pipeline, "destination")
        assert pipeline.destination is not None

    def test_pipeline_has_internal_pipeline(self) -> None:
        pipeline = GamingPipeline()
        assert hasattr(pipeline, "pipeline")
        assert pipeline.pipeline is not None

    def test_pipeline_pipeline_name(self) -> None:
        pipeline = GamingPipeline()
        assert pipeline.pipeline.pipeline_name == "gaming_analytics"

    def test_pipeline_accepts_custom_destination(self) -> None:
        pipeline = GamingPipeline.__new__(GamingPipeline)
        pipeline.destination = MagicMock()
        pipeline.dataset_name = "raw"
        assert pipeline.destination is not None


class TestGamingPipelineMethods:
    """Test GamingPipeline public methods."""

    @pytest.fixture
    def pipeline(self) -> GamingPipeline:
        return GamingPipeline()

    def test_get_load_info_returns_trace_or_dict(
        self, pipeline: GamingPipeline
    ) -> None:
        info = pipeline.get_load_info()
        assert info is not None

    def test_get_schema_returns_dict(self, pipeline: GamingPipeline) -> None:
        schema = pipeline.get_schema()
        assert isinstance(schema, dict)

    def test_refresh_schema_does_not_raise(self, pipeline: GamingPipeline) -> None:
        pipeline.refresh_schema()

    @patch("gaming_pipeline.load.pipeline.rawg_source")
    def test_load_rawg_data_returns_stats(
        self, mock_source: MagicMock, pipeline: GamingPipeline
    ) -> None:
        mock_resource = MagicMock()
        mock_resource.run = MagicMock()
        mock_source.return_value = [mock_resource]

        result = pipeline.load_rawg_data(page_size=20, max_pages=1)
        assert isinstance(result, dict)
        assert "total_games" in result
        assert "genres" in result
        assert "platforms" in result

    @patch("gaming_pipeline.load.pipeline.rawg_source")
    def test_load_rawg_data_handles_error(
        self, mock_source: MagicMock, pipeline: GamingPipeline
    ) -> None:
        mock_source.side_effect = Exception("API error")

        result = pipeline.load_rawg_data(page_size=20, max_pages=1)
        assert isinstance(result, dict)
        assert "error" in result

    @patch("gaming_pipeline.load.pipeline.rawg_source")
    def test_run_full_load_returns_timestamp(
        self, mock_source: MagicMock, pipeline: GamingPipeline
    ) -> None:
        mock_resource = MagicMock()
        mock_resource.run = MagicMock()
        mock_source.return_value = [mock_resource]

        result = pipeline.run_full_load(page_size=20, max_pages=1)
        assert isinstance(result, dict)
        assert "timestamp" in result
        assert "rawg" in result

    @patch("gaming_pipeline.load.pipeline.rawg_source")
    def test_run_full_load_handles_error(
        self, mock_source: MagicMock, pipeline: GamingPipeline
    ) -> None:
        mock_source.side_effect = Exception("API error")

        result = pipeline.run_full_load(page_size=20, max_pages=1)
        assert isinstance(result, dict)
        assert "rawg" in result
        assert "error" in result["rawg"]


class TestCreatePipelineInstance:
    """Test create_pipeline_instance convenience function."""

    def test_creates_gaming_pipeline(self) -> None:
        pipeline = create_pipeline_instance()
        assert isinstance(pipeline, GamingPipeline)
        assert pipeline.dataset_name == "raw"
