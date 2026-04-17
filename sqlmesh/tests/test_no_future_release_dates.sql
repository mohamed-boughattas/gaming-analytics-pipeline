-- SQLMesh Test: No future release dates
-- Business logic: Games cannot have release dates in the future
-- This validates data integrity and prevents data entry errors

SELECT
  COUNT(*) AS future_releases
FROM gaming_analytics.marts.fct_games
WHERE released > CURRENT_DATE;

-- Expected: 0 future releases
-- Any games with future dates indicate data quality issues
-- or incorrect data from the RAWG API
