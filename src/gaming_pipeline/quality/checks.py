"""Soda Core v4 data quality checks for gaming analytics pipeline."""

import logging
import re
import subprocess
from pathlib import Path
from typing import Any

from soda_core.contracts import verify_contract_locally

from gaming_pipeline.config import config

logger = logging.getLogger(__name__)

CONTRACT_FILES: dict[str, list[str]] = {
    "raw": ["raw_games.yaml", "raw_genres.yaml", "raw_platforms.yaml"],
    "marts": ["fct_games.yaml", "fct_genres.yaml", "fct_platforms.yaml"],
}


class SQLMeshTestResult:
    """SQLMesh test result parser."""

    def __init__(self, stdout: str, stderr: str, returncode: int) -> None:
        """Initialize parser with SQLMesh command output.

        Args:
            stdout: Standard output from sqlmesh test command.
            stderr: Standard error from sqlmesh test command.
            returncode: Exit code from sqlmesh test command.
        """
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.test_results = self._parse_sqlmesh_output(stdout)
        self.success = returncode == 0 and all(
            r["failed"] == 0 for r in self.test_results.values()
        )

    def _parse_sqlmesh_output(self, output: str) -> dict[str, dict[str, Any]]:
        """Parse SQLMesh stdout to extract test results.

        Args:
            output: Raw stdout from sqlmesh test.

        Returns:
            Dictionary mapping test names to their result dicts.
        """
        results: dict[str, dict[str, Any]] = {}
        for line in output.strip().split("\n"):
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
            emoji_match = re.search(
                r"([✅❌])\s*(\S+)\s+(PASSED|FAILED|passed|failed)", line
            )
            if emoji_match:
                test_name = emoji_match.group(2).strip()
                status = emoji_match.group(3).upper()
                results[test_name] = {
                    "name": test_name,
                    "status": status,
                    "passed": emoji_match.group(1) == "✅",
                    "failed": emoji_match.group(1) == "❌",
                }
        return results

    def get_summary(self) -> dict[str, Any]:
        """Get summary of test results.

        Returns:
            Dictionary with total, passed, failed counts and success rate.
        """
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results.values() if r["passed"])
        return {
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": sum(1 for r in self.test_results.values() if r["failed"]),
            "success_rate": (passed / max(total, 1)) * 100,
            "results": self.test_results,
            "raw_output": self.stdout,
            "stderr": self.stderr,
            "returncode": self.returncode,
        }


class SodaScanner:
    """Soda Core v4 scanner using contracts."""

    def __init__(self, data_source_file: str = "data_source.yaml") -> None:
        """Initialize scanner with data source configuration.

        Args:
            data_source_file: Name of the Soda data source YAML file.
        """
        self.ds_file = Path(__file__).parent / data_source_file

    def run_checks(self, contract_path: Path) -> dict[str, Any]:
        """Run Soda contract checks against a contract file.

        Args:
            contract_path: Path to the Soda contract YAML file.

        Returns:
            Dictionary with passed/failed status and check counts.
        """
        if not contract_path.exists():
            return {
                "passed": False,
                "failed": True,
                "error": f"Contract file not found: {contract_path}",
            }
        try:
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
            return {"passed": False, "failed": True, "error": str(e)}


def run_soda_checks(layer: str = "marts") -> dict[str, Any]:
    """Run Soda data quality checks for a layer.

    Args:
        layer: The data layer to check ('raw' or 'marts').

    Returns:
        Dictionary with overall pass/fail and per-file results.
    """
    checks_dir = Path(config.soda.checks_path)
    contract_files = CONTRACT_FILES.get(layer, [])
    if not contract_files:
        return {"passed": False, "failed": True, "error": f"Unknown layer: {layer}"}

    scanner = SodaScanner()
    all_passed = True
    results = []
    for contract_file in contract_files:
        result = scanner.run_checks(checks_dir / contract_file)
        results.append(
            {
                "file": contract_file,
                "passed": result.get("passed", False),
                "failed": result.get("failed", True),
                "error": result.get("error"),
            }
        )
        if not result.get("passed", False):
            all_passed = False
    return {
        "passed": all_passed,
        "failed": not all_passed,
        "layer": layer,
        "results": results,
    }


def run_sqlmesh_tests() -> dict[str, Any]:
    """Run SQLMesh native tests.

    Returns:
        Dictionary with test counts, success rate, and results.
    """
    try:
        result = subprocess.run(  # noqa: S603,S607
            ["sqlmesh", "test"],  # noqa: S603,S607
            capture_output=True,
            text=True,
            timeout=120,
            cwd="sqlmesh",
        )
        test_result = SQLMeshTestResult(
            stdout=result.stdout, stderr=result.stderr, returncode=result.returncode
        )
        summary = test_result.get_summary()
        rate = summary["success_rate"]
        logger.info(
            f"SQLMesh tests: {summary['passed_tests']}/{summary['total_tests']} "
            f"passed ({rate:.1f}%)"
        )
        return summary
    except subprocess.TimeoutExpired:
        return {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "success_rate": 0.0,
            "error": "Timed out",
        }
    except Exception as e:
        return {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "success_rate": 0.0,
            "error": str(e),
        }


def run_quality_checks(layer: str = "marts") -> dict[str, Any]:
    """Run unified data quality validation (SQLMesh + Soda).

    Args:
        layer: The data layer to check ('raw' or 'marts').

    Returns:
        Dictionary with SQLMesh results, Soda results, and overall status.
    """
    sqlmesh_result = run_sqlmesh_tests()
    soda_result = run_soda_checks(layer)
    sqlmesh_passed = sqlmesh_result.get("passed_tests", 0)
    sqlmesh_total = sqlmesh_result.get("total_tests", 0)
    sqlmesh_status = "PASS" if sqlmesh_passed == sqlmesh_total else "FAIL"
    soda_status = "PASS" if soda_result.get("passed") else "FAIL"
    overall = "PASS" if sqlmesh_status == "PASS" and soda_status == "PASS" else "FAIL"
    logger.info(
        f"Quality checks: SQLMesh={sqlmesh_status}, Soda={soda_status}, "
        f"Overall={overall}"
    )
    return {
        "sqlmesh": sqlmesh_result,
        "soda": soda_result,
        "sqlmesh_status": sqlmesh_status,
        "soda_status": soda_status,
        "overall_status": overall,
    }
