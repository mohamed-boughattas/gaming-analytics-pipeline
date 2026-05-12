# ADR 005: Choose dlt over Custom Scripts, Fivetran, and Airbyte

## Status

Accepted

## Context

We needed a data ingestion framework for loading gaming data from the RAWG API into DuckDB. Requirements included:

- Automatic retry and exponential backoff on API failures
- Rate limiting support to avoid hitting RAWG API limits
- Pagination handling for API endpoints that return paginated results
- Schema inference for dynamic RAWG API responses
- Incremental loading with checkpoint persistence to avoid re-fetching data on pipeline restart
- No duplicate data on re-runs (merge semantics for games)
- Local development without cloud infrastructure

## Decision

We selected **dlt** (Data Load Tool) as our ingestion framework.

## Rationale

### Advantages of dlt

1. **Code-Defined Sources**: Sources are Python classes/functions, not YAML configs — easier to version control and test
2. **Incremental Loading**: Built-in `dlt.incremental` with state persistence between runs; resumes from last checkpoint on failure
3. **Automatic Schema Inference**: dlt infers and adapts schema from API responses; supports nested JSON normalization into child tables via `_dlt_id` / `_dlt_root_id`
4. **Merge Disposition**: Write disposition `merge` on `games` resource prevents duplicates; `replace` for reference data (`genres`, `platforms`)
5. **No Infrastructure**: Runs locally without a separate server or cloud service
6. **DuckDB Destination**: First-class `dlt.destinations.duckdb` support with automatic schema creation

### Why Not Alternatives?

| Alternative | Reason Rejected |
|---|---|
| **Custom `requests` scripts** | Manual retry logic, pagination, checkpointing; reinventing the wheel |
| **Fivetran** | Cloud-hosted, too heavy for a local portfolio project; no local dev experience |
| **Airbyte** | Requires Docker + separate orchestration; overkill for DuckDB-only stack |
| **Singer taps** | Poor DuckDB destination support; less active development |
| ** pandas / `pd.read_json`** | No incremental loading, no schema evolution, no checkpointing |

### Specific Implementation Details

The RAWG source uses:
- `dlt.incremental` on the `updated` field for games — fetches only records modified since last run
- `write_disposition="merge"` for games (upsert by `primary_key="id"`)
- `write_disposition="replace"` for genres and platforms (full reload on each run)
- `requests.get` with timeout + raise_for_status for API calls
- dlt normalizes nested `genres` and `platforms` arrays into child tables (`raw.games__genres`, `raw.games__platforms`) linked via `_dlt_id` / `_dlt_root_id`

## Consequences

- **Positive**: Pipeline resumes from checkpoint on failure — no wasted API calls
- **Positive**: Schema inference handles RAWG API changes without manual migration
- **Positive**: Child table normalization enables proper JOINs in SQLMesh mart models
- **Neutral**: Requires Python source code (not YAML) — slightly higher learning curve for non-Python users
- **Neutral**: dlt's `templater = raw` conflict with sqlfluff requires disabling template parsing in `.sqlfluff`
- **Negative**: Less community support compared to Airbyte or Fivetran (but sufficient for this use case)

## Alternatives Considered

1. **Custom Python scripts**: Too much boilerplate for retry, pagination, and checkpointing
2. **Fivetran**: Cloud-native, requires account setup, no local dev story
3. **Airbyte**: Requires Docker containers and separate orchestration; overkill for DuckDB-only pipeline
4. **Singer**: Less active maintenance, limited DuckDB destination ecosystem
5. **pandas/scripts**: No incremental state, no schema evolution, manual error handling

## References

- [dlt Documentation](https://dlthub.com/docs)
- [dlt REST API source](https://dlthub.com/docs/dlt-ecosystem/dlt-sources/rest-api)
- [dlt destinations — DuckDB](https://dlthub.com/docs/dlt-ecosystem/destinations/duckdb)
- [dlt write dispositions](https://dlthub.com/docs/general/writing-dispositions)