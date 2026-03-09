SELECT
  release_year,
  COUNT(*) AS game_count,
  ROUND(AVG(rating), 2) AS avg_rating,
  ROUND(AVG(engagement_score), 2) AS avg_engagement
FROM marts.marts_games
GROUP BY release_year
ORDER BY release_year
