# SQLMesh Tests

This directory contains SQLMesh native tests for data quality validation.

## Running Tests

SQLMesh tests can be run as part of the SQLMesh workflow:

```bash
# Run all SQLMesh tests
make sqlmesh-test

# Or directly with sqlmesh
uv run sqlmesh test
```

## Test Files

| File | Purpose | Expected Result |
|------|---------|----------------|
| `test_no_null_game_names.sql` | Ensures all games have names | 0 NULL names |
| `test_rating_ranges.sql` | Validates ratings are in 0-10 range | 0 invalid ratings |
| `test_engagement_score_positive.sql` | Validates engagement_score is non-negative | 0 negative scores |

## Writing New Tests

SQLMesh tests are SQL queries that:
1. Return a count of records failing the test
2. Expected result is 0 (no failures)
3. Can be run against any environment (dev, test, prod)

Example test pattern:

```sql
-- Ensure all IDs are unique
SELECT COUNT(*) - COUNT(DISTINCT id) AS duplicate_ids
FROM gaming_analytics.marts_games;

-- Expected: 0
```

## Integration with Soda Core

SQLMesh tests complement Soda Core checks:
- **Soda Core**: Run in CI/CD for pipeline validation
- **SQLMesh Tests**: Part of transformation validation workflow

Both should be used together for comprehensive data quality.
