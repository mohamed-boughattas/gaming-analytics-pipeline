-- SQLMesh Test: No NULL genre names
-- Ensures all genres have a name populated

SELECT COUNT(*) AS null_genre_names
FROM marts.fct_genres
WHERE name IS NULL OR name = '';

-- Expected: 0