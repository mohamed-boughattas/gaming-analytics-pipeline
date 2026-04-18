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
            gp.platform__name AS platform_name,
            gm.id AS game_id,
            gm.rating,
            gm.ratings_count,
            gm.playtime
        FROM raw.games__platforms gp
        JOIN raw.games gm ON gp._dlt_root_id = gm._dlt_id
        WHERE gm.id IS NOT NULL
    ) gm ON gm.platform_name = p.name
WHERE p.id IS NOT NULL
GROUP BY p.id, p.name, p.slug, p.games_count, p.image_background, p.year_start
