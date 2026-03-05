"""Script to seed DuckDB with sample data for demo purposes."""

from pathlib import Path

import duckdb


def seed_sample_data(db_path: str = "data/gaming_analytics.duckdb"):
    """Seed DuckDB with sample gaming data for demo."""

    # Create data directory if it doesn't exist
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(db_path)

    print("Creating schema...")
    con.execute("""
        CREATE SCHEMA IF NOT EXISTS gaming_analytics;
    """)

    print("Seeding genres...")
    con.execute("""
        CREATE OR REPLACE TABLE gaming_analytics.rawg_genres AS
        SELECT * FROM (
            VALUES
                (1, 'Action', 'action', 'https://image.url/action.jpg', 1000),
                (2, 'Adventure', 'adventure', 'https://image.url/adventure.jpg', 800),
                (3, 'RPG', 'rpg', 'https://image.url/rpg.jpg', 600),
                (4, 'Strategy', 'strategy', 'https://image.url/strategy.jpg', 400),
                (5, 'Shooter', 'shooter', 'https://image.url/shooter.jpg', 900),
                (6, 'Indie', 'indie', 'https://image.url/indie.jpg', 500),
                (7, 'Puzzle', 'puzzle', 'https://image.url/puzzle.jpg', 300),
                (8, 'Racing', 'racing', 'https://image.url/racing.jpg', 200),
                (9, 'Sports', 'sports', 'https://image.url/sports.jpg', 700),
                (10, 'Simulation', 'simulation', 'https://image.url/simulation.jpg', 450)
        ) AS genres(id, name, slug, image_background, games_count);
    """)

    print("Seeding platforms...")
    con.execute("""
        CREATE OR REPLACE TABLE gaming_analytics.rawg_platforms AS
        SELECT * FROM (
            VALUES
                (1, 'PC', 'pc', 'https://image.url/pc.jpg', '{"year_start": 1980, "year_end": null, "games_count": 10000}'),
                (2, 'PlayStation 5', 'playstation5', 'https://image.url/ps5.jpg', '{"year_start": 2020, "year_end": null, "games_count": 3000}'),
                (3, 'Xbox Series X', 'xbox-series-x', 'https://image.url/xbox.jpg', '{"year_start": 2020, "year_end": null, "games_count": 2500}'),
                (4, 'Nintendo Switch', 'switch', 'https://image.url/switch.jpg', '{"year_start": 2017, "year_end": null, "games_count": 5000}'),
                (5, 'PlayStation 4', 'playstation4', 'https://image.url/ps4.jpg', '{"year_start": 2013, "year_end": null, "games_count": 8000}')
        ) AS platforms(id, name, slug, image, platform_details);
    """)

    print("Seeding games...")
    con.execute("""
        CREATE OR REPLACE TABLE gaming_analytics.rawg_games AS
        SELECT * FROM (
            VALUES
                (1, 'The Legend of Zelda: Tears of the Kingdom', 'zelda-totk', '2023-05-12', '2023-05-12', 9.6, 10, 50000, 2000, 50000, 96, 120, 500, 50, 20, 10, 5000, 1000, 500, 200, 50, 20, 10,
                 '[{"id": 1, "name": "Action"}, {"id": 2, "name": "Adventure"}]',
                 '[{"platform": {"id": 1, "name": "PC"}}, {"platform": {"id": 4, "name": "Nintendo Switch"}]',
                 '[{"store": {"id": 1, "name": "Steam"}}]',
                 'https://image.url/zelda.jpg', '#3498db', '#2980b9'),
                (2, 'Baldur''s Gate 3', 'baldurs-gate-3', '2023-08-03', '2023-08-03', 9.7, 10, 45000, 2500, 45000, 96, 150, 600, 40, 15, 12, 4500, 800, 400, 150, 30, 15, 12,
                 '[{"id": 1, "name": "Action"}, {"id": 3, "name": "RPG"}, {"id": 2, "name": "Adventure"}]',
                 '[{"platform": {"id": 1, "name": "PC"}}, {"platform": {"id": 2, "name": "PlayStation 5"}, {"platform": {"id": 4, "name": "Nintendo Switch"}]',
                 '[{"store": {"id": 1, "name": "Steam"}, {"store": {"id": 2, "name": "GOG"}}]',
                 'https://image.url/bg3.jpg', '#9b59b6', '#8e44ad'),
                (3, 'Elden Ring', 'elden-ring', '2022-02-25', '2022-02-25', 9.5, 10, 60000, 3000, 60000, 95, 100, 800, 60, 25, 15, 6000, 900, 450, 200, 40, 20, 15,
                 '[{"id": 1, "name": "Action"}, {"id": 3, "name": "RPG"}]',
                 '[{"platform": {"id": 1, "name": "PC"}}, {"platform": {"id": 2, "name": "PlayStation 5"}]',
                 '[{"store": {"id": 1, "name": "Steam"}}]',
                 'https://image.url/elden.jpg', '#1abc9c', '#16a085'),
                (4, 'Cyberpunk 2077', 'cyberpunk-2077', '2020-12-10', '2023-09-26', 8.2, 10, 80000, 4000, 80000, 86, 80, 1200, 80, 30, 20, 8000, 700, 350, 300, 50, 25, 20,
                 '[{"id": 1, "name": "Action"}, {"id": 2, "name": "Adventure"}, {"id": 3, "name": "RPG"}]',
                 '[{"platform": {"id": 1, "name": "PC"}}, {"platform": {"id": 2, "name": "PlayStation 5"}}]',
                 '[{"store": {"id": 1, "name": "Steam"}}]',
                 'https://image.url/cyberpunk.jpg', '#f39c12', '#e74c3c'),
                (5, 'God of War Ragnarök', 'god-of-war-ragnarok', '2022-11-09', '2022-11-09', 9.4, 10, 35000, 1800, 35000, 94, 40, 550, 35, 15, 10, 3500, 600, 300, 120, 25, 12, 10,
                 '[{"id": 1, "name": "Action"}, {"id": 2, "name": "Adventure"}]',
                 '[{"platform": {"id": 2, "name": "PlayStation 5"}}]',
                 '[{"store": {"id": 3, "name": "PlayStation Store"}}]',
                 'https://image.url/gow.jpg', '#e74c3c', '#c0392b'),
                (6, 'Hollow Knight', 'hollow-knight', '2017-02-24', '2017-02-24', 9.1, 10, 25000, 1200, 25000, 90, 25, 300, 20, 8, 5, 2500, 400, 200, 80, 15, 8, 5,
                 '[{"id": 6, "name": "Indie"}, {"id": 1, "name": "Action"}, {"id": 7, "name": "Puzzle"}]',
                 '[{"platform": {"id": 1, "name": "PC"}}, {"platform": {"id": 4, "name": "Nintendo Switch"}}]',
                 '[{"store": {"id": 1, "name": "Steam"}}]',
                 'https://image.url/hollow.jpg', '#34495e', '#2c3e50'),
                (7, 'Celeste', 'celeste', '2018-01-25', '2018-01-25', 9.3, 10, 15000, 800, 15000, 94, 12, 200, 15, 5, 3, 1500, 300, 150, 60, 10, 6, 3,
                 '[{"id": 6, "name": "Indie"}, {"id": 7, "name": "Puzzle"}, {"id": 1, "name": "Action"}]',
                 '[{"platform": {"id": 1, "name": "PC"}}, {"platform": {"id": 4, "name": "Nintendo Switch"}}]',
                 '[{"store": {"id": 1, "name": "Steam"}}]',
                 'https://image.url/celeste.jpg', '#e67e22', '#d35400'),
                (8, 'Stardew Valley', 'stardew-valley', '2016-02-26', '2016-02-26', 9.4, 10, 35000, 1500, 35000, 93, 200, 400, 25, 8, 5, 3500, 500, 250, 100, 18, 10, 5,
                 '[{"id": 6, "name": "Indie"}, {"id": 10, "name": "Simulation"}]',
                 '[{"platform": {"id": 1, "name": "PC"}}, {"platform": {"id": 4, "name": "Nintendo Switch"}}]',
                 '[{"store": {"id": 1, "name": "Steam"}}]',
                 'https://image.url/stardew.jpg', '#2ecc71', '#27ae60'),
                (9, 'Red Dead Redemption 2', 'rdr2', '2018-10-26', '2018-10-26', 9.1, 10, 70000, 3200, 70000, 97, 80, 900, 50, 20, 15, 7000, 800, 400, 250, 40, 20, 15,
                 '[{"id": 1, "name": "Action"}, {"id": 2, "name": "Adventure"}]',
                 '[{"platform": {"id": 1, "name": "PC"}}, {"platform": {"id": 2, "name": "PlayStation 5"}}]',
                 '[{"store": {"id": 1, "name": "Steam"}}]',
                 'https://image.url/rdr2.jpg', '#8e44ad', '#7d3c98'),
                (10, 'The Witcher 3: Wild Hunt', 'witcher-3', '2015-05-19', '2015-05-19', 9.5, 10, 100000, 4000, 100000, 92, 60, 750, 45, 18, 12, 10000, 900, 450, 350, 45, 22, 12,
                 '[{"id": 1, "name": "Action"}, {"id": 3, "name": "RPG"}, {"id": 2, "name": "Adventure"}]',
                 '[{"platform": {"id": 1, "name": "PC"}}, {"platform": {"id": 2, "name": "PlayStation 5"}}]',
                 '[{"store": {"id": 1, "name": "Steam"}}]',
                 'https://image.url/witcher.jpg', '#16a085', '#138d75')
        ) AS games(
            id, name, slug, released, updated, rating, rating_top, ratings_count, reviews_text_count,
            added, metacritic, playtime, suggestions_count, reviews_count,
            screenshots_count, movies_count, creators_count, achievements_count,
            reddit_count, twitch_count, youtube_count, rating_1_pct, rating_2_pct,
            rating_3_pct, rating_4_pct, rating_5_pct, genres, platforms, stores,
            background_image, saturated_color, dominant_color
        );
    """)

    # Create mart tables by running the SQLMesh transformations
    print("Creating marts_games table...")
    try:
        con.execute(
            "CREATE OR REPLACE TABLE gaming_analytics.marts_games AS SELECT * FROM gaming_analytics.rawg_games WHERE 1=0;"
        )
    except Exception as e:
        print(f"Note: marts_games creation skipped: {e}")

    print("Creating marts_genres table...")
    try:
        con.execute("""
            CREATE OR REPLACE TABLE gaming_analytics.marts_genres AS
            SELECT 
                g.id,
                g.name,
                g.slug,
                g.image_background,
                COUNT(DISTINCT ga.id) AS total_games,
                AVG(ga.rating) AS avg_rating,
                AVG(ga.metacritic) AS avg_metacritic,
                MAX(ga.rating) AS max_rating,
                MIN(ga.rating) AS min_rating,
                SUM(ga.ratings_count) AS total_ratings,
                AVG(ga.ratings_count) AS avg_ratings_per_game,
                AVG(ga.playtime) AS avg_playtime,
                SUM(CASE WHEN ga.rating >= 9.0 THEN 1 ELSE 0 END) AS excellent_games,
                SUM(CASE WHEN ga.rating >= 7.0 AND ga.rating < 9.0 THEN 1 ELSE 0 END) AS good_games,
                SUM(CASE WHEN ga.rating >= 5.0 AND ga.rating < 7.0 THEN 1 ELSE 0 END) AS average_games,
                SUM(CASE WHEN ga.rating < 5.0 THEN 1 ELSE 0 END) AS below_average_games
            FROM gaming_analytics.rawg_genres g
            LEFT JOIN gaming_analytics.rawg_games ga ON g.name LIKE '%' || ga.genres || '%'
            GROUP BY g.id, g.name, g.slug, g.image_background;
        """)
    except Exception as e:
        print(f"Note: marts_genres creation skipped: {e}")

    print("Creating marts_platforms table...")
    try:
        con.execute("""
            CREATE OR REPLACE TABLE gaming_analytics.marts_platforms AS
            SELECT 
                p.id,
                p.name,
                p.slug,
                p.image,
                JSON_EXTRACT(p.platform_details, '$.year_start')::TEXT as year_start,
                COUNT(DISTINCT ga.id) AS total_games,
                AVG(ga.rating) AS avg_rating,
                AVG(ga.metacritic) AS avg_metacritic,
                MAX(ga.rating) AS max_rating,
                MIN(ga.rating) AS min_rating,
                SUM(ga.ratings_count) AS total_ratings,
                AVG(ga.ratings_count) AS avg_ratings_per_game,
                AVG(ga.playtime) AS avg_playtime,
                SUM(CASE WHEN ga.rating >= 9.0 THEN 1 ELSE 0 END) AS excellent_games,
                SUM(CASE WHEN ga.rating >= 7.0 AND ga.rating < 9.0 THEN 1 ELSE 0 END) AS good_games,
                SUM(CASE WHEN ga.rating >= 5.0 AND ga.rating < 7.0 THEN 1 ELSE 0 END) AS average_games,
                SUM(CASE WHEN ga.rating < 5.0 THEN 1 ELSE 0 END) AS below_average_games
            FROM gaming_analytics.rawg_platforms p
            LEFT JOIN gaming_analytics.rawg_games ga ON p.name LIKE '%' || ga.platforms || '%'
            GROUP BY p.id, p.name, p.slug, p.image, p.platform_details;
        """)
    except Exception as e:
        print(f"Note: marts_platforms creation skipped: {e}")

    print("\nSample data seeded successfully!")
    print(f"Database created at: {db_path}")

    # Print summary
    tables = con.execute("""
        SELECT table_name, (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = t.table_name) as row_count
        FROM information_schema.tables t
        WHERE table_schema = 'gaming_analytics'
        ORDER BY table_name
    """).fetchall()

    print("\nTables created:")
    for table, count in tables:
        print(f"  - {table}: {count} rows")

    con.close()


if __name__ == "__main__":
    seed_sample_data()
