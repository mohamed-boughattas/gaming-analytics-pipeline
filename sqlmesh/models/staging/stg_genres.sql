-- ============================================================================
-- SQLMesh Model Definition
-- ============================================================================

MODEL (
    name staging.stg_genres,
    kind VIEW
);

SELECT
    id,
    name,
    slug,
    TRY_CAST(games_count AS INTEGER) AS games_count,
    image_background
FROM raw.genres
WHERE id IS NOT NULL
