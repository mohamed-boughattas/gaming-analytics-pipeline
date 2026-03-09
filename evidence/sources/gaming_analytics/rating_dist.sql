SELECT
  rating_category,
  COUNT(*) AS game_count
FROM marts.marts_games
GROUP BY rating_category
ORDER BY
  CASE rating_category
    WHEN 'Excellent' THEN 1
    WHEN 'Good' THEN 2
    WHEN 'Average' THEN 3
    WHEN 'Below Average' THEN 4
    WHEN 'Poor' THEN 5
    ELSE 6
  END
