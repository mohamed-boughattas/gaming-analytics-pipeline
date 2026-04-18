"""Entry point for running quality checks via `python -m gaming_pipeline.quality`."""

from gaming_pipeline.quality.checks import run_quality_checks

if __name__ == "__main__":
    result = run_quality_checks()
    print(f"Overall: {result['overall_status']}")
    sm = result["sqlmesh"]
    print(
        f"SQLMesh: {result['sqlmesh_status']} "
        f"({sm.get('passed_tests', 0)}/{sm.get('total_tests', 0)} tests)"
    )
    print(f"Soda: {result['soda_status']}")
