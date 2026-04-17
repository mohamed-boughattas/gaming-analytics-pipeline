# SQLMesh Tests

This directory contains SQLMesh native tests for data quality validation.

## Running Tests

```bash
just sqlmesh-test
```

## Test Files

| File | Purpose | Expected Result |
|---|---|---|
| `test_no_future_release_dates.sql` | No release dates in the future | 0 future releases |
| `test_no_null_game_names.sql` | All games have names | 0 NULL names |
| `test_rating_ranges.sql` | Ratings in 0-5 range | 0 invalid ratings |
| `test_engagement_score_positive.sql` | Engagement score >= 0 | 0 negative scores |
| `test_fct_genres_no_null_names.sql` | All genres have names | 0 NULL names |
| `test_fct_genres_valid_ranges.sql` | Genre aggregations in valid range | 0 rows with issues |
| `test_fct_platforms_no_null_names.sql` | All platforms have names | 0 NULL names |
| `test_fct_platforms_valid_ranges.sql` | Platform aggregations in valid range | 0 rows with issues |

## Writing New Tests

SQLMesh tests are SQL queries that:

1. Return a count of records failing the test
2. Expected result is 0 (no failures)

Example test pattern:

```sql
-- Ensure all IDs are unique
SELECT COUNT(*) - COUNT(DISTINCT id) AS duplicate_ids
FROM marts.fct_games;

-- Expected: 0
```

## Integration with Soda Core

SQLMesh tests complement Soda Core checks:

- **Soda Core**: Declarative column-level contracts
- **SQLMesh Tests**: Business logic and transformation validation

Both are used together for defense-in-depth data quality.
