-- SQLMesh Test: Engagement score should be non-negative
-- Ensures the calculated engagement_score is always >= 0
-- Engagement score is a weighted combination of rating, metacritic, and ratings_count

SELECT
    COUNT(*) AS negative_engagement_scores,
    MIN(engagement_score) AS min_engagement_score,
    MAX(engagement_score) AS max_engagement_score
FROM gaming_analytics.marts_games
WHERE engagement_score < 0;

-- Expected: 0 negative engagement scores
-- Formula: COALESCE(rating, 0) * 0.4 + COALESCE(metacritic, 0) / 10.0 * 0.3 + COALESCE(ratings_count, 0) / 100.0 * 0.3
-- With COALESCE handling NULL as 0, all components should be >= 0
