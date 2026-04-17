"""Tests for quality checks module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from gaming_pipeline.quality.checks import (
    CONTRACT_FILES,
    SodaScanner,
    SQLMeshTestResult,
    run_quality_checks,
    run_soda_checks,
    run_sqlmesh_tests,
)


class TestSQLMeshTestResult:
    """Test SQLMeshTestResult parser."""

    def test_parse_emoji_passed(self) -> None:
        output = "✅ test_no_null_game_names PASSED"
        result = SQLMeshTestResult(output, "", 0)
        assert result.success is True
        assert "test_no_null_game_names" in result.test_results
        assert result.test_results["test_no_null_game_names"]["passed"] is True
        assert result.test_results["test_no_null_game_names"]["failed"] is False

    def test_parse_emoji_failed(self) -> None:
        output = "❌ test_rating_ranges FAILED"
        result = SQLMeshTestResult(output, "", 1)
        assert result.success is False
        assert result.test_results["test_rating_ranges"]["failed"] is True
        assert result.test_results["test_rating_ranges"]["passed"] is False

    def test_parse_colon_format(self) -> None:
        output = "test_no_null_names: PASSED\ntest_valid_ratings: FAILED"
        result = SQLMeshTestResult(output, "", 1)
        assert "test_no_null_names" in result.test_results
        assert "test_valid_ratings" in result.test_results

    def test_get_summary_with_results(self) -> None:
        output = "✅ test_a PASSED\n✅ test_b PASSED\n❌ test_c FAILED"
        result = SQLMeshTestResult(output, "", 1)
        summary = result.get_summary()
        assert summary["total_tests"] == 3
        assert summary["passed_tests"] == 2
        assert summary["failed_tests"] == 1
        assert summary["success_rate"] == pytest.approx(66.67, rel=0.1)

    def test_get_summary_empty(self) -> None:
        result = SQLMeshTestResult("", "", 0)
        summary = result.get_summary()
        assert summary["total_tests"] == 0
        assert summary["passed_tests"] == 0
        assert summary["failed_tests"] == 0
        assert summary["success_rate"] == 0

    def test_success_false_on_non_zero_returncode(self) -> None:
        output = "✅ test_a PASSED"
        result = SQLMeshTestResult(output, "", 1)
        assert result.success is False

    def test_parse_mixed_formats(self) -> None:
        output = "✅ test_one PASSED\ntest_two: FAILED\n❌ test_three FAILED"
        result = SQLMeshTestResult(output, "", 1)
        assert len(result.test_results) >= 2

    def test_summary_contains_raw_output(self) -> None:
        result = SQLMeshTestResult("test output", "test stderr", 0)
        summary = result.get_summary()
        assert summary["raw_output"] == "test output"
        assert summary["stderr"] == "test stderr"
        assert summary["returncode"] == 0


class TestSodaScanner:
    """Test SodaScanner class."""

    def test_contract_files_mapping(self) -> None:
        assert "raw" in CONTRACT_FILES
        assert "marts" in CONTRACT_FILES
        assert len(CONTRACT_FILES["raw"]) == 3
        assert len(CONTRACT_FILES["marts"]) == 3

    def test_run_checks_with_missing_file(self) -> None:
        scanner = SodaScanner()
        result = scanner.run_checks(Path("/nonexistent/contract.yaml"))
        assert result["passed"] is False
        assert result["failed"] is True
        assert "not found" in result["error"].lower()

    def test_run_checks_handles_verify_contract_locally_exception(
        self,
    ) -> None:
        from gaming_pipeline.quality.checks import SodaScanner

        scanner = SodaScanner()
        contract_path = (
            Path(__file__).parent.parent
            / "src/gaming_pipeline/quality/checks/raw_games.yaml"
        )

        with patch(
            "gaming_pipeline.quality.checks.verify_contract_locally"
        ) as mock_verify:
            mock_verify.side_effect = RuntimeError("Soda core error")

            result = scanner.run_checks(contract_path)

            assert result["passed"] is False
            assert result["failed"] is True
            assert "Soda core error" in result["error"]

    def test_run_checks_success_path(
        self,
    ) -> None:
        from gaming_pipeline.quality.checks import SodaScanner

        scanner = SodaScanner()
        contract_path = (
            Path(__file__).parent.parent
            / "src/gaming_pipeline/quality/checks/raw_games.yaml"
        )

        mock_result = MagicMock()
        mock_result.is_passed = True
        mock_result.is_failed = False
        mock_result.number_of_checks_passed = 5
        mock_result.number_of_checks_failed = 0
        mock_result.has_errors = False
        mock_result.get_errors.return_value = []

        with patch(
            "gaming_pipeline.quality.checks.verify_contract_locally",
            return_value=mock_result,
        ):
            result = scanner.run_checks(contract_path)

            assert result["passed"] is True
            assert result["failed"] is False
            assert result["checks_passed"] == 5
            assert result["checks_failed"] == 0


class TestRunSodaChecks:
    """Test run_soda_checks function."""

    @patch("gaming_pipeline.quality.checks.SodaScanner")
    def test_run_soda_checks_raw_layer(self, mock_scanner_cls: MagicMock) -> None:
        mock_scanner = MagicMock()
        mock_scanner.run_checks.return_value = {"passed": True, "failed": False}
        mock_scanner_cls.return_value = mock_scanner

        result = run_soda_checks(layer="raw")

        assert isinstance(result, dict)
        assert "passed" in result
        assert "failed" in result
        assert "layer" in result
        assert result["layer"] == "raw"
        assert result["passed"] is True

    @patch("gaming_pipeline.quality.checks.SodaScanner")
    def test_run_soda_checks_marts_layer(self, mock_scanner_cls: MagicMock) -> None:
        mock_scanner = MagicMock()
        mock_scanner.run_checks.return_value = {"passed": True, "failed": False}
        mock_scanner_cls.return_value = mock_scanner

        result = run_soda_checks(layer="marts")

        assert result["layer"] == "marts"

    @patch("gaming_pipeline.quality.checks.SodaScanner")
    def test_run_soda_checks_unknown_layer(self, mock_scanner_cls: MagicMock) -> None:
        result = run_soda_checks(layer="unknown")

        assert result["passed"] is False
        assert result["failed"] is True
        assert "Unknown layer" in result["error"]

    @patch("gaming_pipeline.quality.checks.SodaScanner")
    def test_run_soda_checks_all_passed(self, mock_scanner_cls: MagicMock) -> None:
        mock_scanner = MagicMock()
        mock_scanner.run_checks.return_value = {"passed": True, "failed": False}
        mock_scanner_cls.return_value = mock_scanner

        result = run_soda_checks(layer="raw")

        assert result["passed"] is True

    @patch("gaming_pipeline.quality.checks.SodaScanner")
    def test_run_soda_checks_one_fails(self, mock_scanner_cls: MagicMock) -> None:
        mock_scanner = MagicMock()
        mock_scanner.run_checks.side_effect = [
            {"passed": True, "failed": False},
            {"passed": True, "failed": False},
            {"passed": False, "failed": True},
        ]
        mock_scanner_cls.return_value = mock_scanner

        result = run_soda_checks(layer="raw")

        assert result["passed"] is False


class TestRunSQLMeshTests:
    """Test run_sqlmesh_tests function."""

    @patch("gaming_pipeline.quality.checks.subprocess.run")
    def test_run_sqlmesh_tests_success(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="✅ test_one PASSED\n✅ test_two PASSED",
            stderr="",
        )

        result = run_sqlmesh_tests()

        assert isinstance(result, dict)
        assert result["total_tests"] == 2
        assert result["passed_tests"] == 2
        assert result["failed_tests"] == 0
        assert result["success_rate"] == 100.0

    @patch("gaming_pipeline.quality.checks.subprocess.run")
    def test_run_sqlmesh_tests_partial_failure(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="✅ test_one PASSED\n❌ test_two FAILED",
            stderr="",
        )

        result = run_sqlmesh_tests()

        assert result["total_tests"] == 2
        assert result["passed_tests"] == 1
        assert result["failed_tests"] == 1

    @patch("gaming_pipeline.quality.checks.subprocess.run")
    def test_run_sqlmesh_tests_timeout(self, mock_run: MagicMock) -> None:
        from subprocess import TimeoutExpired

        mock_run.side_effect = TimeoutExpired("sqlmesh", 120)

        result = run_sqlmesh_tests()

        assert result["total_tests"] == 0
        assert result["error"] == "Timed out"

    @patch("gaming_pipeline.quality.checks.subprocess.run")
    def test_run_sqlmesh_tests_exception(self, mock_run: MagicMock) -> None:
        mock_run.side_effect = Exception("sqlmesh not found")

        result = run_sqlmesh_tests()

        assert result["total_tests"] == 0
        assert "sqlmesh not found" in result["error"]


class TestRunQualityChecks:
    """Test run_quality_checks function."""

    @patch("gaming_pipeline.quality.checks.run_soda_checks")
    @patch("gaming_pipeline.quality.checks.run_sqlmesh_tests")
    def test_run_quality_checks_all_pass(
        self, mock_sqlmesh: MagicMock, mock_soda: MagicMock
    ) -> None:
        mock_sqlmesh.return_value = {
            "total_tests": 5,
            "passed_tests": 5,
            "failed_tests": 0,
            "success_rate": 100.0,
        }
        mock_soda.return_value = {"passed": True, "failed": False}

        result = run_quality_checks(layer="marts")

        assert result["sqlmesh_status"] == "PASS"
        assert result["soda_status"] == "PASS"
        assert result["overall_status"] == "PASS"

    @patch("gaming_pipeline.quality.checks.run_soda_checks")
    @patch("gaming_pipeline.quality.checks.run_sqlmesh_tests")
    def test_run_quality_checks_sqlmesh_fails(
        self, mock_sqlmesh: MagicMock, mock_soda: MagicMock
    ) -> None:
        mock_sqlmesh.return_value = {
            "total_tests": 5,
            "passed_tests": 3,
            "failed_tests": 2,
            "success_rate": 60.0,
        }
        mock_soda.return_value = {"passed": True, "failed": False}

        result = run_quality_checks(layer="marts")

        assert result["sqlmesh_status"] == "FAIL"
        assert result["overall_status"] == "FAIL"

    @patch("gaming_pipeline.quality.checks.run_soda_checks")
    @patch("gaming_pipeline.quality.checks.run_sqlmesh_tests")
    def test_run_quality_checks_soda_fails(
        self, mock_sqlmesh: MagicMock, mock_soda: MagicMock
    ) -> None:
        mock_sqlmesh.return_value = {
            "total_tests": 5,
            "passed_tests": 5,
            "failed_tests": 0,
            "success_rate": 100.0,
        }
        mock_soda.return_value = {"passed": False, "failed": True}

        result = run_quality_checks(layer="marts")

        assert result["soda_status"] == "FAIL"
        assert result["overall_status"] == "FAIL"

    @patch("gaming_pipeline.quality.checks.run_soda_checks")
    @patch("gaming_pipeline.quality.checks.run_sqlmesh_tests")
    def test_run_quality_checks_returns_full_results(
        self, mock_sqlmesh: MagicMock, mock_soda: MagicMock
    ) -> None:
        mock_sqlmesh.return_value = {
            "total_tests": 5,
            "passed_tests": 5,
            "failed_tests": 0,
            "success_rate": 100.0,
        }
        mock_soda.return_value = {"passed": True, "failed": False}

        result = run_quality_checks(layer="raw")

        assert "sqlmesh" in result
        assert "soda" in result
        assert "sqlmesh_status" in result
        assert "soda_status" in result
        assert "overall_status" in result


class TestMainBlock:
    """Test the if __name__ == '__main__' block of checks.py."""

    def test_main_block_runs_quality_checks(self) -> None:
        import subprocess
        import sys

        result = subprocess.run(  # noqa: S603
            [
                sys.executable,
                "-m",
                "coverage",
                "run",
                "-m",
                "gaming_pipeline.quality.checks",
            ],
            capture_output=True,
            text=True,
            cwd=".",
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
