"""Seed script to create sample gaming data for demo purposes.

This script creates mock data in DuckDB so the pipeline can be tested
without requiring a RAWG API key.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

import duckdb

# Sample game data matching the Game model schema
SAMPLE_GAMES = [
    {
        "id": 1,
        "name": "Elden Ring",
        "released": "2022-02-25",
        "background_image": "https://example.com/elden-ring.jpg",
        "rating": 9.5,
        "rating_top": 5,
        "ratings_count": 45000,
        "reviews_text_count": 12000,
        "added": 85000,
        "metacritic": 96,
        "playtime": 45,
        "suggestions_count": 3200,
        "updated": "2024-01-15T10:30:00Z",
        "reviews_count": 8000,
        "saturated_color": "#1a1a2e",
        "dominant_color": "#16213e",
        "platforms": [
            {"platform": {"name": "PlayStation 5", "id": 187}},
            {"platform": {"name": "Xbox Series X", "id": 186}},
            {"platform": {"name": "PC", "id": 4}},
        ],
        "parent_platforms": [
            {"platform": {"name": "PlayStation", "id": 2}},
            {"platform": {"name": "Xbox", "id": 3}},
            {"platform": {"name": "PC", "id": 1}},
        ],
        "genres": [
            {"name": "Action RPG", "id": 4},
            {"name": "Adventure", "id": 3},
        ],
        "stores": [
            {"store": {"name": "Steam", "id": 1}},
            {"store": {"name": "PlayStation Store", "id": 3}},
        ],
        "tags": [
            {"name": "Open World", "id": 15},
            {"name": "Fantasy", "id": 17},
            {"name": "Souls-like", "id": 21},
        ],
        "short_screenshots": [
            {"id": 1, "image": "https://example.com/shot1.jpg"},
            {"id": 2, "image": "https://example.com/shot2.jpg"},
        ],
    },
    {
        "id": 2,
        "name": "Baldur's Gate 3",
        "released": "2023-08-03",
        "background_image": "https://example.com/baldurs-gate-3.jpg",
        "rating": 9.7,
        "rating_top": 5,
        "ratings_count": 68000,
        "reviews_text_count": 25000,
        "added": 120000,
        "metacritic": 96,
        "playtime": 85,
        "suggestions_count": 5400,
        "updated": "2024-02-01T14:20:00Z",
        "reviews_count": 15000,
        "saturated_color": "#2d1b69",
        "dominant_color": "#431d7c",
        "platforms": [
            {"platform": {"name": "PlayStation 5", "id": 187}},
            {"platform": {"name": "Xbox Series X", "id": 186}},
            {"platform": {"name": "PC", "id": 4}},
        ],
        "parent_platforms": [
            {"platform": {"name": "PlayStation", "id": 2}},
            {"platform": {"name": "Xbox", "id": 3}},
            {"platform": {"name": "PC", "id": 1}},
        ],
        "genres": [
            {"name": "RPG", "id": 5},
            {"name": "Strategy", "id": 10},
        ],
        "stores": [
            {"store": {"name": "Steam", "id": 1}},
            {"store": {"name": "GOG", "id": 5}},
        ],
        "tags": [
            {"name": "Turn-based", "id": 25},
            {"name": "Co-op", "id": 7},
            {"name": "Story Rich", "id": 40},
        ],
        "short_screenshots": [
            {"id": 3, "image": "https://example.com/shot3.jpg"},
            {"id": 4, "image": "https://example.com/shot4.jpg"},
        ],
    },
    {
        "id": 3,
        "name": "Cyberpunk 2077",
        "released": "2020-12-10",
        "background_image": "https://example.com/cyberpunk.jpg",
        "rating": 7.8,
        "rating_top": 5,
        "ratings_count": 52000,
        "reviews_text_count": 18000,
        "added": 95000,
        "metacritic": 86,
        "playtime": 55,
        "suggestions_count": 4100,
        "updated": "2024-01-28T09:45:00Z",
        "reviews_count": 9500,
        "saturated_color": "#fcee0a",
        "dominant_color": "#ff00ff",
        "platforms": [
            {"platform": {"name": "PlayStation 5", "id": 187}},
            {"platform": {"name": "Xbox Series X", "id": 186}},
            {"platform": {"name": "PC", "id": 4}},
        ],
        "parent_platforms": [
            {"platform": {"name": "PlayStation", "id": 2}},
            {"platform": {"name": "Xbox", "id": 3}},
            {"platform": {"name": "PC", "id": 1}},
        ],
        "genres": [
            {"name": "Action RPG", "id": 4},
            {"name": "Shooter", "id": 2},
        ],
        "stores": [
            {"store": {"name": "Steam", "id": 1}},
            {"store": {"name": "Epic Games", "id": 11}},
        ],
        "tags": [
            {"name": "Sci-Fi", "id": 18},
            {"name": "Open World", "id": 15},
            {"name": "Cyberpunk", "id": 33},
        ],
        "short_screenshots": [
            {"id": 5, "image": "https://example.com/shot5.jpg"},
        ],
    },
    {
        "id": 4,
        "name": "Hades",
        "released": "2020-09-17",
        "background_image": "https://example.com/hades.jpg",
        "rating": 9.2,
        "rating_top": 5,
        "ratings_count": 28000,
        "reviews_text_count": 8500,
        "added": 62000,
        "metacritic": 93,
        "playtime": 22,
        "suggestions_count": 2800,
        "updated": "2024-01-20T16:15:00Z",
        "reviews_count": 6200,
        "saturated_color": "#c9302c",
        "dominant_color": "#ff4500",
        "platforms": [
            {"platform": {"name": "PlayStation 4", "id": 18}},
            {"platform": {"name": "Xbox One", "id": 1}},
            {"platform": {"name": "PC", "id": 4}},
            {"platform": {"name": "Nintendo Switch", "id": 7}},
        ],
        "parent_platforms": [
            {"platform": {"name": "PlayStation", "id": 2}},
            {"platform": {"name": "Xbox", "id": 3}},
            {"platform": {"name": "PC", "id": 1}},
            {"platform": {"name": "Nintendo", "id": 7}},
        ],
        "genres": [
            {"name": "Roguelike", "id": 15},
            {"name": "Action", "id": 4},
        ],
        "stores": [
            {"store": {"name": "Steam", "id": 1}},
            {"store": {"name": "Epic Games", "id": 11}},
            {"store": {"name": "Nintendo Store", "id": 7}},
        ],
        "tags": [
            {"name": "Indie", "id": 51},
            {"name": "Difficult", "id": 26},
            {"name": "Mythology", "id": 42},
        ],
        "short_screenshots": [
            {"id": 6, "image": "https://example.com/shot6.jpg"},
        ],
    },
    {
        "id": 5,
        "name": "The Legend of Zelda: Tears of the Kingdom",
        "released": "2023-05-12",
        "background_image": "https://example.com/zelda-totk.jpg",
        "rating": 9.6,
        "rating_top": 5,
        "ratings_count": 38000,
        "reviews_text_count": 11000,
        "added": 72000,
        "metacritic": 96,
        "playtime": 58,
        "suggestions_count": 2900,
        "updated": "2024-01-25T11:40:00Z",
        "reviews_count": 8900,
        "saturated_color": "#6cb043",
        "dominant_color": "#5ca904",
        "platforms": [
            {"platform": {"name": "Nintendo Switch", "id": 7}},
        ],
        "parent_platforms": [
            {"platform": {"name": "Nintendo", "id": 7}},
        ],
        "genres": [
            {"name": "Action-Adventure", "id": 3},
            {"name": "Open World", "id": 15},
        ],
        "stores": [
            {"store": {"name": "Nintendo Store", "id": 7}},
        ],
        "tags": [
            {"name": "Fantasy", "id": 17},
            {"name": "Puzzle", "id": 34},
            {"name": "Exploration", "id": 43},
        ],
        "short_screenshots": [
            {"id": 7, "image": "https://example.com/shot7.jpg"},
            {"id": 8, "image": "https://example.com/shot8.jpg"},
        ],
    },
]

SAMPLE_GENRES = [
    {"id": 1, "name": "Action", "slug": "action", "games_count": 15000, "image_background": "https://example.com/action.jpg"},
    {"id": 2, "name": "Shooter", "slug": "shooter", "games_count": 8500, "image_background": "https://example.com/shooter.jpg"},
    {"id": 3, "name": "Adventure", "slug": "adventure", "games_count": 12000, "image_background": "https://example.com/adventure.jpg"},
    {"id": 4, "name": "RPG", "slug": "rpg", "games_count": 6800, "image_background": "https://example.com/rpg.jpg"},
    {"id": 5, "name": "Strategy", "slug": "strategy", "games_count": 4200, "image_background": "https://example.com/strategy.jpg"},
    {"id": 6, "name": "Indie", "slug": "indie", "games_count": 9500, "image_background": "https://example.com/indie.jpg"},
    {"id": 7, "name": "Platformer", "slug": "platformer", "games_count": 3800, "image_background": "https://example.com/platformer.jpg"},
    {"id": 8, "name": "Simulation", "slug": "simulation", "games_count": 5200, "image_background": "https://example.com/simulation.jpg"},
    {"id": 9, "name": "Sports", "slug": "sports", "games_count": 4800, "image_background": "https://example.com/sports.jpg"},
    {"id": 10, "name": "Racing", "slug": "racing", "games_count": 2100, "image_background": "https://example.com/racing.jpg"},
]

SAMPLE_PLATFORMS = [
    {"id": 1, "name": "PC", "slug": "pc", "games_count": 58000, "image_background": "https://example.com/pc.jpg", "year_start": 1960, "year_end": None},
    {"id": 2, "name": "PlayStation 4", "slug": "playstation-4", "games_count": 32000, "image_background": "https://example.com/ps4.jpg", "year_start": 2013, "year_end": None},
    {"id": 3, "name": "Xbox One", "slug": "xbox-one", "games_count": 28000, "image_background": "https://example.com/xbox-one.jpg", "year_start": 2013, "year_end": 2020},
    {"id": 4, "name": "Nintendo Switch", "slug": "nintendo-switch", "games_count": 45000, "image_background": "https://example.com/switch.jpg", "year_start": 2017, "year_end": None},
    {"id": 5, "name": "PlayStation 5", "slug": "playstation-5", "games_count": 18000, "image_background": "https://example.com/ps5.jpg", "year_start": 2020, "year_end": None},
    {"id": 6, "name": "Xbox Series X", "slug": "xbox-series-x", "games_count": 15000, "image_background": "https://example.com/xbox-series-x.jpg", "year_start": 2020, "year_end": None},
]


def seed_database(db_path: str = "data/gaming_analytics.duckdb") -> None:
    """Seed DuckDB database with sample gaming data.

    Args:
        db_path: Path to the DuckDB database file
    """
    # Ensure data directory exists
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    # Connect to DuckDB
    con = duckdb.connect(str(db_file))

    print("Creating tables...")

    # Create games table
    con.execute("""
        CREATE TABLE IF NOT EXISTS rawg_games (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            released TEXT,
            background_image TEXT,
            rating DOUBLE,
            rating_top INTEGER,
            ratings_count INTEGER,
            reviews_text_count INTEGER,
            added INTEGER,
            metacritic INTEGER,
            playtime INTEGER,
            suggestions_count INTEGER,
            updated TEXT,
            reviews_count INTEGER,
            saturated_color TEXT,
            dominant_color TEXT,
            platforms JSON,
            parent_platforms JSON,
            genres JSON,
            stores JSON,
            clip JSON,
            tags JSON,
            short_screenshots JSON
        )
    """)

    # Create genres table
    con.execute("""
        CREATE TABLE IF NOT EXISTS rawg_genres (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            slug TEXT,
            games_count INTEGER,
            image_background TEXT
        )
    """)

    # Create platforms table
    con.execute("""
        CREATE TABLE IF NOT EXISTS rawg_platforms (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            slug TEXT,
            games_count INTEGER,
            image_background TEXT,
            year_start INTEGER,
            year_end INTEGER
        )
    """)

    print("Inserting sample data...")

    # Insert games
    for game in SAMPLE_GAMES:
        con.execute(
            """
            INSERT INTO rawg_games VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                game["id"],
                game["name"],
                game["released"],
                game["background_image"],
                game["rating"],
                game["rating_top"],
                game["ratings_count"],
                game["reviews_text_count"],
                game["added"],
                game["metacritic"],
                game["playtime"],
                game["suggestions_count"],
                game["updated"],
                game["reviews_count"],
                game["saturated_color"],
                game["dominant_color"],
                json.dumps(game["platforms"]),
                json.dumps(game["parent_platforms"]),
                json.dumps(game["genres"]),
                json.dumps(game["stores"]),
                json.dumps(game.get("clip")),
                json.dumps(game["tags"]),
                json.dumps(game["short_screenshots"]),
            ),
        )

    # Insert genres
    for genre in SAMPLE_GENRES:
        con.execute(
            """
            INSERT INTO rawg_genres VALUES (?, ?, ?, ?, ?)
            """,
            (genre["id"], genre["name"], genre["slug"], genre["games_count"], genre["image_background"]),
        )

    # Insert platforms
    for platform in SAMPLE_PLATFORMS:
        con.execute(
            """
            INSERT INTO rawg_platforms VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                platform["id"],
                platform["name"],
                platform["slug"],
                platform["games_count"],
                platform["image_background"],
                platform["year_start"],
                platform["year_end"],
            ),
        )

    # Verify data
    games_count = con.execute("SELECT COUNT(*) FROM rawg_games").fetchone()[0]
    genres_count = con.execute("SELECT COUNT(*) FROM rawg_genres").fetchone()[0]
    platforms_count = con.execute("SELECT COUNT(*) FROM rawg_platforms").fetchone()[0]

    print(f"\nSample data seeded successfully!")
    print(f"  - {games_count} games")
    print(f"  - {genres_count} genres")
    print(f"  - {platforms_count} platforms")
    print(f"\nDatabase location: {db_file.absolute()}")

    con.close()


if __name__ == "__main__":
    seed_database()
