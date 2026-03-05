-- ============================================================================
-- SQLMesh Model Definition
-- ============================================================================
-- NOTE: This file uses SQLMesh's custom MODEL DSL syntax (not standard SQL).
-- The MODEL block is SQLMesh-specific and is validated by SQLMesh itself.
-- IDE SQL linters may show warnings about this syntax - this is expected.
-- ============================================================================
MODEL (
    name gaming_analytics.marts_genres,
    kind FULL,
    grain id
);

-- Genres mart table with aggregated metrics
WITH exploded_genres AS (
    -- Explode genres from JSON array in games table
    SELECT
        CAST(g.genre->>'id' AS INTEGER) AS genre_id,
        g.genre->>'name' AS genre_name,
        g.genre->>'slug' AS genre_slug,
        ga.id AS game_id,
        ga.name AS game_name,
        ga.rating,
        ga.metacritic,
        ga.ratings_count,
        ga.released,
        ga.playtime
    FROM gaming_analytics.stg_games ga,
         UNNEST(genres) AS g(genre)
    WHERE ga.genres IS NOT NULL
),

genre_metrics AS (
    SELECT
        eg.genre_id AS id,
        eg.genre_name AS name,
        eg.genre_slug AS slug,
        g.image_background,
        -- Aggregate game metrics by genre
        COUNT(DISTINCT eg.game_id) AS total_games,
        AVG(eg.rating) AS avg_rating,
        AVG(eg.metacritic) AS avg_metacritic,
        MAX(eg.rating) AS max_rating,
        MIN(eg.rating) AS min_rating,
        SUM(eg.ratings_count) AS total_ratings,
        AVG(eg.ratings_count) AS avg_ratings_per_game,
        AVG(eg.playtime) AS avg_playtime,
        -- Count games by rating category
        SUM(CASE WHEN eg.rating >= 9.0 THEN 1 ELSE 0 END) AS excellent_games,
        SUM(CASE WHEN eg.rating >= 7.0 AND eg.rating < 9.0 THEN 1 ELSE 0 END) AS good_games,
        SUM(CASE WHEN eg.rating >= 5.0 AND eg.rating < 7.0 THEN 1 ELSE 0 END) AS average_games,
        SUM(CASE WHEN eg.rating < 5.0 THEN 1 ELSE 0 END) AS below_average_games
FROM exploded_genres eg
LEFT JOIN gaming_analytics.stg_genres g ON eg.genre_id = g.id
GROUP BY
        eg.genre_id,
        eg.genre_name,
        eg.genre_slug,
        g.image_background
)

SELECT
    id,
    name,
    slug,
    image_background,
    total_games,
    ROUND(avg_rating, 2) AS avg_rating,
    ROUND(avg_metacritic, 2) AS avg_metacritic,
    ROUND(max_rating, 2) AS max_rating,
    ROUND(min_rating, 2) AS min_rating,
    total_ratings,
    ROUND(avg_ratings_per_game, 2) AS avg_ratings_per_game,
    ROUND(avg_playtime, 2) AS avg_playtime,
    excellent_games,
    good_games,
    average_games,
    below_average_games,
    -- Calculate percentage breakdown
    ROUND(excellent_games * 100.0 / total_games, 2) AS excellent_pct,
    ROUND(good_games * 100.0 / total_games, 2) AS good_pct,
    ROUND(average_games * 100.0 / total_games, 2) AS average_pct,
    ROUND(below_average_games * 100.0 / total_games, 2) AS below_average_pct
FROM genre_metrics
