"""Soda Core checks for gaming analytics pipeline."""

import logging
from typing import Any

from soda.scan import Scan

from gaming_pipeline.config import config

logger = logging.getLogger(__name__)


def run_soda_checks(
    data_source_name: str = "gaming_analytics",
    checks_path: str | None = None,
    configuration_file: str | None = None,
    variables: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Run Soda Core data quality checks.

    Args:
        data_source_name: Name of the data source
        checks_path: Path to checks directory
        configuration_file: Path to Soda configuration file
        variables: Variables for dynamic configuration

    Returns:
        Dictionary with scan results
    """
    logger.info(f"Running Soda Core checks for {data_source_name}")

    # Initialize scan
    scan = Scan()

    # Set scan properties
    scan.set_scan_definition_name("gaming-analytics-data-quality")
    scan.set_data_source_name(data_source_name)

    # Set configuration file
    config_file = configuration_file or config.soda.configuration_file
    if config_file:
        scan.add_configuration_yaml_file(config_file)

    # Add variables
    scan_variables = variables or {}
    scan_variables.update(
        {
            "schema": "main",
            "table_prefix": "rawg_",
            "date_column": "released",
            "rating_column": "rating",
            "id_column": "id",
        }
    )

    for key, value in scan_variables.items():
        scan.add_variables({key: value})

    # Add checks
    checks_dir = checks_path or config.soda.checks_path
    if checks_dir:
        scan.add_sodacl_yaml_files(checks_dir)

    # Execute scan
    scan_result = scan.execute()

    # Get results
    results = {
        "scan_result": scan_result,
        "logs": scan.get_logs_text(),
        "failed_checks": scan_result.get_fail_results_count()  # type: ignore[call-non-callable]
        if hasattr(scan_result, "get_fail_results_count")
        else 0,
        "passed_checks": scan_result.get_pass_results_count()  # type: ignore[call-non-callable]
        if hasattr(scan_result, "get_pass_results_count")
        else 0,
        "total_checks": scan_result.get_all_results_count()  # type: ignore[call-non-callable]
        if hasattr(scan_result, "get_all_results_count")
        else 0,
        "execution_time": scan_result.get_execution_time()  # type: ignore[call-non-callable]
        if hasattr(scan_result, "get_execution_time")
        else 0,
    }

    # Log results
    failed_count = (
        scan_result.get_fail_results_count()  # type: ignore[call-non-callable]
        if hasattr(scan_result, "get_fail_results_count")
        else 0
    )
    if failed_count > 0:
        logger.warning(f"Soda checks failed: {failed_count} failures")
        logger.info(f"Scan logs: {scan.get_logs_text()}")
    else:
        logger.info("All Soda checks passed successfully")

    return results


def validate_staging_data() -> dict[str, Any]:
    """Validate staging tables with Soda Core."""
    logger.info("Validating staging data quality")

    return run_soda_checks(
        data_source_name="gaming_analytics",
        checks_path="src/gaming_pipeline/quality/checks/staging.yml",
        variables={
            "table_prefix": "rawg_",
            "date_column": "released",
            "rating_column": "rating",
        },
    )


def validate_mart_data() -> dict[str, Any]:
    """Validate mart tables with Soda Core."""
    logger.info("Validating mart data quality")

    return run_soda_checks(
        data_source_name="gaming_analytics",
        checks_path="src/gaming_pipeline/quality/checks/marts.yml",
        variables={
            "table_prefix": "mart_",
            "date_column": "release_date",
            "rating_column": "average_rating",
        },
    )


def validate_full_pipeline() -> dict[str, Any]:
    """Run complete data quality validation."""
    logger.info("Running full pipeline data quality validation")

    staging_results = validate_staging_data()
    mart_results = validate_mart_data()

    overall_result = {
        "staging_validation": staging_results,
        "mart_validation": mart_results,
        "overall_status": "PASS"
        if (
            staging_results["failed_checks"] == 0 and mart_results["failed_checks"] == 0
        )
        else "FAIL",
        "execution_time": staging_results["execution_time"]
        + mart_results["execution_time"],
    }

    logger.info(
        f"Full pipeline validation completed: {overall_result['overall_status']}"
    )
    return overall_result


def validate_table_quality(table_name: str) -> dict[str, Any]:
    """
    Validate specific table with Soda Core.

    Args:
        table_name: Name of the table to validate

    Returns:
        Dictionary with validation results
    """
    logger.info(f"Validating table: {table_name}")

    return run_soda_checks(
        data_source_name="gaming_analytics",
        checks_path="src/gaming_pipeline/quality/checks",
        variables={
            "table_name": table_name,
            "date_column": "released" if "rawg_" in table_name else "release_date",
            "rating_column": "rating" if "rawg_" in table_name else "average_rating",
        },
    )


def get_data_quality_summary() -> dict[str, Any]:
    """Get summary of data quality checks."""
    logger.info("Generating data quality summary")

    # Run all validations
    full_results = validate_full_pipeline()

    summary = {
        "staging_quality": {
            "total_checks": full_results["staging_validation"]["total_checks"],
            "passed_checks": full_results["staging_validation"]["passed_checks"],
            "failed_checks": full_results["staging_validation"]["failed_checks"],
            "success_rate": (
                full_results["staging_validation"]["passed_checks"]
                / max(full_results["staging_validation"]["total_checks"], 1)
            )
            * 100,
        },
        "mart_quality": {
            "total_checks": full_results["mart_validation"]["total_checks"],
            "passed_checks": full_results["mart_validation"]["passed_checks"],
            "failed_checks": full_results["mart_validation"]["failed_checks"],
            "success_rate": (
                full_results["mart_validation"]["passed_checks"]
                / max(full_results["mart_validation"]["total_checks"], 1)
            )
            * 100,
        },
        "overall_quality": {
            "status": full_results["overall_status"],
            "total_checks": (
                full_results["staging_validation"]["total_checks"]
                + full_results["mart_validation"]["total_checks"]
            ),
            "total_passed": (
                full_results["staging_validation"]["passed_checks"]
                + full_results["mart_validation"]["passed_checks"]
            ),
            "total_failed": (
                full_results["staging_validation"]["failed_checks"]
                + full_results["mart_validation"]["failed_checks"]
            ),
            "overall_success_rate": (
                (
                    full_results["staging_validation"]["passed_checks"]
                    + full_results["mart_validation"]["passed_checks"]
                )
                / max(
                    full_results["staging_validation"]["total_checks"]
                    + full_results["mart_validation"]["total_checks"],
                    1,
                )
            )
            * 100,
        },
    }

    logger.info(f"Data quality summary generated: {summary}")
    return summary
