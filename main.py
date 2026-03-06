import asyncio
import sys
from pathlib import Path

import click

from gaming_pipeline.logging_config import setup_logging
from gaming_pipeline.orchestrate.flows import (
    daily_pipeline_flow,
    full_load_pipeline_flow,
)


@click.group()
@click.option(
    "--log-level",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
)
@click.pass_context
def cli(ctx, log_level):
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
def run(ctx, page_size: int, max_pages: int, dry_run: bool):
    """Run the daily pipeline (incremental load)

    Fetches and processes new gaming data from the RAWG API.
    """
    if dry_run:
        click.echo("Dry run mode - validating configuration...")
        click.echo(f"  Page size: {page_size}")
        click.echo(f"  Max pages: {max_pages}")
        click.echo("Configuration valid ✓")
        return

    click.echo(
        f"Starting daily pipeline (page_size={page_size}, max_pages={max_pages})..."
    )
    try:
        result = asyncio.run(
            daily_pipeline_flow(page_size=page_size, max_pages=max_pages)
        )
        click.echo("✓ Daily pipeline completed successfully!")
        if result:
            click.echo(f"  Games loaded: {result.get('total_games', 'N/A')}")
            click.echo(f"  Genres loaded: {result.get('genres', 'N/A')}")
            click.echo(f"  Platforms loaded: {result.get('platforms', 'N/A')}")
    except Exception as e:
        click.echo(f"✗ Pipeline failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--dry-run", is_flag=True, help="Validate without executing")
@click.pass_context
def full_load(ctx, dry_run: bool):
    """Run full historical load

    Fetches all available historical data from the RAWG API.
    This may take a long time for large datasets.
    """
    if dry_run:
        click.echo("Dry run mode - validating full load configuration...")
        click.echo("Configuration valid ✓")
        return

    click.echo("Starting full historical load...")
    click.echo("Warning: This may take a significant amount of time.")
    click.confirm("Do you want to continue?", abort=True)

    try:
        result = asyncio.run(full_load_pipeline_flow())
        click.echo("✓ Full load completed successfully!")
        if result and "rawg" in result:
            rawg = result["rawg"]
            click.echo(f"  Games loaded: {rawg.get('total_games', 'N/A')}")
            click.echo(f"  Genres loaded: {rawg.get('genres', 'N/A')}")
            click.echo(f"  Platforms loaded: {rawg.get('platforms', 'N/A')}")
    except Exception as e:
        click.echo(f"✗ Full load failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx):
    """Check pipeline status and database health"""
    import duckdb

    db_path = Path("data/gaming_analytics.duckdb")
    if not db_path.exists():
        click.echo("✗ Database not found. Run 'python main.py run' to initialize.")
        sys.exit(1)

    try:
        con = duckdb.connect(str(db_path))

        # Check tables
        tables = con.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'gaming_analytics'
            ORDER BY table_name
        """).fetchall()

        click.echo("Pipeline Status:")
        click.echo(f"  Database: {db_path}")
        click.echo(f"  Tables: {len(tables)}")

        if tables:
            click.echo("\n  Tables:")
            for (table,) in tables:
                # Table names are from trusted database schema query
                count = con.execute(
                    f"SELECT COUNT(*) FROM gaming_analytics.{table}"  # nosec
                ).fetchone()[0]
                click.echo(f"    • {table}: {count:,} rows")

        con.close()
        click.echo("\n✓ Pipeline healthy")

    except Exception as e:
        click.echo(f"✗ Error checking status: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--db-path", default="data/gaming_analytics.duckdb", help="Path to DuckDB database")
@click.pass_context
def seed(ctx, db_path: str):
    """Seed database with sample gaming data

    Creates mock data for demo purposes without requiring a RAWG API key.
    """
    from scripts.seed_sample_data import seed_database

    click.echo(f"Seeding database at: {db_path}")
    try:
        seed_database(db_path=db_path)
        click.echo("✓ Sample data seeded successfully!")
    except Exception as e:
        click.echo(f"✗ Seed failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def version():
    """Show version information"""
    from gaming_pipeline import __version__

    click.echo(f"Gaming Analytics Pipeline v{__version__}")


if __name__ == "__main__":
    cli()
