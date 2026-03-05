-- ============================================================================
-- SQLMesh Model Definition
-- ============================================================================
-- NOTE: This file uses SQLMesh's custom MODEL DSL syntax (not standard SQL).
-- The MODEL block is SQLMesh-specific and is validated by SQLMesh itself.
-- IDE SQL linters may show warnings about this syntax - this is expected.
-- ============================================================================
MODEL (
    name gaming_analytics.marts_platforms,
    kind FULL,
    grain id
);

-- Platforms mart table with aggregated metrics
WITH exploded_platforms AS (
    -- Explode platforms from JSON array in games table
    SELECT
        CAST(p.platform->>'id' AS INTEGER) AS platform_id,
        p.platform->>'name' AS platform_name,
        p.platform->>'slug' AS platform_slug,
        ga.id AS game_id,
        ga.name AS game_name,
        ga.rating,
        ga.metacritic,
        ga.ratings_count,
        ga.released,
        ga.playtime
    FROM gaming_analytics.stg_games ga,
         UNNEST(platforms) AS p(platform)
    WHERE ga.platforms IS NOT NULL
),

platform_metrics AS (
    SELECT
        ep.platform_id AS id,
        ep.platform_name AS name,
        ep.platform_slug AS slug,
        p.platform_details->>'image' AS image_background,
        p.platform_details->>'year_end' AS year_end,
        p.platform_details->>'year_start' AS year_start,
        p.platform_details->>'games_count' AS games_count_rawg,
        -- Aggregate game metrics by platform
        COUNT(DISTINCT ep.game_id) AS total_games,
        AVG(ep.rating) AS avg_rating,
        AVG(ep.metacritic) AS avg_metacritic,
        MAX(ep.rating) AS max_rating,
        MIN(ep.rating) AS min_rating,
        SUM(ep.ratings_count) AS total_ratings,
        AVG(ep.ratings_count) AS avg_ratings_per_game,
        AVG(ep.playtime) AS avg_playtime,
        -- Count games by rating category
        SUM(CASE WHEN ep.rating >= 9.0 THEN 1 ELSE 0 END) AS excellent_games,
        SUM(CASE WHEN ep.rating >= 7.0 AND ep.rating < 9.0 THEN 1 ELSE 0 END) AS good_games,
        SUM(CASE WHEN ep.rating >= 5.0 AND ep.rating < 7.0 THEN 1 ELSE 0 END) AS average_games,
        SUM(CASE WHEN ep.rating < 5.0 THEN 1 ELSE 0 END) AS below_average_games
FROM exploded_platforms ep
LEFT JOIN gaming_analytics.stg_platforms p ON ep.platform_id = p.id
GROUP BY
        ep.platform_id,
        ep.platform_name,
        ep.platform_slug,
        p.platform_details
)

SELECT
    id,
    name,
    slug,
    image_background,
    year_end,
    year_start,
    games_count_rawg,
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
FROM platform_metrics