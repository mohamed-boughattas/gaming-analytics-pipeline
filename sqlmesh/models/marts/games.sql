-- ============================================================================
-- SQLMesh Model Definition
-- ============================================================================
-- NOTE: This file uses SQLMesh's custom MODEL DSL syntax (not standard SQL).
-- The MODEL block is SQLMesh-specific and is validated by SQLMesh itself.
-- IDE SQL linters may show warnings about this syntax - this is expected.
-- ============================================================================

MODEL ( -- noqa: PRS
    name marts.games,
    dialect duckdb,
    kind VIEW,
    start '2020-01-01',
    grain id
);

-- Games mart table with enriched metrics
WITH raw_games AS (
    SELECT
        id,
        name,
        released,
        updated,
        rating,
        rating_top,
        ratings_count,
        reviews_text_count,
        added,
        metacritic,
        playtime,
        suggestions_count,
        reviews_count,
        background_image,
        saturated_color,
        dominant_color,
        -- Keep JSON arrays as-is for explosion in other models
        genres,
        platforms,
        stores
FROM staging.stg_games
WHERE id IS NOT NULL
),

enriched_games AS (
    SELECT
        *,
        -- Calculate rating categories
        CASE
            WHEN rating >= 9.0 THEN 'Excellent'
            WHEN rating >= 7.0 THEN 'Good'
            WHEN rating >= 5.0 THEN 'Average'
            WHEN rating >= 3.0 THEN 'Below Average'
            ELSE 'Poor'
        END AS rating_category,
        -- Calculate release year and month
        TRY_CAST(STRFTIME(released, '%Y') AS INTEGER) AS release_year,
        TRY_CAST(STRFTIME(released, '%m') AS INTEGER) AS release_month,
        -- Calculate engagement score (weighted combination)
        COALESCE(rating, 0) * 0.4 +
        COALESCE(metacritic, 0) / 10.0 * 0.3 +
        COALESCE(ratings_count, 0) / 100.0 * 0.3 AS engagement_score
    FROM raw_games
)

SELECT
    id,
    name,
    released,
    updated,
    rating,
    rating_top,
    ratings_count,
    reviews_text_count,
    added,
    metacritic,
    playtime,
    suggestions_count,
    reviews_count,
    background_image,
    saturated_color,
    dominant_color,
    genre,
    platforms,
    stores,
    rating_category,
    release_year,
    release_month,
    engagement_score
FROM enriched_games
CROSS JOIN UNNEST(genres) AS t(genre)
