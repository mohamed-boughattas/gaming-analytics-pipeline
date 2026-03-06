-- SQLMesh Test: Rating ranges validation
-- Ensures that ratings fall within expected bounds (0.0 to 10.0)
-- This validates data quality and API response integrity

SELECT
    COUNT(*) AS invalid_ratings,
    MIN(rating) AS min_rating,
    MAX(rating) AS max_rating
FROM gaming_analytics.marts_games
WHERE rating IS NOT NULL AND (rating < 0.0 OR rating > 10.0);

-- Expected: 0 invalid ratings
-- The RAWG API should return ratings in the 0-10 range
-- Any violations indicate data quality issues or API anomalies
