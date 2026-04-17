"""Tests for data extraction module."""

from gaming_pipeline.extract.dlt_source import RAWG_FIELDS, rawg_source


class TestRAWGFields:
    """Test RAWG_FIELDS configuration."""

    def test_rawg_fields_has_games(self) -> None:
        assert "games" in RAWG_FIELDS
        assert len(RAWG_FIELDS["games"]) > 5

    def test_rawg_fields_has_genres(self) -> None:
        assert "genres" in RAWG_FIELDS
        assert "id" in RAWG_FIELDS["genres"]
        assert "name" in RAWG_FIELDS["genres"]

    def test_rawg_fields_has_platforms(self) -> None:
        assert "platforms" in RAWG_FIELDS
        assert "id" in RAWG_FIELDS["platforms"]
        assert "name" in RAWG_FIELDS["platforms"]


class TestRAWGSource:
    """Test RAWG dlt source creation."""

    def test_rawg_source_returns_source_object(self) -> None:
        source = rawg_source(page_size=20, max_pages=5)
        assert source is not None
        assert hasattr(source, "name")

    def test_rawg_source_default_params(self) -> None:
        source = rawg_source()
        assert source is not None

    def test_rawg_source_name_is_rawg(self) -> None:
        source = rawg_source()
        assert source.name == "rawg"


class TestRAWGSourceResourceNames:
    """Test resource names from the source."""

    def test_source_resource_names_include_games(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        assert "games" in source.resources

    def test_source_resource_names_include_genres(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        assert "genres" in source.resources

    def test_source_resource_names_include_platforms(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        assert "platforms" in source.resources

    def test_source_has_three_resources(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        assert len(source.resources) == 3


class TestRAWGSourceResourceMetadata:
    """Test resource metadata by accessing the source's resource descriptions."""

    def test_games_resource_has_merge_disposition(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        games_resource = source.resources["games"]
        assert hasattr(games_resource, "write_disposition")
        assert games_resource.write_disposition == "merge"

    def test_genres_resource_has_replace_disposition(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        genres_resource = source.resources["genres"]
        assert hasattr(genres_resource, "write_disposition")
        assert genres_resource.write_disposition == "replace"

    def test_platforms_resource_has_replace_disposition(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        platforms_resource = source.resources["platforms"]
        assert hasattr(platforms_resource, "write_disposition")
        assert platforms_resource.write_disposition == "replace"

    def test_games_resource_write_disposition_is_merge(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        games_resource = source.resources["games"]
        assert games_resource.write_disposition == "merge"

    def test_genres_resource_write_disposition_is_replace(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        genres_resource = source.resources["genres"]
        assert genres_resource.write_disposition == "replace"

    def test_platforms_resource_write_disposition_is_replace(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        platforms_resource = source.resources["platforms"]
        assert platforms_resource.write_disposition == "replace"

    def test_games_resource_is_callable(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        games_resource = source.resources["games"]
        assert callable(games_resource)

    def test_genres_resource_is_callable(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        genres_resource = source.resources["genres"]
        assert callable(genres_resource)

    def test_platforms_resource_is_callable(self) -> None:
        source = rawg_source(page_size=20, max_pages=2)
        platforms_resource = source.resources["platforms"]
        assert callable(platforms_resource)
