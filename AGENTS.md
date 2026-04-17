# AGENTS.md

## Entry Points

- **Pipeline run**: `uv run python main.py`
- **Marimo**: `uv run marimo edit marimo/gaming_analytics.py --headless --host 0.0.0.0 --port 2718 --no-token`
- **Evidence**: `just evidence` (Node 22 required via fnm)
- **SQLMesh**: Must `cd sqlmesh` first: `cd sqlmesh && uv run sqlmesh <plan|apply|test|lint>`

## Dev Commands

```bash
just install        # uv sync
just lint          # uv run ruff check src/ tests/ (includes --select S)
just format        # uv run ruff format src/ tests/
just typecheck     # uv run ty check src/
just test         # uv run pytest tests/ -v --no-cov
just test-cov    # uv run pytest tests/ -v --cov=src --cov-report=term-missing
just sqlmesh-lint   # cd sqlmesh && uv run sqlmesh lint
just sqlmesh-test  # cd sqlmesh && uv run sqlmesh test --verbose
just sqlmesh-plan  # cd sqlmesh && uv run sqlmesh plan
just sqlmesh-apply # cd sqlmesh && uv run sqlmesh plan --auto-apply
just lint-full     # just format → lint → typecheck → sqlmesh-lint → lint-yaml
just soda-scan     # uv run python -m gaming_pipeline.quality.checks
```

## CI Order

`just lint-full` runs: format → lint → typecheck → sqlmesh-lint → lint-yaml

CI has 2 jobs: `lint` (lint + typecheck + sqlmesh-lint) and `test`.

## Architecture

```
RAWG API → dlt (extract/load) → DuckDB → SQLMesh (transform)
                                                      → Soda Core (quality checks)
                                                      → Marimo / Evidence (visualization)

Package: src/gaming_pipeline/
  config/     # Pydantic settings from .env
  extract/    # dlt source (dlt_source.py)
  load/      # dlt pipeline wrapper
  orchestrate/  # Prefect flows + tasks
  quality/    # Soda checks (checks.py) + contract YAML files
  demo/       # seed_database.py (demo mode without API key)
  (no transform/ — SQLMesh called directly via subprocess)
```

## SQLMesh Model Locations

- Staging: `sqlmesh/models/staging/stg_*.sql`
- Marts: `sqlmesh/models/marts/fct_*.sql`

SQLMesh config: `sqlmesh/sqlmesh.yaml` — dialect `duckdb`, gateway `local`.

## Important Gotchas

- Marimo must bind to `0.0.0.0` with `--no-token`
- sqlfluff excludes `tests/sqlmesh/`
- sqlfluff enforces `capitalisation = lower` — all SQL keywords must be lowercase
- `.env` is gitignored; copy from `.env.example`
- Evidence requires Node 22 (use `fnm use 22` or `just evidence` handles this)
- SQLMesh gateway is `duckdb` (local file); path in `sqlmesh/sqlmesh.yaml` must be absolute (resolved relative to `sqlmesh/` dir)

## Conventions

- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/) — `feat:`, `fix:`, `docs:`, `test:`, `chore:`
- **Docstrings**: Google-style
- **Type hints**: Required; use `ty` (astral-sh/ty), not mypy
- **DuckDB paths**: Use `read_only=True` for concurrent read access
- **Secrets**: Never commit secrets to the repository
