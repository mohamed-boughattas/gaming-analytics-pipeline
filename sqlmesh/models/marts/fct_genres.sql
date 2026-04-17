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
            gm_inner.id AS game_id,
            gm_inner.rating,
            gm_inner.ratings_count,
            gm_inner.playtime,
            je.value->>'name' AS genre_name
        FROM staging.stg_games gm_inner
        CROSS JOIN LATERAL json_each(gm_inner.genres) AS je
        WHERE gm_inner.id IS NOT NULL AND gm_inner.genres IS NOT NULL
    ) gm ON gm.genre_name = g.name
WHERE g.id IS NOT NULL
GROUP BY g.id, g.name, g.slug, g.games_count, g.image_background
