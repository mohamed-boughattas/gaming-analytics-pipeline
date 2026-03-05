-- ============================================================================
-- SQLMesh Model Definition
-- ============================================================================
-- NOTE: This file uses SQLMesh's custom MODEL DSL syntax (not standard SQL).
-- The MODEL block is SQLMesh-specific and is validated by SQLMesh itself.
-- IDE SQL linters may show warnings about this syntax - this is expected.
-- ============================================================================
MODEL (
    name gaming_analytics.stg_platforms,
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
    
    -- Platform details (kept as JSON for flexibility)
    platform_details,
    
    -- Metadata
    updated,
    added
FROM gaming_analytics.rawg_platforms
WHERE id IS NOT NULL