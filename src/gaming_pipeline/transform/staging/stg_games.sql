-- ============================================================================
-- SQLMesh Model Definition
-- ============================================================================
-- NOTE: This file uses SQLMesh's custom MODEL DSL syntax (not standard SQL).
-- The MODEL block is SQLMesh-specific and is validated by SQLMesh itself.
-- IDE SQL linters may show warnings about this syntax - this is expected.
-- ============================================================================
MODEL (
    name gaming_analytics.stg_games,
    kind FULL,
    grain id
);

-- Staging layer for games - light transformations only
-- This layer handles: type casting, null handling, column renaming
-- Business logic and aggregations are in marts layer
SELECT
    -- Primary key
    id,
    
    -- Basic info
    name,
    
    -- Dates with proper casting
    TRY_CAST(released AS DATE) AS released,
    TRY_CAST(updated AS DATE) AS updated,
    
    -- Ratings
    TRY_CAST(rating AS DOUBLE) AS rating,
    TRY_CAST(rating_top AS INTEGER) AS rating_top,
    TRY_CAST(ratings_count AS INTEGER) AS ratings_count,
    TRY_CAST(reviews_text_count AS INTEGER) AS reviews_text_count,
    
    -- Engagement
    TRY_CAST(added AS INTEGER) AS added,
    TRY_CAST(metacritic AS INTEGER) AS metacritic,
    TRY_CAST(playtime AS INTEGER) AS playtime,
    TRY_CAST(suggestions_count AS INTEGER) AS suggestions_count,
    TRY_CAST(reviews_count AS INTEGER) AS reviews_count,
    
    -- Visual assets
    background_image,
    saturated_color,
    dominant_color,
    
    -- JSON arrays (kept as is, will be processed in marts)
    platforms,
    parent_platforms,
    genres,
    stores,
    tags,
    short_screenshots,
    clip
FROM gaming_analytics.rawg_games
WHERE id IS NOT NULL