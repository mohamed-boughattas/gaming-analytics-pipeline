-- SQLMesh Test: No NULL platform names
-- Ensures all platforms have a name populated

SELECT COUNT(*) AS null_platform_names
FROM marts.fct_platforms
WHERE name IS NULL OR name = '';

-- Expected: 0