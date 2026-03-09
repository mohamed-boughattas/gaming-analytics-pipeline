"""SQLMesh runner for gaming analytics pipeline."""

import logging
import subprocess
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SQLMeshRunner:
    """Runner for SQLMesh transformations."""

    def __init__(self):
        self.models_path = Path("models")
        self.sqlmesh_config = Path("sqlmesh.yaml")

    def plan(self, **kwargs: Any) -> dict[str, Any]:
        """Run sqlmesh plan command to preview changes.

        Returns:
            dict with stdout, stderr, and returncode
        """
        cmd = ["sqlmesh", "plan"]
        logger.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")  # noqa: S603
        logger.info(f"SQLMesh plan completed with return code: {result.returncode}")
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }

    def apply(self, **kwargs: Any) -> dict[str, Any]:
        """Run sqlmesh plan --apply command to execute transformations.

        Returns:
            dict with stdout, stderr, and returncode
        """
        cmd = ["sqlmesh", "plan", "--apply"]
        logger.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")  # noqa: S603
        logger.info(f"SQLMesh apply completed with return code: {result.returncode}")
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }

    def test(self) -> dict[str, Any]:
        """Run sqlmesh test command to run model tests.

        Returns:
            dict with stdout, stderr, and returncode
        """
        cmd = ["sqlmesh", "test"]
        logger.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")  # noqa: S603
        logger.info(f"SQLMesh test completed with return code: {result.returncode}")
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
