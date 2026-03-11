"""Tests for load module - simplified for dlt source."""

from gaming_pipeline.load.pipeline import GamingPipeline


class TestGamingPipeline:
    """Test GamingPipeline class."""

    def test_pipeline_creation(self):
        """Test pipeline can be created."""
        pipeline = GamingPipeline()
        assert pipeline is not None
        assert pipeline.dataset_name == "gaming_analytics"

    def test_pipeline_custom_dataset_name(self):
        """Test pipeline accepts custom dataset name."""
        pipeline = GamingPipeline(dataset_name="custom_dataset")
        assert pipeline.dataset_name == "custom_dataset"

    def test_get_load_info_returns_dict(self):
        """Test get_load_info returns a dict."""
        pipeline = GamingPipeline()
        info = pipeline.get_load_info()
        assert isinstance(info, dict)

    def test_get_schema_returns_dict(self):
        """Test get_schema returns a dict."""
        pipeline = GamingPipeline()
        schema = pipeline.get_schema()
        assert isinstance(schema, dict)

    def test_refresh_schema_does_not_raise(self):
        """Test refresh_schema handles gracefully."""
        pipeline = GamingPipeline()
        # Should not raise an exception
        pipeline.refresh_schema()

    def test_pipeline_has_pipeline_attribute(self):
        """Test pipeline has internal pipeline object."""
        pipeline = GamingPipeline()
        assert hasattr(pipeline, "pipeline")
        assert pipeline.pipeline is not None

    def test_create_pipeline_instance_function(self):
        """Test convenience function creates pipeline."""
        from gaming_pipeline.load.pipeline import create_pipeline_instance

        pipeline = create_pipeline_instance()
        assert isinstance(pipeline, GamingPipeline)
