-- SQLMesh Test: No NULL game names
-- Ensures that all games have a name populated
-- This is a critical data quality check as game name is required for all analytics

SELECT COUNT(*) AS null_game_names
FROM gaming_analytics.marts_games
WHERE name IS NULL OR name = '';

-- Expected: 0
-- Any result > 0 indicates games without names, which would break downstream analytics
