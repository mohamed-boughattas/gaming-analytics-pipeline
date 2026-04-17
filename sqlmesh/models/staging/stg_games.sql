-- ============================================================================
-- SQLMesh Model Definition
-- ============================================================================

MODEL (
    name staging.stg_games,
    kind VIEW
);

SELECT
    id,
    name,
    TRY_CAST(released AS DATE) AS released,
    background_image,
    TRY_CAST(rating AS DOUBLE) AS rating,
    TRY_CAST(rating_top AS INTEGER) AS rating_top,
    TRY_CAST(ratings_count AS INTEGER) AS ratings_count,
    TRY_CAST(reviews_text_count AS INTEGER) AS reviews_text_count,
    TRY_CAST(added AS INTEGER) AS added,
    TRY_CAST(playtime AS INTEGER) AS playtime,
    TRY_CAST(suggestions_count AS INTEGER) AS suggestions_count,
    TRY_CAST(updated AS TIMESTAMP) AS updated,
    TRY_CAST(reviews_count AS INTEGER) AS reviews_count,
    saturated_color,
    dominant_color,
    genres,
    platforms
FROM raw.games
WHERE id IS NOT NULL
