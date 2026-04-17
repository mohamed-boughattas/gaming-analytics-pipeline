-- SQLMesh Test: No NULL game names
-- Ensures that all games have a name populated

SELECT COUNT(*) AS null_game_names
FROM marts.fct_games
WHERE name IS NULL OR name = '';

-- Expected: 0
