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


def test_sql_files_have_content():
    """Test that SQL files contain actual SQL code."""
    marts_dir = Path("src/gaming_pipeline/transform/marts")

    for sql_file in marts_dir.glob("*.sql"):
        content = sql_file.read_text()
        # Should have substantial SQL
        assert len(content) > 100
        # Should contain SQL keywords
        content_upper = content.upper()
        assert "SELECT" in content_upper or "MODEL" in content_upper


def test_games_mart_has_rating_category():
    """Test that games mart has rating category logic."""
    games_mart = Path("src/gaming_pipeline/transform/marts/games.sql")
    content = games_mart.read_text()

    # Should have rating category CASE statement
    assert "rating_category" in content
    assert "CASE" in content.upper()
    assert "Excellent" in content or "Excellent'" in content
    assert "Good" in content or "Good'" in content


def test_games_mart_has_engagement_score():
    """Test that games mart has engagement score calculation."""
    games_mart = Path("src/gaming_pipeline/transform/marts/games.sql")
    content = games_mart.read_text()

    # Should have engagement score calculation
    assert "engagement_score" in content
    assert "COALESCE" in content.upper()


def test_games_mart_unnests_genres():
    """Test that games mart unnests genres from JSON."""
    games_mart = Path("src/gaming_pipeline/transform/marts/games.sql")
    content = games_mart.read_text()

    # Should have UNNEST for genres
    assert "UNNEST" in content.upper()
    assert "genres" in content


def test_staging_games_has_type_casting():
    """Test that staging games has type casting."""
    stg_games = Path("src/gaming_pipeline/transform/staging/stg_games.sql")
    content = stg_games.read_text()

    # Should have TRY_CAST for dates and numbers
    assert "TRY_CAST" in content
    assert "released" in content
    assert "rating" in content
    assert "metacritic" in content


def test_all_files_use_sqlmesh_syntax():
    """Test that transformation files use SQLMesh MODEL DSL."""
    marts_dir = Path("src/gaming_pipeline/transform/marts")
    staging_dir = Path("src/gaming_pipeline/transform/staging")

    all_sql_files = list(marts_dir.glob("*.sql")) + list(staging_dir.glob("*.sql"))

    for sql_file in all_sql_files:
        content = sql_file.read_text()
        # Should have MODEL block (SQLMesh-specific syntax)
        assert "MODEL (" in content or "MODEL(" in content
