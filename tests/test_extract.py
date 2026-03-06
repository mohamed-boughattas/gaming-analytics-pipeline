"""Tests for data extraction module."""

import pytest

from gaming_pipeline.extract.rawg import (
    Game,
)


class TestGameModel:
    """Test Game model validation."""

    def test_game_creation(self):
        """Test basic game creation."""
        game_data = {
            "id": 12345,
            "name": "Test Game",
            "rating": 4.5,
            "released": "2024-01-01",
        }

        game = Game(**game_data)
        assert game.id == 12345
        assert game.name == "Test Game"
        assert game.rating == 4.5
        assert game.released == "2024-01-01"

    def test_game_optional_fields(self):
        """Test game creation with optional fields."""
        game_data = {
            "id": 12345,
            "name": "Test Game",
            "rating": 4.5,
            "metacritic": 85,
            "platforms": [{"platform": {"id": 1, "name": "PC"}}],
            "genres": [{"id": 1, "name": "Action"}],
        }

        game = Game(**game_data)
        assert game.metacritic == 85
        assert game.platforms is not None
        assert game.genres is not None


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

        # Test games
        games_batch = []
        async for games in mock_rawg_extractor.extract_games():
            games_batch.extend(games)

        assert len(games_batch) == 2
        assert games_batch[0].name == "Game 1"
