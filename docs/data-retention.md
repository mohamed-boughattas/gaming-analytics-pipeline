# Data Retention Policy

This document defines data retention policies for the Gaming Analytics Pipeline.

## Overview

Data retention is managed to balance:

- Data availability for analytics
- Storage efficiency
- Performance optimization
- Data privacy considerations

## Retention Policies

### Staging Layer (Raw Data)

| Table            | Retention Period | Archive Strategy   | Rationale                                                     |
| ---------------- | ---------------- | ------------------ | ------------------------------------------------------------- |
| `rawg_games`     | 2 years          | Archive to parquet | Games data grows large; keep recent games for active analysis |
| `rawg_genres`    | Indefinite       | N/A                | Small reference data; rarely changes                          |
| `rawg_platforms` | Indefinite       | N/A                | Small reference data; rarely changes                          |

### Mart Layer (Transformed Data)

| Table             | Retention Period | Archive Strategy | Rationale                        |
| ----------------- | ---------------- | ---------------- | -------------------------------- |
| `marts_games`     | 1 year           | Re-computable    | Can be regenerated from raw data |
| `marts_genres`    | 1 year           | Re-computable    | Can be regenerated from raw data |
| `marts_platforms` | 1 year           | Re-computable    | Can be regenerated from raw data |

## Archive Strategy

### Archiving Process

When data reaches its retention limit:

1. **Export**: Export data to Parquet format in `data/archive/`
2. **Compress**: Compress archives to save space
3. **Delete**: Remove old data from active database
4. **Catalog**: Update archive catalog

### Archive Format

```text
data/archive/
├── rawg_games/
│   ├── rawg_games_2023.parquet
│   ├── rawg_games_2022.parquet
│   └── rawg_games_2021.parquet
└── archive_catalog.csv
```

### Archive Catalog

The `archive_catalog.csv` tracks archived data:

```csv
table_name,year,file_path,row_count,created_at,checksum
rawg_games,2023,data/archive/rawg_games/rawg_games_2023.parquet,50000,2024-01-15,abc123
rawg_games,2022,data/archive/rawg_games/rawg_games_2022.parquet,48000,2024-01-15,def456
```

## Cleanup Scripts

### Manual Archive

To manually archive data older than retention period:

```python
from datetime import datetime, timedelta
from pathlib import Path
import duckdb

def archive_old_games(years_to_keep: int = 2):
    """Archive game data older than specified years."""
    cutoff_date = datetime.now() - timedelta(days=365 * years_to_keep)

    # Export old data
    con = duckdb.connect("data/gaming_analytics.duckdb")
    con.execute(f"""
        COPY (
            SELECT * FROM gaming_analytics.rawg_games
            WHERE released < '{cutoff_date.date()}'
        ) TO 'data/archive/rawg_games/rawg_games_{year}.parquet'
        (FORMAT PARQUET)
    """)

    # Delete old data
    con.execute(f"""
        DELETE FROM gaming_analytics.rawg_games
        WHERE released < '{cutoff_date.date()}'
    """)

    con.close()
```

### Automated Archive

A scheduled task can run the archive process:

```bash
# Run archive monthly
0 0 1 * * python scripts/archive_data.py --years 2
```

## Rehydration Process

To restore archived data:

```python
import duckdb

def restore_archive(year: int):
    """Restore archived data for a specific year."""
    archive_path = f"data/archive/rawg_games/rawg_games_{year}.parquet"

    con = duckdb.connect("data/gaming_analytics.duckdb")
    con.execute(f"""
        INSERT INTO gaming_analytics.rawg_games
        SELECT * FROM read_parquet('{archive_path}')
    """)
    con.close()
```

## Monitoring

### Storage Monitoring

Track database and archive sizes:

```python
import os
from pathlib import Path

def get_storage_stats():
    """Get storage statistics."""
    db_size = os.path.getsize("data/gaming_analytics.duckdb") / (1024 * 1024)  # MB
    archive_size = sum(
        os.path.getsize(f) for f in Path("data/archive").rglob("*") if f.is_file()
    ) / (1024 * 1024)  # MB

    return {
        "database_mb": db_size,
        "archive_mb": archive_size,
        "total_mb": db_size + archive_size
    }
```

### Alerts

Set up alerts for:

- Database size exceeding threshold (e.g., 5GB)
- Archive directory size exceeding threshold (e.g., 10GB)
- Failed archive operations

## Data Deletion Requests

For data deletion requests (e.g., GDPR):

1. Identify affected records
2. Archive before deletion (for audit trail)
3. Delete from staging and marts
4. Update catalog
5. Generate deletion report

## Configuration

Retention policies can be configured via environment variables:

```bash
# .env
RETENTION_GAMES_YEARS=2
RETENTION_MARTS_YEARS=1
ARCHIVE_ENABLED=true
ARCHIVE_PATH=data/archive
```

## Compliance

- **GDPR**: Support right to erasure
- **Data Minimization**: Keep only necessary data
- **Audit Trail**: Maintain archive catalog
- **Documentation**: Document all retention policies

## Review Schedule

Review retention policies annually or when:

- Data volume increases significantly
- New compliance requirements emerge
- Business needs change
- Storage costs increase

## Emergency Retention

In case of emergency (e.g., data corruption):

- Keep recent backups for 30 days
- Archive all data before major changes
- Maintain audit logs indefinitely
