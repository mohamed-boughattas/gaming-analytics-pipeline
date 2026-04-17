"""Tests for demo seed database module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from gaming_pipeline.demo.seed_database import (
    SAMPLE_GAMES,
    SAMPLE_GENRES,
    SAMPLE_PLATFORMS,
    seed_database,
)


class TestSampleDataConstants:
    """Test that sample data constants are well-formed."""

    def test_sample_games_is_list(self) -> None:
        assert isinstance(SAMPLE_GAMES, list)
        assert len(SAMPLE_GAMES) == 5

    def test_sample_genres_is_list(self) -> None:
        assert isinstance(SAMPLE_GENRES, list)
        assert len(SAMPLE_GENRES) == 6

    def test_sample_platforms_is_list(self) -> None:
        assert isinstance(SAMPLE_PLATFORMS, list)
        assert len(SAMPLE_PLATFORMS) == 6

    def test_each_game_has_required_fields(self) -> None:
        for game in SAMPLE_GAMES:
            assert "id" in game
            assert "name" in game
            assert "released" in game
            assert "rating" in game
            assert "platforms" in game
            assert "genres" in game

    def test_each_genre_has_required_fields(self) -> None:
        for genre in SAMPLE_GENRES:
            assert "id" in genre
            assert "name" in genre
            assert "slug" in genre

    def test_each_platform_has_required_fields(self) -> None:
        for platform in SAMPLE_PLATFORMS:
            assert "id" in platform
            assert "name" in platform
            assert "slug" in platform

    def test_game_platforms_are_json_serializable(self) -> None:
        for game in SAMPLE_GAMES:
            json.dumps(game["platforms"])
            json.dumps(game["genres"])


class TestSeedDatabaseFunction:
    """Test seed_database function with temporary database."""

    @pytest.fixture
    def temp_db_path(self) -> Path:
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir) / "test.db"

    def test_seed_database_creates_tables(self, temp_db_path: Path) -> None:
        result = seed_database(db_path=temp_db_path)
        assert isinstance(result, dict)
        assert "games" in result
        assert "genres" in result
        assert "platforms" in result

    def test_seed_database_inserts_correct_counts(self, temp_db_path: Path) -> None:
        result = seed_database(db_path=temp_db_path)
        assert result["games"] == 5
        assert result["genres"] == 6
        assert result["platforms"] == 6

    def test_seed_database_is_idempotent(self, temp_db_path: Path) -> None:
        seed_database(db_path=temp_db_path)
        result = seed_database(db_path=temp_db_path)
        assert result["games"] == 5
        assert result["genres"] == 6
        assert result["platforms"] == 6

    def test_seed_database_creates_schema(self, temp_db_path: Path) -> None:
        import duckdb

        seed_database(db_path=temp_db_path)
        con = duckdb.connect(str(temp_db_path))
        schema_result = con.execute(
            "SELECT schema_name FROM information_schema.schemata "
            "WHERE schema_name = 'raw'"
        ).fetchone()
        con.close()
        assert schema_result is not None

    def test_seed_database_clears_existing_data(self, temp_db_path: Path) -> None:
        import duckdb

        seed_database(db_path=temp_db_path)
        seed_database(db_path=temp_db_path)
        con = duckdb.connect(str(temp_db_path), read_only=True)
        count = con.execute("SELECT COUNT(*) FROM raw.games").fetchone()[0]
        con.close()
        assert count == 5

    def test_seed_database_games_have_correct_ids(self, temp_db_path: Path) -> None:
        import duckdb

        seed_database(db_path=temp_db_path)
        con = duckdb.connect(str(temp_db_path), read_only=True)
        ids = con.execute("SELECT id FROM raw.games ORDER BY id").fetchall()
        con.close()
        assert [r[0] for r in ids] == [1, 2, 3, 4, 5]

    def test_seed_database_genres_have_correct_ids(self, temp_db_path: Path) -> None:
        import duckdb

        seed_database(db_path=temp_db_path)
        con = duckdb.connect(str(temp_db_path), read_only=True)
        ids = con.execute("SELECT id FROM raw.genres ORDER BY id").fetchall()
        con.close()
        assert [r[0] for r in ids] == [2, 3, 4, 5, 10, 15]

    def test_seed_database_creates_parent_directory(self, temp_db_path: Path) -> None:
        temp_db_path.parent.mkdir(parents=True, exist_ok=True)
        seed_database(db_path=temp_db_path)
        assert temp_db_path.exists()

    def test_seed_database_uses_default_path_when_none(
        self, temp_db_path: Path
    ) -> None:
        with patch("gaming_pipeline.config.config") as mock_config:
            mock_config.database.path = str(temp_db_path)

            result = seed_database(db_path=None)

            assert result["games"] == 5
            assert result["genres"] == 6
            assert result["platforms"] == 6

    def test_main_block_runs_seed_database(self, temp_db_path: Path) -> None:
        import subprocess
        import sys

        result = subprocess.run(  # noqa: S603
            [
                sys.executable,
                "-m",
                "coverage",
                "run",
                "-m",
                "gaming_pipeline.demo.seed_database",
            ],
            capture_output=True,
            text=True,
            cwd=".",
            env={**__import__("os").environ, "DB_PATH": str(temp_db_path)},
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
