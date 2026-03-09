SELECT
  name,
  rating,
  metacritic,
  release_year,
  rating_category,
  engagement_score,
  genre_count,
  platform_count
FROM marts.marts_games
ORDER BY rating DESC, engagement_score DESC
LIMIT 20
