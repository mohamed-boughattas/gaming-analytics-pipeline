# AGENTS.md

## Requirements

- Python 3.12–3.13 (`requires-python = ">=3.12,<3.14"`)
- [uv](https://github.com/astral-sh/uv) package manager

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
just test          # uv run pytest tests/ -v --no-cov (fast, no coverage)
just test-cov      # uv run pytest tests/ -v --cov=src --cov-report=term-missing
just sqlmesh-lint   # cd sqlmesh && uv run sqlmesh lint
just sqlmesh-test  # cd sqlmesh && uv run sqlmesh test --verbose
just sqlmesh-plan  # cd sqlmesh && uv run sqlmesh plan
just sqlmesh-apply # cd sqlmesh && uv run sqlmesh plan --auto-apply
just lint-full     # format → lint → lint-security → typecheck → sqlmesh-lint → lint-yaml
just soda-scan     # uv run python -m gaming_pipeline.quality
just db-reset      # deletes DuckDB + SQLMesh cache (prompts confirmation)
```

## CI

`just lint-full` auto-formats with `ruff format`; CI runs `ruff format --check` (read-only). Run `just lint-full` locally before committing.

CI has 2 jobs: `lint` (format-check + lint + typecheck + sqlmesh-lint + yamllint) and `test` (pytest with coverage).

## Architecture

```
RAWG API → dlt (loads into raw schema in DuckDB)
                ↓
         DuckDB (raw tables)
                ↓
         SQLMesh (staging views + marts views)
                ↓
         Soda Core (quality checks) + Marimo / Evidence (visualization)
```

**DuckDB schema layers** (all in one DuckDB file):
- `raw.*` — dlt-loaded tables (from RAWG API)
- `staging.*` — SQLMesh VIEWs (type casting, null handling)
- `marts.*` — SQLMesh VIEWs (business logic, derived metrics)

Package: `src/gaming_pipeline/`
  config/     # Pydantic settings from .env
  extract/    # dlt source (dlt_source.py)
  load/      # dlt pipeline wrapper
  orchestrate/  # Prefect flows + tasks
  quality/    # Soda checks (checks.py) + contract YAML files
  (no transform/ — SQLMesh called directly via subprocess)

SQLMesh model locations:
- Staging: `sqlmesh/models/staging/stg_*.sql`
- Marts: `sqlmesh/models/marts/fct_*.sql`
- Config: `sqlmesh/sqlmesh.yaml` — gateway name `local`, connection type `duckdb`

## Important Gotchas

- Python 3.12–3.13 only (`>=3.12,<3.14`)
- Marimo must bind to `0.0.0.0` with `--no-token`
- sqlfluff enforces `capitalisation = lower` — all SQL keywords must be lowercase
- sqlfluff uses `templater = raw` (SQLMesh uses custom Jinja-like syntax, not sqlfluff templates)
- `.env` is gitignored; copy from `.env.example`
- Evidence requires Node 22 (use `fnm use 22` or `just evidence` handles this)
- SQLMesh gateway name is `local` (not `duckdb`); database path in `sqlmesh.yaml` is absolute
- SQLMesh tests are `.sql` files in `sqlmesh/tests/`, run via `just sqlmesh-test` (not pytest)
- Soda quality uses `verify_contract_locally` (Soda Core v4 contract API), not SodaCL scan files
- Soda `data_source.yaml` uses relative path — `just soda-scan` must run from repo root
- bare `pytest` runs with coverage by default (pyproject.toml `addopts`); use `just test` for fast runs or `pytest --no-cov` explicitly
- yamllint ignores `.github/` and `sqlmesh/` — CI YAML and SQLMesh config are not linted by yamllint
- `lint` already includes `S` (security) rules via ruff config; `lint-security` is a redundant explicit pass — both run in `lint-full`
- pytest `integration` marker requires a running Prefect server; skip with `pytest -m "not integration"`

## Conventions

- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/) — `feat:`, `fix:`, `docs:`, `test:`, `chore:`
- **Docstrings**: Google-style
- **Type hints**: Required; use `ty` (astral-sh/ty), not mypy
- **DuckDB paths**: Use `read_only=True` for concurrent read access
