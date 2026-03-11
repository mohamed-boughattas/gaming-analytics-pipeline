# API Reference

This document provides detailed API documentation for the Gaming Analytics Pipeline.

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RAWG_API_KEY` | RAWG API key for data fetching | Required |
| `DATABASE_PATH` | Path to DuckDB database | `data/gaming_analytics.duckdb` |
| `ENVIRONMENT` | Runtime environment | `development` |
| `BATCH_SIZE` | Batch size for processing | `100` |
| `MAX_RETRIES` | Maximum retry attempts | `3` |
| `PREFECT_API_URL` | Prefect API server URL | `http://localhost:4200/api` |

## Python API

### Data Extraction

#### `rawg_source()`

Creates a dlt source for extracting data from the RAWG API.

```python
from gaming_pipeline.extract.dlt_source import rawg_source

source = rawg_source(
    page_size=20,        # Items per page (max 100)
    max_pages=None,      # Maximum pages to fetch
    updated_after=None   # ISO date for incremental loading
)
```

#### `DefaultExtractors`

Backwards-compatible extractor class.

```python
from gaming_pipeline.extract.base import DefaultExtractors

extractors = DefaultExtractors()
genres = await extractors.extract_genres()
platforms = await extractors.extract_platforms()
```

**Note:** These methods return empty lists. Use `GamingPipeline.load_rawg_data()` for actual extraction.

---

### Data Loading

#### `GamingPipeline`

Main pipeline class for loading data into DuckDB.

```python
from gaming_pipeline.load.pipeline import GamingPipeline

pipeline = GamingPipeline(
    destination=None,           # Optional custom destination
    dataset_name="gaming_analytics"  # Dataset name
)
```

##### Methods

###### `load_rawg_data()`

Load RAWG data into DuckDB.

```python
stats = await pipeline.load_rawg_data(
    page_size=20,
    max_pages=10,
    updated_after="2024-01-01"  # Optional ISO date
)
```

Returns:
```python
{
    "total_games": 500,
    "genres": 20,
    "platforms": 10
}
```

###### `run_full_load()`

Run full historical data load.

```python
result = await pipeline.run_full_load()
```

Returns:
```python
{
    "rawg": {"total_games": 500, "genres": 20, "platforms": 10},
    "timestamp": "2024-01-01T12:00:00Z"
}
```

###### `get_schema()`

Get current pipeline schema.

```python
schema = pipeline.get_schema()
```

###### `get_load_info()`

Get information about last load.

```python
info = pipeline.get_load_info()
```

---

### Data Quality

#### `SQLMeshRunner`

Runner for SQLMesh transformations.

```python
from gaming_pipeline.transform.sqlmesh_runner import SQLMeshRunner

runner = SQLMeshRunner()
result = runner.apply()
```

##### Methods

- `plan(**kwargs)` - Preview changes without applying
- `apply(**kwargs)` - Apply transformations
- `test()` - Run SQLMesh tests

#### `SodaScanner`

Scanner for Soda Core data quality checks.

```python
from gaming_pipeline.quality.checks import SodaScanner

scanner = SodaScanner()
result = scanner.run_checks(contract_path=Path("checks/marts.yml"))
```

---

### Orchestration

#### Prefect Flows

##### `daily_pipeline_flow()`

Daily incremental pipeline.

```python
from gaming_pipeline.orchestrate.flows import daily_pipeline_flow

result = await daily_pipeline_flow(
    page_size=50,
    max_pages=10,
    updated_after_days=1
)
```

##### `full_load_pipeline_flow()`

Full historical data load.

```python
from gaming_pipeline.orchestrate.flows import full_load_pipeline_flow

result = await full_load_pipeline_flow(
    page_size=100,
    max_pages=50
)
```

---

### CLI Commands

#### `python main.py run`

Run daily pipeline.

```bash
python main.py run --page-size=50 --max-pages=10
```

Options:
- `--page-size`: Items per page (default: 50)
- `--max-pages`: Maximum pages (default: 10)
- `--dry-run`: Validate without executing

#### `python main.py full-load`

Run full historical load.

```bash
python main.py full-load
```

#### `python main.py status`

Check pipeline status.

```bash
python main.py status
```

#### `python main.py seed`

Seed database with sample data.

```bash
python main.py seed
```

---

## Data Schemas

### Raw Layer

| Table | Description |
|-------|-------------|
| `raw.rawg_games` | Raw game data from RAWG API |
| `raw.rawg_genres` | Genre reference data |
| `raw.rawg_platforms` | Platform reference data |

### Staging Layer

| Table | Description |
|-------|-------------|
| `staging.stg_games` | Cleaned game data with type casting |
| `staging.stg_genres` | Cleaned genre data |
| `staging.stg_platforms` | Cleaned platform data |

### Marts Layer

| Table | Description |
|-------|-------------|
| `marts.games` | Enriched games with rating categories |
| `marts.genres` | Genre analytics |
| `marts.platforms` | Platform analytics |

---

## Error Handling

All pipeline methods return error information in their response dict:

```python
result = await pipeline.load_rawg_data()
if "error" in result:
    print(f"Pipeline error: {result['error']}")
```

Common errors:
- `API key missing`: Set `RAWG_API_KEY` environment variable
- `Connection failed`: Check network connectivity
- `Rate limited`: Wait and retry (dlt handles automatically)
