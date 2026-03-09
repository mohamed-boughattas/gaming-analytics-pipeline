"""Data quality module for gaming analytics pipeline."""

from .checks import (
    SodaScanner,
    SQLMeshTestResult,
    UnifiedDataQualityChecker,
    get_data_quality_summary,
    run_soda_checks,
    run_sqlmesh_tests,
    run_unified_validation,
    validate_full_pipeline,
    validate_mart_data,
    validate_raw_data,
    validate_staging_data,  # Deprecated, kept for backward compatibility
    validate_table_quality,
)

__all__ = [
    "SQLMeshTestResult",
    "SodaScanner",
    "UnifiedDataQualityChecker",
    "run_sqlmesh_tests",
    "run_soda_checks",
    "run_unified_validation",
    "validate_full_pipeline",
    "validate_raw_data",
    "validate_staging_data",  # Deprecated
    "validate_mart_data",
    "validate_table_quality",
    "get_data_quality_summary",
]
