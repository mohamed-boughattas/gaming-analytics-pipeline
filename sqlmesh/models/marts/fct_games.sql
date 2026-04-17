-- ============================================================================
-- SQLMesh Model Definition
-- ============================================================================

MODEL (
    name marts.fct_games,
    kind VIEW,
    grain id
);

SELECT
    id,
    name,
    released,
    updated,
    background_image,
    rating,
    rating_top,
    ratings_count,
    reviews_text_count,
    added,
    playtime,
    suggestions_count,
    reviews_count,
    saturated_color,
    dominant_color,
    CASE
        WHEN rating >= 4.5 THEN 'Excellent'
        WHEN rating >= 3.5 THEN 'Good'
        WHEN rating >= 2.5 THEN 'Average'
        WHEN rating >= 1.5 THEN 'Below Average'
        ELSE 'Poor'
    END AS rating_category,
    TRY_CAST(STRFTIME(released, '%Y') AS INTEGER) AS release_year,
    TRY_CAST(STRFTIME(released, '%m') AS INTEGER) AS release_month,
    COALESCE(rating, 0) * 0.4 +
    COALESCE(ratings_count, 0) / 100.0 * 0.6 AS engagement_score
FROM staging.stg_games
WHERE id IS NOT NULL
