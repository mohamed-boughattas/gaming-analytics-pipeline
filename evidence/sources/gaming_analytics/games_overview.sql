SELECT
  COUNT(*) AS total_games,
  ROUND(AVG(rating), 2) AS avg_rating,
  ROUND(AVG(metacritic), 1) AS avg_metacritic,
  SUM(playtime) AS total_playtime_hours,
  ROUND(AVG(engagement_score), 2) AS avg_engagement_score
FROM marts.marts_games
