-- SQLMesh Test: Rating ranges validation
-- RAWG ratings are on a 0-5 scale; this validates bounds

SELECT
  COUNT(*) AS invalid_ratings,
  MIN(rating) AS min_rating,
  MAX(rating) AS max_rating
FROM marts.fct_games
WHERE rating IS NOT NULL AND (rating < 0.0 OR rating > 5.0);

-- Expected: 0 invalid ratings
