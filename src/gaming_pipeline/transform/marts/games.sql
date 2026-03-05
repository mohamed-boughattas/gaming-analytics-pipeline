-- ============================================================================
-- SQLMesh Model Definition
-- ============================================================================
-- NOTE: This file uses SQLMesh's custom MODEL DSL syntax (not standard SQL).
-- The MODEL block is SQLMesh-specific and is validated by SQLMesh itself.
-- IDE SQL linters may show warnings about this syntax - this is expected.
-- ============================================================================
MODEL (
    name gaming_analytics.marts_games,
    kind INCREMENTAL,
    start_date '2020-01-01',
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
        -- Extract genre names from JSON array
        UNNEST(genres) AS genre_names,
        -- Extract platform names from JSON array
        [p->'platform'->>'name' FOR p IN UNNEST(platforms)] AS platform_names,
        -- Extract store names from JSON array
        [s->'store'->>'name' FOR s IN UNNEST(stores)] AS store_names
FROM gaming_analytics.stg_games
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
        COALESCE(ratings_count, 0) / 100.0 * 0.3 AS engagement_score,
        -- Count arrays for metrics
        ARRAY_LENGTH(genre_names) AS genre_count,
        ARRAY_LENGTH(platform_names) AS platform_count,
        ARRAY_LENGTH(store_names) AS store_count
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
    genre_names,
    platform_names,
    store_names,
    rating_category,
    release_year,
    release_month,
    engagement_score,
    genre_count,
    platform_count,
    store_count
FROM enriched_games
