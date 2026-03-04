"""Logging configuration for the Gaming Analytics Pipeline."""

import logging
import sys
from pathlib import Path

try:
    from rich.logging import RichHandler

    HAS_RICH = True
except ImportError:
    HAS_RICH = False


def setup_logging(level: str = "INFO") -> None:
    """Configure logging for application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Console handler
    if HAS_RICH:
        console_handler: logging.Handler = RichHandler(
            rich_tracebacks=True,
            show_time=True,
            show_path=False,
        )
    else:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)

    # File handler (always log to file at DEBUG level)
    file_handler = logging.FileHandler(log_dir / "pipeline.log")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # Set specific logger levels
    logging.getLogger("dlt").setLevel(logging.WARNING)
    logging.getLogger("prefect").setLevel(logging.WARNING)
    logging.getLogger("sqlmesh").setLevel(logging.WARNING)
    logging.getLogger("soda").setLevel(logging.WARNING)
