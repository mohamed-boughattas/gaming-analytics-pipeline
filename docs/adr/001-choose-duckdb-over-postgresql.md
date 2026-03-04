# ADR 001: Choose DuckDB over PostgreSQL

## Status

Accepted

## Context

We needed to select a database for storing and analyzing gaming data from the RAWG API. The primary use cases include:

- Storing raw API responses
- Running analytical queries for dashboards
- Supporting development and testing workflows
- Potential cloud deployment options

## Decision

We selected **DuckDB** as our primary database over PostgreSQL.

## Rationale

### Advantages of DuckDB

1. **Zero Configuration**: No need to manage a separate database server process
2. **Embedded**: Database is a single file, simplifying deployment and backups
3. **Performance**: Excellent performance for analytical workloads on local data
4. **Portability**: Easy to move databases between environments
5. **Cost**: Free, no infrastructure costs for local development
6. **Integration**: Native Python integration with pandas and arrow
7. **Development Experience**: Faster iteration during development

### Why Not PostgreSQL?

While PostgreSQL is a robust production database, for this use case:

- Overkill for local development and demo scenarios
- Requires additional infrastructure setup
- Higher operational complexity
- No significant advantage for analytical workloads on this dataset size

### MotherDuck Integration

We maintain the option to use MotherDuck for cloud deployment, which provides:

- DuckDB compatibility (no migration needed)
- Serverless scaling
- Easy sharing and collaboration

## Consequences

- **Positive**: Simplified development workflow, easier demos, lower costs
- **Positive**: Fast analytical queries for dashboard
- **Neutral**: Need to consider scale limits (can migrate to PostgreSQL if needed)
- **Negative**: Not suitable for high-concurrency transactional workloads
- **Neutral**: Trade-off between operational simplicity and production scalability

## Alternatives Considered

1. **PostgreSQL**: More mature for production, but higher operational overhead
2. **SQLite**: Too limited for analytical workloads
3. **ClickHouse**: Excellent for analytics, but overkill for this use case
4. **BigQuery**: Great for scale, but overkill and higher costs

## References

- [DuckDB Documentation](https://duckdb.org/)
- [MotherDuck](https://motherduck.com/)
- [DuckDB vs PostgreSQL](https://duckdb.org/2021/10/22/duckdb-vs-postgresql.html)
