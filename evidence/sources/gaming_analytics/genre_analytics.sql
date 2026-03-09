SELECT
  name AS genre_name,
  total_games,
  ROUND(avg_rating, 2) AS avg_rating,
  ROUND(avg_metacritic, 1) AS avg_metacritic,
  ROUND(excellent_pct, 1) AS excellent_pct
FROM marts.marts_genres
ORDER BY total_games DESC, avg_rating DESC
