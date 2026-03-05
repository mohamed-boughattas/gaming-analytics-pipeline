"""Tests for SQLMesh transformations - simplified smoke tests."""

from pathlib import Path


def test_staging_tables_exist():
    """Test that staging SQL files exist."""
    staging_dir = Path("src/gaming_pipeline/transform/staging")

    sql_files = list(staging_dir.glob("*.sql"))
    assert len(sql_files) >= 2  # At least games and genres

    # Check specific tables
    assert (staging_dir / "stg_games.sql").exists()
    assert (staging_dir / "stg_genres.sql").exists()


def test_mart_tables_exist():
    """Test that mart SQL files exist."""
    marts_dir = Path("src/gaming_pipeline/transform/marts")

    sql_files = list(marts_dir.glob("*.sql"))
    assert len(sql_files) >= 2  # At least games and genres

    # Check specific tables
    assert (marts_dir / "games.sql").exists()
    assert (marts_dir / "genres.sql").exists()


def test_sql_files_are_not_empty():
    """Test that SQL files contain actual SQL code."""
    marts_dir = Path("src/gaming_pipeline/transform/marts")

    for sql_file in marts_dir.glob("*.sql"):
        content = sql_file.read_text()
        assert len(content) > 100  # Should have substantial SQL
        assert "SELECT" in content.upper() or "MODEL" in content.upper()
