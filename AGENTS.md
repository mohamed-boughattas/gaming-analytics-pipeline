# AGENTS.md

## Requirements

- Python 3.12–3.13 (`requires-python = ">=3.12,<3.14"`, `.python-version` pins `3.12`)
- [uv](https://github.com/astral-sh/uv) package manager
- [Taskfile](https://taskfile.dev) (`brew install go-task`)

## Entry Points

- **Pipeline run**: `task run` (or `uv run python main.py`)
- **Marimo**: `task marimo`
- **Evidence**: `task evidence` (Node 22 required via fnm)
- **SQLMesh**: `task sqlmesh-plan|apply|test|lint` (Taskfile handles `cd sqlmesh` automatically)

## Dev Commands

```bash
task install        # uv sync
task lint          # uv run ruff check src/ tests/
task format        # uv run ruff format src/ tests/
task typecheck     # uv run ty check src/
task test          # uv run pytest tests/ -v --no-cov (fast, no coverage)
task test-cov      # uv run pytest tests/ -v --cov=src --cov-report=term-missing
task sqlmesh-lint   # cd sqlmesh && uv run sqlmesh lint
task sqlmesh-test  # cd sqlmesh && uv run sqlmesh test --verbose
task sqlmesh-plan  # cd sqlmesh && uv run sqlmesh plan
task sqlmesh-apply # cd sqlmesh && uv run sqlmesh plan --auto-apply
task lint-full     # format → lint → lint-security → typecheck → sqlmesh-lint → lint-yaml
task soda-scan     # uv run python -m gaming_pipeline.quality
task db-reset      # deletes DuckDB + SQLMesh cache (requires interactive TTY, type 'yes' to confirm)
```

## CI

`task lint-full` auto-formats with `ruff format`; CI runs `ruff format --check` (read-only). Run `task lint-full` locally before committing.

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
- Evidence requires Node 22 (use `fnm use 22` or `task evidence` handles this)
- SQLMesh gateway name is `local` (not `duckdb`); database path in `sqlmesh.yaml` is **absolute** — must be updated per developer
- SQLMesh tests are `.sql` files in `sqlmesh/tests/` using `-- Expected: 0` assertion pattern, run via `task sqlmesh-test` (not pytest)
- Soda quality uses `verify_contract_locally` (Soda Core v4 contract API), not SodaCL scan files
- Soda `data_source.yaml` uses relative path — `task soda-scan` must run from repo root
- bare `pytest` runs with coverage by default (pyproject.toml `addopts`); use `task test` for fast runs or `pytest --no-cov` explicitly
- yamllint ignores `.github/` and `sqlmesh/` — CI YAML and SQLMesh config are not linted by yamllint
- `lint` already includes `S` (security) rules via ruff config; `lint-security` is a redundant explicit pass — both run in `lint-full`
- pytest `integration` marker requires a running Prefect server; skip with `pytest -m "not integration"`

## Conventions

- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/) — `feat:`, `fix:`, `docs:`, `test:`, `chore:`
- **Docstrings**: Google-style
- **Type hints**: Required; use `ty` (astral-sh/ty), not mypy
- **DuckDB paths**: Use `read_only=True` for concurrent read access
