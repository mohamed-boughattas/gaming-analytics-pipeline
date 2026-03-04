"""Test configuration and fixtures for gaming analytics pipeline."""

import os
import tempfile
from collections.abc import AsyncGenerator, Generator
from pathlib import Path

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser

from gaming_pipeline.config import config


def pytest_addoption(parser: Parser) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests that require API keys",
    )


def pytest_configure(config: Config) -> None:
    """Configure pytest."""
    config.addinivalue_line("markers", "integration: mark test as integration test")


def pytest_collection_modifyitems(config: Config, items: list) -> None:
    """Modify test collection to skip integration tests if not requested."""
    if config.getoption("--integration"):
        # --integration given in cli: do not skip integration tests
        return
    skip_integration = pytest.mark.skip(reason="need --integration option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


@pytest.fixture
def temp_duckdb_path() -> Generator[str]:
    """Create a temporary DuckDB file path."""
    with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=False) as tmp_file:
        yield tmp_file.name
        # Clean up
        Path(tmp_file.name).unlink(missing_ok=True)


@pytest.fixture
def mock_config(temp_duckdb_path: str) -> Generator[None]:
    """Mock configuration for testing."""
    original_db_path = config.database.path
    config.database.path = temp_duckdb_path

    yield

    # Restore original config
    config.database.path = original_db_path


@pytest.fixture
async def async_client() -> AsyncGenerator:
    """Create an async HTTP client for testing."""
    import httpx

    async with httpx.AsyncClient() as client:
        yield client


@pytest.fixture
def sample_game_data() -> dict:
    """Sample game data for testing."""
    return {
        "id": 12345,
        "name": "Test Game",
        "released": "2024-01-01",
        "rating": 4.5,
        "ratings_count": 1000,
        "metacritic": 85,
        "platforms": [
            {"platform": {"id": 1, "name": "PC", "slug": "pc"}},
            {"platform": {"id": 2, "name": "PlayStation", "slug": "playstation"}},
        ],
        "genres": [
            {"id": 1, "name": "Action", "slug": "action"},
            {"id": 2, "name": "Adventure", "slug": "adventure"},
        ],
    }


@pytest.fixture
def api_keys_available() -> bool:
    """Check if API keys are available for integration tests."""
    return bool(os.getenv("RAWG_API_KEY"))


@pytest.fixture
def mock_rawg_extractor():
    """Mock RAWG extractor for testing with cleanup."""
    from gaming_pipeline.extract.rawg import RAWGExtractor

    class MockRAWGExtractor(RAWGExtractor):
        async def extract_genres(self):
            return [
                {"id": 1, "name": "Action", "slug": "action"},
                {"id": 2, "name": "Adventure", "slug": "adventure"},
            ]

        async def extract_platforms(self):
            return [
                {"id": 1, "name": "PC", "slug": "pc"},
                {"id": 2, "name": "PlayStation", "slug": "playstation"},
            ]

        async def extract_games(self, page_size=20, max_pages=None, updated_after=None):
            from gaming_pipeline.extract.rawg import Game

            sample_games = [
                Game(id=1, name="Game 1", rating=4.5, released="2024-01-01"),
                Game(id=2, name="Game 2", rating=3.8, released="2024-01-02"),
            ]
            yield sample_games

    # Provide the mock extractor
    yield MockRAWGExtractor()

    # Cleanup: drop pending packages to avoid state pollution between tests
    import dlt

    try:
        pipeline = dlt.pipeline("gaming_analytics")
        pipeline.drop_pending_packages()
    except Exception:
        # Ignore cleanup errors - pipeline may not exist
        pass
