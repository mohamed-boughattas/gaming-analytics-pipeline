-- ============================================================================
-- SQLMesh Model Definition
-- ============================================================================

MODEL (
    name marts.fct_genres,
    kind VIEW,
    grain id
);

SELECT
    g.id,
    g.name,
    g.slug,
    g.games_count AS api_games_count,
    g.image_background,
    COUNT(DISTINCT gm.game_id) AS total_games,
    AVG(gm.rating) AS avg_rating,
    SUM(gm.ratings_count) AS total_ratings,
    AVG(gm.playtime) AS avg_playtime
FROM staging.stg_genres g
LEFT JOIN (
        SELECT
            gg.name AS genre_name,
            gm.id AS game_id,
            gm.rating,
            gm.ratings_count,
            gm.playtime
        FROM raw.games__genres gg
        JOIN raw.games gm ON gg._dlt_root_id = gm._dlt_id
        WHERE gm.id IS NOT NULL
    ) gm ON gm.genre_name = g.name
WHERE g.id IS NOT NULL
GROUP BY g.id, g.name, g.slug, g.games_count, g.image_background
