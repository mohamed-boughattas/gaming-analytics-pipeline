-- ============================================================================
-- SQLMesh Model Definition
-- ============================================================================

MODEL (
    name marts.fct_platforms,
    kind VIEW,
    grain id
);

SELECT
    p.id,
    p.name,
    p.slug,
    p.games_count AS api_games_count,
    p.image_background,
    p.year_start,
    COUNT(DISTINCT gm.game_id) AS total_games,
    AVG(gm.rating) AS avg_rating,
    SUM(gm.ratings_count) AS total_ratings,
    AVG(gm.playtime) AS avg_playtime
FROM staging.stg_platforms p
LEFT JOIN (
        SELECT
            gm_inner.id AS game_id,
            gm_inner.rating,
            gm_inner.ratings_count,
            gm_inner.playtime,
            je.value->'platform'->>'name' AS platform_name
        FROM staging.stg_games gm_inner
        CROSS JOIN LATERAL json_each(gm_inner.platforms) AS je
        WHERE gm_inner.id IS NOT NULL AND gm_inner.platforms IS NOT NULL
    ) gm ON gm.platform_name = p.name
WHERE p.id IS NOT NULL
GROUP BY p.id, p.name, p.slug, p.games_count, p.image_background, p.year_start
