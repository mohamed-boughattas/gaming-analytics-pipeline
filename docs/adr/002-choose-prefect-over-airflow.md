# ADR 002: Choose Prefect over Apache Airflow

## Status

Accepted

## Context

We needed to select an orchestration tool for managing data pipeline workflows. Requirements include:

- Modern Python-native implementation
- Support for async/await patterns
- Easy local development experience
- Potential for cloud deployment
- Good observability and monitoring

## Decision

We selected **Prefect 3.x** as our orchestration tool over Apache Airflow.

## Rationale

### Advantages of Prefect 3.x

1. **Pythonic Design**: Native Python code, no DAG definition files or UI-heavy workflows
2. **Async Support**: Built-in support for async/await patterns
3. **Type Safety**: Strong type hints and IDE support
4. **State Management**: Explicit state handling with better error recovery
5. **Modern Stack**: Active development with Python 3.12 support
6. **Simplicity**: Lower learning curve and faster development
7. **Dynamic Workflows**: Can create dynamic workflows programmatically
8. **Local Development**: Easy to run locally without complex infrastructure

### Why Not Apache Airflow?

While Airflow is industry-standard, for this project:

- Steep learning curve for new users
- Requires significant infrastructure setup
- DAG files can become complex and hard to maintain
- Less intuitive for async workflows
- Heavier resource requirements
- More operational overhead for a demo/portfolio project

### Specific Use Case Considerations

For a gaming analytics portfolio project:

- Prefect's code-first approach is more demonstrable
- Easier to understand for hiring managers reviewing the code
- Better alignment with modern Python data engineering practices
- Simpler to set up and demo

## Consequences

- **Positive**: More maintainable and readable workflow code
- **Positive**: Better developer experience with async support
- **Positive**: Easier to demonstrate understanding in portfolio
- **Neutral**: Smaller community compared to Airflow
- **Negative**: Fewer pre-built operators (but we don't need many)
- **Neutral**: Less mature enterprise features (not needed for this use case)

## Alternatives Considered

1. **Apache Airflow**: Industry standard, but complex and heavy
2. **Dagster**: Great data management, but steeper learning curve
3. **Prefect 2.x**: Previous version, but 3.x has better async support
4. **Temporal**: Excellent for workflows, but overkill for this use case

## References

- [Prefect Documentation](https://docs.prefect.io/)
- [Prefect vs Airflow](https://www.prefect.io/blog/prefect-vs-airflow/)
- [Prefect 3.x Release Notes](https://github.com/PrefectHQ/prefect/releases)
