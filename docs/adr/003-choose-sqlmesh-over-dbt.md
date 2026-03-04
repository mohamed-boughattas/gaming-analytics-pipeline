# ADR 003: Choose SQLMesh over dbt

## Status

Accepted

## Context

We needed to select a data transformation tool for managing SQL-based transformations. Requirements include:

- SQL-based transformation language
- Support for incremental loads
- Data versioning and lineage
- Local development experience
- Integration with DuckDB

## Decision

We selected **SQLMesh** as our transformation tool over dbt.

## Rationale

### Advantages of SQLMesh

1. **DuckDB Native**: First-class support for DuckDB (dbt's DuckDB adapter is less mature)
2. **Virtual Environments**: Better isolation and versioning of transformations
3. **Forward/Backward Compatibility**: Can run multiple versions of transformations simultaneously
4. **Integrated Planning**: Built-in deployment planning and validation
5. **Python Integration**: Better Python integration for custom transformations
6. **State Management**: More sophisticated state handling and dependencies
7. **Incremental Updates**: Better support for incremental materialization strategies
8. **Schema Evolution**: Better handling of schema changes over time

### Why Not dbt?

While dbt is the industry standard with a larger ecosystem, for this project:

- DuckDB adapter is less mature than other database adapters
- Requires additional setup for local development
- More focused on production data warehouses (Snowflake, BigQuery)
- Less native support for the workflow patterns we need
- Heavier infrastructure requirements

### Specific Use Case Considerations

For a gaming analytics portfolio project with DuckDB:

- SQLMesh provides better DuckDB integration out of the box
- More modern architecture with Python 3.12 support
- Better demonstrates understanding of newer data engineering tools
- Simpler local development experience

## Consequences

- **Positive**: Better DuckDB integration and performance
- **Positive**: More advanced versioning and deployment features
- **Positive**: Modern, Pythonic approach to transformations
- **Neutral**: Smaller community and fewer third-party integrations
- **Negative**: Less ecosystem and fewer pre-built packages
- **Neutral**: Less familiarity in the job market (but demonstrates forward-thinking)

## Alternatives Considered

1. **dbt**: Industry standard, but less optimized for DuckDB
2. **SQLGlot**: Excellent for SQL translation, but no orchestration
3. **Custom Python**: Too much work to build from scratch
4. **Apache Spark**: Overkill for this dataset size

## References

- [SQLMesh Documentation](https://sqlmesh.com/)
- [dbt Documentation](https://docs.getdbt.com/)
- [SQLMesh vs dbt](https://sqlmesh.com/docs/learn/SQLMesh_vs_dbt/)
