"""Tests for SQLMesh transformations."""

from pathlib import Path

import pytest

SQLMESH_MODELS = Path("sqlmesh/models")


class TestFctGamesModel:
    """Test fct_games.sql model has correct transformation logic."""

    @pytest.fixture
    def fct_games_content(self) -> str:
        return (SQLMESH_MODELS / "marts/fct_games.sql").read_text()

    def test_has_rating_category_case_statement(self, fct_games_content: str) -> None:
        assert "rating_category" in fct_games_content
        assert "CASE" in fct_games_content.upper()
        assert "Excellent" in fct_games_content
        assert "Good" in fct_games_content
        assert "Average" in fct_games_content

    def test_rating_category_thresholds_are_correct(
        self, fct_games_content: str
    ) -> None:
        assert (
            "rating >= 4.5" in fct_games_content or "rating>=4.5" in fct_games_content
        )
        assert (
            "rating >= 3.5" in fct_games_content or "rating>=3.5" in fct_games_content
        )

    def test_has_engagement_score(self, fct_games_content: str) -> None:
        assert "engagement_score" in fct_games_content
        assert "COALESCE" in fct_games_content.upper()

    def test_has_release_year_extraction(self, fct_games_content: str) -> None:
        assert "release_year" in fct_games_content
        assert (
            "STRFTIME" in fct_games_content.upper()
            or "YEAR" in fct_games_content.upper()
        )

    def test_uses_staging_source(self, fct_games_content: str) -> None:
        assert "staging.stg_games" in fct_games_content

    def test_has_try_cast_for_release_year_and_month(
        self, fct_games_content: str
    ) -> None:
        assert "TRY_CAST" in fct_games_content.upper()
        assert "release_year" in fct_games_content.lower()
        assert "release_month" in fct_games_content.lower()

    def test_is_sqlmesh_model(self, fct_games_content: str) -> None:
        assert "MODEL (" in fct_games_content or "MODEL(" in fct_games_content


class TestFctGenresModel:
    """Test fct_genres.sql has real aggregations."""

    @pytest.fixture
    def fct_genres_content(self) -> str:
        return (SQLMESH_MODELS / "marts/fct_genres.sql").read_text()

    def test_has_group_by(self, fct_genres_content: str) -> None:
        assert "GROUP BY" in fct_genres_content.upper()

    def test_has_avg_rating_aggregation(self, fct_genres_content: str) -> None:
        assert "avg_rating" in fct_genres_content.lower()

    def test_has_total_games_count(self, fct_genres_content: str) -> None:
        assert "total_games" in fct_genres_content.lower()

    def test_uses_staging_games_json_explode(self, fct_genres_content: str) -> None:
        assert "staging.stg_games" in fct_genres_content
        assert "genres" in fct_genres_content.lower()
        assert (
            "json_each" in fct_genres_content.lower()
            or "unnest" in fct_genres_content.lower()
        )


class TestFctPlatformsModel:
    """Test fct_platforms.sql has real aggregations."""

    @pytest.fixture
    def fct_platforms_content(self) -> str:
        return (SQLMESH_MODELS / "marts/fct_platforms.sql").read_text()

    def test_has_group_by(self, fct_platforms_content: str) -> None:
        assert "GROUP BY" in fct_platforms_content.upper()

    def test_has_avg_rating_aggregation(self, fct_platforms_content: str) -> None:
        assert "avg_rating" in fct_platforms_content.lower()

    def test_has_total_games_count(self, fct_platforms_content: str) -> None:
        assert "total_games" in fct_platforms_content.lower()

    def test_uses_staging_games_json_explode(self, fct_platforms_content: str) -> None:
        assert "staging.stg_games" in fct_platforms_content
        assert "platforms" in fct_platforms_content.lower()
        assert (
            "json_each" in fct_platforms_content.lower()
            or "unnest" in fct_platforms_content.lower()
        )


class TestStagingModels:
    """Test staging models have type casting."""

    @pytest.fixture
    def stg_games_content(self) -> str:
        return (SQLMESH_MODELS / "staging/stg_games.sql").read_text()

    def test_stg_games_has_try_cast(self, stg_games_content: str) -> None:
        assert "TRY_CAST" in stg_games_content.upper()

    def test_stg_games_has_released_column(self, stg_games_content: str) -> None:
        assert "released" in stg_games_content.lower()

    def test_stg_games_has_rating_column(self, stg_games_content: str) -> None:
        assert "rating" in stg_games_content.lower()

    def test_stg_games_has_genres_and_platforms_json(
        self, stg_games_content: str
    ) -> None:
        assert "genres" in stg_games_content.lower()
        assert "platforms" in stg_games_content.lower()

    def test_is_sqlmesh_model(self, stg_games_content: str) -> None:
        assert "MODEL (" in stg_games_content or "MODEL(" in stg_games_content
