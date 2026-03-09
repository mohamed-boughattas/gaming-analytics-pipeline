"""Soda Core v4 data quality checks for gaming analytics pipeline."""

import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Any

from soda_core.contracts import verify_contract_locally

from gaming_pipeline.config import settings

logger = logging.getLogger(__name__)


class SQLMeshTestResult:
    """SQLMesh test result parser."""

    def __init__(self, stdout: str, stderr: str, returncode: int):
        """Initialize SQLMesh test result.

        Args:
            stdout: Standard output from sqlmesh test
            stderr: Standard error from sqlmesh test
            returncode: Return code from sqlmesh test
        """
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.test_results = self._parse_sqlmesh_output(stdout)
        self.success = returncode == 0 and all(
            r["failed"] == 0 for r in self.test_results.values()
        )

    def _parse_sqlmesh_output(self, output: str) -> dict[str, dict[str, Any]]:
        """Parse SQLMesh test output.

        Args:
            output: SQLMesh test stdout

        Returns:
            Dictionary of test results by test name
        """
        results = {}

        # Parse SQLMesh test output format
        # Example format:
        # ✅ test_no_null_game_names PASSED
        # ❌ test_rating_ranges FAILED
        lines = output.strip().split("\n")

        for line in lines:
            # Match patterns like:
            # ✅ test_name PASSED
            # ❌ test_name FAILED
            # test_name: PASSED/FAILED
            match = re.search(
                r"[:\s*]?([^:\s]+)\s*:\s*(PASSED|FAILED|passed|failed)", line
            )
            if match:
                test_name = match.group(1).strip()
                status = match.group(2).upper()
                results[test_name] = {
                    "name": test_name,
                    "status": status,
                    "passed": status == "PASSED",
                    "failed": status == "FAILED",
                }

            # Also match emoji-based format
            emoji_match = re.search(
                r"([✅❌])\s*(\S+)\s+(PASSED|FAILED|passed|failed)", line
            )
            if emoji_match:
                emoji = emoji_match.group(1)
                test_name = emoji_match.group(2).strip()
                status = emoji_match.group(3).upper()
                results[test_name] = {
                    "name": test_name,
                    "status": status,
                    "passed": emoji == "✅",
                    "failed": emoji == "❌",
                }

        return results

    def get_summary(self) -> dict[str, Any]:
        """Get summary of SQLMesh test results.

        Returns:
            Dictionary with test summary
        """
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results.values() if r["passed"])
        failed = sum(1 for r in self.test_results.values() if r["failed"])

        return {
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": failed,
            "success_rate": (passed / max(total, 1)) * 100,
            "results": self.test_results,
            "raw_output": self.stdout,
            "stderr": self.stderr,
            "returncode": self.returncode,
        }


class SodaScanner:
    """Soda Core v4 scanner using contracts."""

    # Mapping of layer names to contract files
    # Raw layer: data ingested from external sources (RAWG API)
    # Marts layer: transformed and enriched data for analytics
    CONTRACT_FILES = {
        "raw": [
            "rawg_games.yml",
            "rawg_genres.yml",
            "rawg_platforms.yml",
        ],
        "marts": [
            "games.yml",
            "genres.yml",
            "platforms.yml",
        ],
    }

    def __init__(self, data_source_file: str = "ds.yml"):
        """Initialize the Soda scanner.

        Args:
            data_source_file: Name of the data source config file
        """
        self.ds_file = Path(__file__).parent / data_source_file
        logger.info(f"Initialized Soda scanner with data source: {self.ds_file}")

    def run_checks(self, contract_path: Path) -> dict[str, Any]:
        """Run Soda v4 contract checks and return results.

        Args:
            contract_path: Path to the contract YAML file

        Returns:
            Dictionary with scan results
        """
        logger.info(f"Running Soda checks from: {contract_path}")

        if not contract_path.exists():
            logger.error(f"Contract file not found: {contract_path}")
            return {
                "passed": False,
                "failed": True,
                "error": f"Contract file not found: {contract_path}",
            }

        try:
            # Set environment variable for DUCKDB_PATH if needed
            env = os.environ.copy()
            if "DUCKDB_PATH" not in env:
                env["DUCKDB_PATH"] = str(settings.database.path)

            # Use verify_contract_locally (singular) - the recommended API
            result = verify_contract_locally(
                data_source_file_path=str(self.ds_file),
                contract_file_path=str(contract_path),
            )

            return {
                "passed": result.is_passed,
                "failed": result.is_failed,
                "checks_passed": result.number_of_checks_passed,
                "checks_failed": result.number_of_checks_failed,
                "has_errors": result.has_errors,
                "errors": result.get_errors(),
            }

        except Exception as e:
            logger.error(f"Error running Soda checks: {e}")
            return {
                "passed": False,
                "failed": True,
                "error": str(e),
            }

    def run_checks_for_layer(self, layer: str) -> dict[str, Any]:
        """Run Soda checks for a specific layer (raw/marts).

        Args:
            layer: Layer name (raw or marts)

        Returns:
            Dictionary with scan results
        """
        checks_dir = Path(__file__).parent / "checks"

        # Get the list of contract files for this layer
        contract_files = self.CONTRACT_FILES.get(layer, [])

        if not contract_files:
            logger.warning(f"Unknown layer: {layer}")
            return {"passed": False, "failed": True, "error": f"Unknown layer: {layer}"}

        # Run checks for each contract file and aggregate results
        all_passed = True
        all_failed = False
        results = []

        for contract_file in contract_files:
            contract_path = checks_dir / contract_file
            result = self.run_checks(contract_path)
            results.append(
                {
                    "file": contract_file,
                    "passed": result.get("passed", False),
                    "failed": result.get("failed", True),
                    "error": result.get("error"),
                }
            )

            # Aggregate results
            if not result.get("passed", False):
                all_passed = False
            if result.get("failed", True):
                all_failed = True

        return {
            "passed": all_passed,
            "failed": all_failed,
            "layer": layer,
            "results": results,
        }


class UnifiedDataQualityChecker:
    """Unified data quality checker combining SQLMesh tests and Soda scans."""

    def __init__(self, db_path: str | None = None):
        """Initialize the unified data quality checker.

        Args:
            db_path: Path to DuckDB database (unused, kept for API compatibility)
        """
        self.db_path = db_path or settings.database.path
        self.soda_scanner = SodaScanner()
        self.sqlmesh_dir = Path("sqlmesh")
        logger.info("Initialized unified data quality checker")

    def run_sqlmesh_tests(self, sqlmesh_dir: Path | None = None) -> SQLMeshTestResult:
        """Run SQLMesh native tests.

        Args:
            sqlmesh_dir: Path to SQLMesh directory

        Returns:
            SQLMeshTestResult with test results
        """
        work_dir = sqlmesh_dir or self.sqlmesh_dir

        if not work_dir.exists():
            logger.warning(f"SQLMesh directory not found: {work_dir}")
            return SQLMeshTestResult(
                stdout="",
                stderr=f"SQLMesh directory not found: {work_dir}",
                returncode=1,
            )

        logger.info(f"Running SQLMesh tests in: {work_dir}")

        try:
            # sqlmesh is a known safe command from project dependencies
            result = subprocess.run(
                ["sqlmesh", "test"],  # noqa: S607
                capture_output=True,
                text=True,
                cwd=work_dir,
                timeout=120,
            )

            test_result = SQLMeshTestResult(
                stdout=result.stdout, stderr=result.stderr, returncode=result.returncode
            )

            summary = test_result.get_summary()
            success_rate = summary["success_rate"]
            logger.info(
                f"SQLMesh tests: {summary['passed_tests']}/{summary['total_tests']} "
                f"passed ({success_rate:.1f}%)"
            )

            return test_result

        except subprocess.TimeoutExpired:
            logger.error("SQLMesh tests timed out")
            return SQLMeshTestResult(
                stdout="",
                stderr="SQLMesh tests timed out",
                returncode=1,
            )
        except Exception as e:
            logger.error(f"Error running SQLMesh tests: {e}")
            return SQLMeshTestResult(stdout="", stderr=str(e), returncode=1)

    def run_soda_checks(self, layer: str = "marts") -> dict[str, Any]:
        """Run Soda data quality checks.

        Args:
            layer: Layer to check (raw or marts)

        Returns:
            Dictionary with Soda scan results
        """
        logger.info(f"Running Soda checks for layer: {layer}")
        return self.soda_scanner.run_checks_for_layer(layer)

    def run_unified_validation(
        self,
        layer: str = "marts",
        run_sqlmesh: bool = True,
    ) -> dict[str, Any]:
        """Run unified data quality validation (SQLMesh + Soda).

        Args:
            layer: Layer to validate (raw or marts)
            run_sqlmesh: Whether to run SQLMesh tests

        Returns:
            Dictionary with combined validation results
        """
        logger.info("Running unified data quality validation")

        results: dict[str, Any] = {
            "sqlmesh_tests": None,
            "soda_validation": None,
            "sqlmesh_status": "SKIPPED",
            "soda_status": "PASS",
            "overall_status": "PASS",
        }

        # Run SQLMesh tests
        if run_sqlmesh:
            sqlmesh_result = self.run_sqlmesh_tests()
            results["sqlmesh_tests"] = sqlmesh_result.get_summary()
            results["overall_status"] = "PASS" if sqlmesh_result.success else "FAIL"

        # Run Soda checks
        soda_result = self.run_soda_checks(layer)
        results["soda_validation"] = soda_result

        # Combine results
        if results["sqlmesh_tests"]:
            sqlmesh_passed = results["sqlmesh_tests"]["passed_tests"]
            sqlmesh_total = results["sqlmesh_tests"]["total_tests"]
            results["sqlmesh_status"] = (
                "PASS" if sqlmesh_passed == sqlmesh_total else "FAIL"
            )
        else:
            results["sqlmesh_status"] = "SKIPPED"

        results["soda_status"] = "PASS" if soda_result.get("passed") else "FAIL"

        # Determine overall status
        if results["sqlmesh_status"] != "SKIPPED":
            results["overall_status"] = (
                "PASS"
                if results["sqlmesh_status"] == "PASS"
                and results["soda_status"] == "PASS"
                else "FAIL"
            )
        else:
            results["overall_status"] = results["soda_status"]

        logger.info(
            f"Unified validation completed: "
            f"SQLMesh={results['sqlmesh_status']}, "
            f"Soda={results['soda_status']}, "
            f"Overall={results['overall_status']}"
        )

        return results


# Convenience functions
def run_sqlmesh_tests(sqlmesh_dir: Path | None = None) -> dict[str, Any]:
    """Run SQLMesh native tests.

    Args:
        sqlmesh_dir: Path to SQLMesh directory

    Returns:
        Dictionary with SQLMesh test results
    """
    checker = UnifiedDataQualityChecker()
    result = checker.run_sqlmesh_tests(sqlmesh_dir)
    return result.get_summary()


def run_soda_checks(layer: str = "marts") -> dict[str, Any]:
    """Run Soda data quality checks.

    Args:
        layer: Layer to check (raw or marts)

    Returns:
        Dictionary with Soda scan results
    """
    scanner = SodaScanner()
    return scanner.run_checks_for_layer(layer)


def run_unified_validation(
    layer: str = "marts",
    run_sqlmesh: bool = True,
) -> dict[str, Any]:
    """Run unified data quality validation (SQLMesh + Soda).

    Args:
        layer: Layer to validate (raw or marts)
        run_sqlmesh: Whether to run SQLMesh tests

    Returns:
        Dictionary with combined validation results
    """
    checker = UnifiedDataQualityChecker()
    return checker.run_unified_validation(layer, run_sqlmesh)


def validate_raw_data() -> dict[str, Any]:
    """Validate raw data with unified approach."""
    logger.info("Validating raw data quality")
    return run_unified_validation(layer="raw", run_sqlmesh=True)


# Keep backward compatibility alias
def validate_staging_data() -> dict[str, Any]:
    """Validate staging data with unified approach.

    Deprecated: Use validate_raw_data() instead.
    """
    logger.warning(
        "validate_staging_data() is deprecated, use validate_raw_data() instead"
    )
    return validate_raw_data()


def validate_mart_data() -> dict[str, Any]:
    """Validate mart data with unified approach."""
    logger.info("Validating mart data quality")
    return run_unified_validation(layer="marts", run_sqlmesh=True)


def validate_full_pipeline() -> dict[str, Any]:
    """Run complete data quality validation."""
    logger.info("Running full pipeline data quality validation")

    # Run unified validation on raw layer
    full_results = validate_raw_data()

    overall_result = {
        "raw_validation": full_results,
        "overall_status": full_results.get("overall_status", "UNKNOWN"),
        "execution_time": 0,
    }

    logger.info(
        f"Full pipeline validation completed: {overall_result['overall_status']}"
    )
    return overall_result


def validate_table_quality(table_name: str) -> dict[str, Any]:
    """Validate specific table with unified approach.

    Args:
        table_name: Name of the table to validate

    Returns:
        Dictionary with validation results
    """
    logger.info(f"Validating table: {table_name}")
    # Determine layer based on table name
    layer = "raw" if "rawg_" in table_name else "marts"
    return run_unified_validation(layer=layer, run_sqlmesh=True)


def get_data_quality_summary() -> dict[str, Any]:
    """Get summary of data quality checks (SQLMesh + Soda)."""
    logger.info("Generating data quality summary")

    # Run unified validation
    full_results = validate_full_pipeline()
    raw = full_results.get("raw_validation", {})

    # Extract SQLMesh results
    sqlmesh_results = raw.get("sqlmesh_tests", {})
    soda_results = raw.get("soda_validation", {})

    summary = {
        "sqlmesh_quality": {
            "total_tests": sqlmesh_results.get("total_tests", 0),
            "passed_tests": sqlmesh_results.get("passed_tests", 0),
            "failed_tests": sqlmesh_results.get("failed_tests", 0),
            "success_rate": sqlmesh_results.get("success_rate", 100.0),
            "results": sqlmesh_results.get("results", {}),
        },
        "soda_quality": {
            "passed": soda_results.get("passed", False),
            "failed": soda_results.get("failed", True),
        },
        "overall_quality": {
            "status": full_results.get("overall_status", "UNKNOWN"),
            "sqlmesh_status": raw.get("sqlmesh_status", "SKIPPED"),
            "soda_status": raw.get("soda_status", "SKIPPED"),
        },
    }

    logger.info(f"Data quality summary generated: {summary}")
    return summary
