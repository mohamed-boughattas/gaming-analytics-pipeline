"""Tests for quality checks module - focused on parser logic."""

import pytest

from gaming_pipeline.quality.checks import (
    SodaScanner,
    SQLMeshTestResult,
    UnifiedDataQualityChecker,
)


class TestSQLMeshTestResult:
    """Test SQLMeshTestResult class."""

    def test_parse_emoji_passed(self):
        """Test parsing emoji-based PASSED output."""
        output = "✅ test_no_null_game_names PASSED"
        result = SQLMeshTestResult(output, "", 0)

        assert result.success is True
        assert "test_no_null_game_names" in result.test_results
        assert result.test_results["test_no_null_game_names"]["passed"] is True
        assert result.test_results["test_no_null_game_names"]["failed"] is False

    def test_parse_emoji_failed(self):
        """Test parsing emoji-based FAILED output."""
        output = "❌ test_rating_ranges FAILED"
        result = SQLMeshTestResult(output, "", 1)

        assert result.success is False
        assert "test_rating_ranges" in result.test_results
        assert result.test_results["test_rating_ranges"]["failed"] is True
        assert result.test_results["test_rating_ranges"]["passed"] is False

    def test_parse_colon_format(self):
        """Test parsing colon-separated format."""
        output = "test_no_null_names: PASSED\ntest_valid_ratings: FAILED"
        result = SQLMeshTestResult(output, "", 1)

        assert "test_no_null_names" in result.test_results
        assert "test_valid_ratings" in result.test_results

    def test_get_summary_with_results(self):
        """Test summary calculation with results."""
        output = "✅ test_a PASSED\n✅ test_b PASSED\n❌ test_c FAILED"
        result = SQLMeshTestResult(output, "", 1)

        summary = result.get_summary()
        assert summary["total_tests"] == 3
        assert summary["passed_tests"] == 2
        assert summary["failed_tests"] == 1
        assert summary["success_rate"] == pytest.approx(66.67, rel=0.1)

    def test_get_summary_empty(self):
        """Test summary with no results."""
        result = SQLMeshTestResult("", "", 0)

        summary = result.get_summary()
        assert summary["total_tests"] == 0
        assert summary["passed_tests"] == 0
        assert summary["failed_tests"] == 0
        assert summary["success_rate"] == 0

    def test_success_false_on_non_zero_returncode(self):
        """Test success is False when returncode is non-zero."""
        output = "✅ test_a PASSED"
        result = SQLMeshTestResult(output, "", 1)

        assert result.success is False


class TestSodaScanner:
    """Test SodaScanner class."""

    def test_contract_files_mapping(self):
        """Test contract file mappings are defined."""
        scanner = SodaScanner()

        assert "raw" in scanner.CONTRACT_FILES
        assert "marts" in scanner.CONTRACT_FILES
        assert len(scanner.CONTRACT_FILES["raw"]) == 3
        assert len(scanner.CONTRACT_FILES["marts"]) == 3

    def test_run_checks_with_missing_file(self):
        """Test error handling for missing contract file."""
        from pathlib import Path

        scanner = SodaScanner()
        result = scanner.run_checks(Path("/nonexistent/contract.yml"))

        assert result["passed"] is False
        assert result["failed"] is True
        assert "not found" in result["error"].lower()


class TestUnifiedDataQualityChecker:
    """Test UnifiedDataQualityChecker class."""

    def test_initialization(self):
        """Test checker initialization."""
        checker = UnifiedDataQualityChecker()

        assert checker.db_path is not None
        assert isinstance(checker.soda_scanner, SodaScanner)
