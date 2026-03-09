SELECT
  name,
  rating,
  engagement_score,
  rating_category,
  release_year
FROM marts.marts_games
ORDER BY engagement_score DESC
LIMIT 20
