-- SQLMesh Test: Engagement score should be non-negative
-- Business logic: engagement_score is always >= 0
-- Formula: COALESCE(rating, 0) * 0.4 + COALESCE(ratings_count, 0) / 100.0 * 0.6

SELECT
  COUNT(*) AS negative_engagement_scores,
  MIN(engagement_score) AS min_engagement_score,
  MAX(engagement_score) AS max_engagement_score
FROM marts.fct_games
WHERE engagement_score < 0;

-- Expected: 0 negative engagement scores
