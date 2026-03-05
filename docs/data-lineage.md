# Data Lineage Documentation

## Overview

This document describes the data flow and transformations in the Gaming Analytics Pipeline, from API ingestion through to final analytics tables.

## Architecture Diagram

```text
┌─────────────────┐
│   RAWG API      │
│  (Source)       │
└────────┬────────┘
         │
         │ HTTP/JSON
         │
         ▼
┌─────────────────────────────────────────┐
│        Extract Layer                  │
│  ┌────────────────────────────────┐   │
│  │ - extract_rawg_genres()       │   │
│  │ - extract_rawg_platforms()    │   │
│  │ - extract_rawg_games()        │   │
│  └────────────────────────────────┘   │
└────────┬────────────────────────────────┘
         │
         │ JSON Data
         │
         ▼
┌─────────────────────────────────────────┐
│        Load Layer (dlt)              │
│  ┌────────────────────────────────┐   │
│  │ rawg_genres                │   │
│  │ rawg_platforms             │   │
│  │ rawg_games                 │   │
│  └────────────────────────────────┘   │
└────────┬────────────────────────────────┘
         │
         │ DuckDB (gaming_analytics schema)
         │
         ▼
┌─────────────────────────────────────────┐
│     Transform Layer (SQLMesh)         │
│  ┌────────────────────────────────┐   │
│  │ marts_games                 │   │
│  │   - Rating categories       │   │
│  │   - Engagement score        │   │
│  │   - JSON array expansion    │   │
│  ├────────────────────────────────┤   │
│  │ marts_genres               │   │
│  │   - Aggregated metrics      │   │
│  │   - Rating breakdowns       │   │
│  │   - Percentage columns      │   │
│  ├────────────────────────────────┤   │
│  │ marts_platforms             │   │
│  │   - Aggregated metrics      │   │
│  │   - Year ranges            │   │
│  │   - Rating breakdowns       │   │
│  └────────────────────────────────┘   │
└────────┬────────────────────────────────┘
         │
         │ Analytics Tables
         │
         ▼
┌─────────────────────────────────────────┐
│      Visualization Layer               │
│  ┌────────────────────────────────┐   │
│  │ Marimo Dashboard            │   │
│  └────────────────────────────────┘   │
│  ┌────────────────────────────────┐   │
└─────────────────────────────────────────┘
```

## Data Flow Details

### 1. Extraction

**Source**: RAWG API (<https://api.rawg.io/api>)

**Endpoints Used**:

- `/genres` - List all game genres
- `/platforms` - List all gaming platforms
- `/games` - List games with pagination

**Extractors**:

- `extract_rawg_genres()` - Fetches genre metadata
- `extract_rawg_platforms()` - Fetches platform metadata
- `extract_rawg_games()` - Fetches games with configurable pagination

**Rate Limiting**: 5 requests per second (configurable)

### 2. Loading (dlt)

**Destination**: DuckDB

**Schema**: `gaming_analytics`

**Raw Tables**:

#### `rawg_genres`

| Column           | Type    | Description          |
| ---------------- | ------- | -------------------- |
| id               | INTEGER | Primary key          |
| name             | VARCHAR | Genre name           |
| slug             | VARCHAR | URL-friendly name    |
| image_background | VARCHAR | Background image URL |
| games_count      | INTEGER | Total games in genre |

#### `rawg_platforms`

| Column           | Type    | Description              |
| ---------------- | ------- | ------------------------ |
| id               | INTEGER | Primary key              |
| name             | VARCHAR | Platform name            |
| slug             | VARCHAR | URL-friendly name        |
| image            | VARCHAR | Platform image URL       |
| platform_details | JSON    | Year ranges, game counts |

#### `rawg_games`

| Column           | Type      | Description               |
| ---------------- | --------- | ------------------------- |
| id               | INTEGER   | Primary key               |
| name             | VARCHAR   | Game title                |
| slug             | VARCHAR   | URL-friendly name         |
| released         | DATE      | Release date              |
| updated          | TIMESTAMP | Last updated              |
| rating           | FLOAT     | User rating (0-5)         |
| metacritic       | INTEGER   | Metacritic score (0-100)  |
| ratings_count    | INTEGER   | Number of user ratings    |
| genres           | JSON      | Array of genre objects    |
| platforms        | JSON      | Array of platform objects |
| stores           | JSON      | Array of store objects    |
| playtime         | INTEGER   | Average playtime (hours)  |
| background_image | VARCHAR   | Game image URL            |
| ...              | ...       | Additional metadata       |

**Load Strategy**:

- Genres/Platforms: `REPLACE` (full refresh)
- Games: `APPEND` (incremental)

### 3. Transformation (SQLMesh)

#### `marts_games`

**Purpose**: Enrich games with calculated metrics and expand JSON arrays

**Transformations**:

1. Extract genre names from JSON array → `genre_names` (LIST)
2. Extract platform names from JSON array → `platform_names` (LIST)
3. Extract store names from JSON array → `store_names` (LIST)
4. Calculate `rating_category` (Excellent/Good/Average/Below Average/Poor)
5. Extract `release_year` and `release_month` from date
6. Calculate `engagement_score` (weighted formula)
7. Count array lengths for metrics

**Engagement Score Formula**:

```text
engagement_score = (rating * 0.4) + (metacritic/10 * 0.3) + (ratings_count/100 * 0.3)
```

**Model Type**: INCREMENTAL (by `id`)

#### `marts_genres`

**Purpose**: Aggregate metrics per genre

**Transformations**:

1. Explode genre-game relationships from games table
2. Aggregate:
   - `total_games` - Count distinct games
   - `avg_rating`, `avg_metacritic` - Average scores
   - `max_rating`, `min_rating` - Score ranges
   - `total_ratings`, `avg_ratings_per_game` - Rating volume
   - `avg_playtime` - Average gameplay hours
3. Categorize games by quality (excellent/good/average/below_average)
4. Calculate percentages for each quality tier

**Model Type**: FULL (refreshes all data)

#### `marts_platforms`

**Purpose**: Aggregate metrics per platform

**Transformations**:

1. Explode platform-game relationships from games table
2. Extract year ranges from JSON metadata
3. Aggregate same metrics as genres
4. Categorize games by quality
5. Calculate percentages for each quality tier

**Model Type**: FULL (refreshes all data)

### 4. Visualization

**Marimo Dashboard**:

- Interactive Python notebook
- Plotly visualizations
- Real-time data queries
- Local development

## Data Quality Checks

### Soda Core Checks

**Staging Layer** (`src/gaming_pipeline/quality/checks/staging.yml`):

- Row count checks (expect > 0)
- Schema validation
- Null checks on key columns

**Marts Layer** (`src/gaming_pipeline/quality/checks/marts.yml`):

- Aggregation accuracy
- Rating range validation (0-5, 0-100)
- Reference integrity
- Duplicate detection

## Orchestration

**Prefect 3.x**:

- Flow: `gaming-analytics-daily` - Daily incremental load
- Flow: `gaming-analytics-full-load` - Historical load
- Flow: `gaming-analytics-extract-only` - Extraction only
- Flow: `gaming-analytics-load-only` - Loading only

**Schedule**:

- Daily: 6 AM UTC (incremental)
- Weekly: Sunday 2 AM UTC (full load)

## Data Retention

See [data-retention.md](./data-retention.md) for detailed retention policies.

## Key Metrics

| Metric             | Source                   | Update Frequency     |
| ------------------ | ------------------------ | -------------------- |
| Total Games        | rawg_games               | Daily (append)       |
| Avg Rating         | marts_games              | Daily (incremental)  |
| Genre Distribution | marts_genres             | Daily (full refresh) |
| Platform Stats     | marts_platforms          | Daily (full refresh) |
| Engagement Score   | marts_games (calculated) | Daily (incremental)  |

## Dependencies

**External**:

- RAWG API key (required)
- Internet connection (for extraction)

**Internal**:

- DuckDB file must exist
- SQLMesh models must be applied
- Soda checks must pass

## Troubleshooting

### Pipeline Failures

1. **API Rate Limiting**: Increase delay between requests
2. **Missing Tables**: Run SQLMesh plan/apply first
3. **Data Quality Issues**: Review Soda check results
4. **Dashboard Errors**: Ensure marts tables are populated

### Common Issues

- **Empty results**: Check if API key is valid
- **Schema errors**: Verify SQLMesh model syntax
- **Performance**: Reduce page size or max pages
- **Memory issues**: DuckDB file too large - consider partitioning

## Future Enhancements

- Add incremental loading for genres/platforms
- Implement data versioning with SQLMesh
- Add more quality checks
- Real-time streaming support
- Multi-source ingestion (additional APIs)
- Advanced ML models for predictions
