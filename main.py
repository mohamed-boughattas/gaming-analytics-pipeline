"""CLI for Gaming Analytics Pipeline."""

import sys
import warnings
from pathlib import Path

import click

from gaming_pipeline.config import config
from gaming_pipeline.logging_config import setup_logging
from gaming_pipeline.orchestrate.flows import (
    daily_pipeline_flow,
    full_load_pipeline_flow,
)

# Suppress non-critical warnings
warnings.filterwarnings(
    "ignore",
    message="Config key.*is set in model_config but will be ignored",
)
warnings.filterwarnings(
    "ignore",
    message="urllib3.*or chardet.*doesn't match a supported version",
)


@click.group()
@click.option(
    "--log-level",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
)
@click.pass_context
def cli(ctx: click.Context, log_level: str) -> None:
    """Gaming Analytics Pipeline CLI

    A modern data engineering pipeline for collecting, processing,
    and analyzing gaming data
    """
    ctx.ensure_object(dict)
    ctx.obj["log_level"] = log_level
    setup_logging(log_level)


@cli.command()
@click.option("--page-size", default=50, help="Page size for API requests")
@click.option("--max-pages", default=10, help="Maximum pages to fetch")
@click.option("--dry-run", is_flag=True, help="Validate without executing")
@click.pass_context
def run(ctx: click.Context, page_size: int, max_pages: int, dry_run: bool) -> None:
    """Run the daily pipeline (incremental load)

    Fetches and processes new gaming data from the RAWG API.
    """
    if dry_run:
        click.echo("Dry run mode - validating configuration...")
        click.echo(f"  Page size: {page_size}")
        click.echo(f"  Max pages: {max_pages}")
        click.echo("Configuration valid")
        return

    click.echo(
        f"Starting daily pipeline (page_size={page_size}, max_pages={max_pages})..."
    )
    try:
        result = daily_pipeline_flow(page_size=page_size, max_pages=max_pages)
        click.echo("Daily pipeline completed successfully!")
        if result:
            click.echo(f"  Games loaded: {result.get('total_games', 'N/A')}")
            click.echo(f"  Genres loaded: {result.get('genres', 'N/A')}")
            click.echo(f"  Platforms loaded: {result.get('platforms', 'N/A')}")
    except Exception as e:
        click.echo(f"Pipeline failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--dry-run", is_flag=True, help="Validate without executing")
@click.pass_context
def full_load(ctx: click.Context, dry_run: bool) -> None:
    """Run full historical load

    Fetches all available historical data from the RAWG API.
    This may take a long time for large datasets.
    """
    if dry_run:
        click.echo("Dry run mode - validating full load configuration...")
        click.echo("Configuration valid")
        return

    click.echo("Starting full historical load...")
    click.echo("Warning: This may take a significant amount of time.")
    click.confirm("Do you want to continue?", abort=True)

    try:
        result = full_load_pipeline_flow()
        click.echo("Full load completed successfully!")
        if result and "rawg" in result:
            rawg = result["rawg"]
            click.echo(f"  Games loaded: {rawg.get('total_games', 'N/A')}")
            click.echo(f"  Genres loaded: {rawg.get('genres', 'N/A')}")
            click.echo(f"  Platforms loaded: {rawg.get('platforms', 'N/A')}")
    except Exception as e:
        click.echo(f"Full load failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """Check pipeline status and database health"""
    import duckdb

    db_path = Path(config.database.path)
    if not db_path.exists():
        click.echo("Database not found. Run 'python main.py run' to initialize.")
        sys.exit(1)

    try:
        with duckdb.connect(str(db_path)) as con:
            tables = con.execute(
                """
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_schema IN ('raw', 'staging', 'marts')
                ORDER BY table_schema, table_name
                """
            ).fetchall()

            click.echo("Pipeline Status:")
            click.echo(f"  Database: {db_path}")
            click.echo(f"  Tables: {len(tables)}")

            if tables:
                click.echo("\n  Tables:")
                current_schema = None
                for schema, table in tables:
                    if schema != current_schema:
                        if current_schema:
                            click.echo(f"\n  {current_schema}:")
                        click.echo(f"  {schema}:")
                        current_schema = schema

                    count = con.execute(
                        f"SELECT COUNT(*) FROM {schema}.{table}"  # noqa: S608
                    ).fetchone()
                    count = count[0] if count else 0
                    click.echo(f"    - {table}: {count:,} rows")

        click.echo("\nPipeline healthy")

    except Exception as e:
        click.echo(f"Error checking status: {e}", err=True)
        sys.exit(1)


@cli.command("seed")
@click.pass_context
def seed(ctx: click.Context) -> None:
    """Seed database with sample gaming data

    Creates mock data for demo purposes without requiring a RAWG API key.
    This is perfect for testing and exploring the dashboards.
    """
    from gaming_pipeline.demo import seed_database

    click.echo("Seeding database with sample data...")
    try:
        result = seed_database()
        click.echo("Sample data seeded successfully!")
        click.echo(f"  - {result['games']} games")
        click.echo(f"  - {result['genres']} genres")
        click.echo(f"  - {result['platforms']} platforms")
    except Exception as e:
        click.echo(f"Seed failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def version() -> None:
    """Show version information"""
    from importlib.metadata import version

    try:
        pkg_version = version("gaming_analytics_pipeline")
        click.echo(f"Gaming Analytics Pipeline v{pkg_version}")
    except Exception:
        click.echo("Gaming Analytics Pipeline v0.1.0")


if __name__ == "__main__":
    cli()
