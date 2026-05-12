"""Test configuration and fixtures for gaming analytics pipeline."""

import pytest
import responses
from _pytest.config import Config


def pytest_configure(config: Config) -> None:
    """Configure pytest."""
    config.addinivalue_line("markers", "integration: mark test as integration test")


@pytest.fixture
def mock_rawg_games_page() -> responses.RequestsMock:
    """Fixture that mocks RAWG games API paginated response."""
    with responses.RequestsMock() as rsps:
        rsps.get(
            "https://api.rawg.io/api/games",
            json={
                "count": 1,
                "next": None,
                "results": [
                    {
                        "id": 123,
                        "name": "Test Game",
                        "released": "2024-01-15",
                        "updated": "2024-01-20T00:00:00Z",
                        "rating": 4.5,
                        "rating_top": 5,
                        "ratings_count": 100,
                        "metacritic": 85,
                        "platforms": [
                            {"platform": {"id": 1, "name": "PC", "slug": "pc"}},
                            {"platform": {"id": 4, "name": "Xbox", "slug": "xbox"}},
                        ],
                        "genres": [
                            {"id": 4, "name": "Action", "slug": "action"},
                            {"id": 5, "name": "RPG", "slug": "role-playing-games-pg"},
                        ],
                        "background_image": "https://example.com/image.jpg",
                        "short_description": "A test game description",
                    }
                ],
            },
            status=200,
        )
        yield rsps


@pytest.fixture
def mock_rawg_genres() -> responses.RequestsMock:
    """Fixture that mocks RAWG genres API response."""
    with responses.RequestsMock() as rsps:
        rsps.get(
            "https://api.rawg.io/api/genres",
            json={
                "count": 2,
                "results": [
                    {"id": 4, "name": "Action", "slug": "action"},
                    {"id": 5, "name": "RPG", "slug": "role-playing-games-pg"},
                ],
            },
            status=200,
        )
        yield rsps


@pytest.fixture
def mock_rawg_platforms() -> responses.RequestsMock:
    """Fixture that mocks RAWG platforms API response."""
    with responses.RequestsMock() as rsps:
        rsps.get(
            "https://api.rawg.io/api/platforms",
            json={
                "count": 2,
                "results": [
                    {"id": 1, "name": "PC", "slug": "pc"},
                    {"id": 4, "name": "Xbox", "slug": "xbox"},
                ],
            },
            status=200,
        )
        yield rsps


@pytest.fixture
def mock_rawg_full() -> responses.RequestsMock:
    """Fixture that mocks all three RAWG API endpoints."""
    with responses.RequestsMock() as rsps:
        rsps.get(
            "https://api.rawg.io/api/games",
            json={
                "count": 1,
                "next": None,
                "results": [
                    {
                        "id": 123,
                        "name": "Test Game",
                        "released": "2024-01-15",
                        "updated": "2024-01-20T00:00:00Z",
                        "rating": 4.5,
                        "rating_top": 5,
                        "ratings_count": 100,
                        "platforms": [
                            {"platform": {"id": 1, "name": "PC", "slug": "pc"}},
                        ],
                        "genres": [
                            {"id": 4, "name": "Action", "slug": "action"},
                        ],
                        "background_image": "https://example.com/image.jpg",
                    }
                ],
            },
            status=200,
        )
        rsps.get(
            "https://api.rawg.io/api/genres",
            json={
                "results": [{"id": 4, "name": "Action", "slug": "action"}],
            },
            status=200,
        )
        rsps.get(
            "https://api.rawg.io/api/platforms",
            json={
                "results": [{"id": 1, "name": "PC", "slug": "pc"}],
            },
            status=200,
        )
        yield rsps
