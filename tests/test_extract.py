"""Tests for data extraction module."""

import pytest

from gaming_pipeline.extract.base import DefaultExtractors, ExtractorBundle
from gaming_pipeline.extract.dlt_source import rawg_source


class TestDLTSource:
    """Test dlt RAWG source configuration."""

    def test_rawg_source_creation(self):
        """Test basic source creation."""
        source = rawg_source(page_size=20, max_pages=5)
        assert source is not None
        # The source name may be 'rawg' or 'rest_api' depending on dlt version
        assert source.name in ("rawg", "rest_api")

    def test_rawg_source_with_updated_after(self):
        """Test source creation with incremental loading."""
        source = rawg_source(page_size=50, max_pages=10, updated_after="2024-01-01")
        assert source is not None
        assert source.name in ("rawg", "rest_api")

    def test_rawg_source_page_size_parameter(self):
        """Test source respects page_size parameter."""
        source = rawg_source(page_size=50)
        assert source is not None
        # Just verify it can be created with custom page_size

    def test_rawg_source_max_pages_parameter(self):
        """Test source accepts max_pages parameter."""
        source = rawg_source(max_pages=3)
        assert source is not None


class TestExtractorBundle:
    """Test ExtractorBundle protocol and DefaultExtractors."""

    def test_default_extractors_is_extractor_bundle(self):
        """Test DefaultExtractors implements ExtractorBundle."""
        extractors = DefaultExtractors()
        assert isinstance(extractors, ExtractorBundle)

    def test_extractor_bundle_has_extract_genres_method(self):
        """Test ExtractorBundle has extract_genres method."""
        extractors = DefaultExtractors()
        assert hasattr(extractors, "extract_genres")
        assert callable(extractors.extract_genres)

    def test_extractor_bundle_has_extract_platforms_method(self):
        """Test ExtractorBundle has extract_platforms method."""
        extractors = DefaultExtractors()
        assert hasattr(extractors, "extract_platforms")
        assert callable(extractors.extract_platforms)


@pytest.mark.asyncio
class TestMockExtractors:
    """Test mock extractors for unit testing."""

    async def test_mock_rawg_extractor(self, mock_rawg_extractor):
        """Test mock RAWG extractor."""
        # Test genres
        genres = await mock_rawg_extractor.extract_genres()
        assert len(genres) == 2
        assert genres[0]["name"] == "Action"

        # Test platforms
        platforms = await mock_rawg_extractor.extract_platforms()
        assert len(platforms) == 2
        assert platforms[0]["name"] == "PC"
