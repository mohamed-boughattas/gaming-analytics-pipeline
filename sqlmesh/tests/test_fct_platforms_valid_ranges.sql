-- SQLMesh Test: fct_platforms avg_rating and total_games bounds
-- Validates aggregated metrics are within expected ranges

SELECT
  COUNT(*) AS rows_with_issues,
  SUM(CASE WHEN avg_rating < 0.0 OR avg_rating > 5.0 THEN 1 ELSE 0 END) AS invalid_avg_ratings,
  SUM(CASE WHEN total_games < 0 THEN 1 ELSE 0 END) AS negative_total_games
FROM marts.fct_platforms
WHERE 1 = 1;

-- Expected: 0 rows with issues (all counts should be 0)