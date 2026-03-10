-- ============================================================================
-- SQLMesh Model Definition
-- ============================================================================
-- NOTE: This file uses SQLMesh's custom MODEL DSL syntax (not standard SQL).
-- The MODEL block is SQLMesh-specific and is validated by SQLMesh itself.
-- IDE SQL linters may show warnings about this syntax - this is expected.
-- ============================================================================

MODEL ( -- noqa: PRS
    name staging.stg_platforms,
    dialect duckdb,
    kind FULL,
    grain id
);

-- Staging layer for platforms - light transformations only
-- This layer handles: type casting, null handling, column renaming
-- Business logic and aggregations are in marts layer
SELECT
    -- Primary key
    TRY_CAST(id AS INTEGER) AS id,

    -- Basic info
    name,
    slug,
    image_background,

    -- Platform years
    TRY_CAST(year_start AS INTEGER) AS year_start,
    TRY_CAST(year_end AS INTEGER) AS year_end,

    -- Games count from API (not our count)
    TRY_CAST(games_count AS INTEGER) AS games_count_rawg
FROM raw.rawg_platforms
WHERE id IS NOT NULL
