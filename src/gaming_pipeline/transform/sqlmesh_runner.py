"""SQLMesh runner for gaming analytics pipeline."""

import logging
import subprocess
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Default timeout for SQLMesh commands (in seconds)
DEFAULT_TIMEOUT = 300


class SQLMeshRunner:
    """Runner for SQLMesh transformations."""

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        """Initialize SQLMesh runner.

        Args:
            timeout: Maximum time in seconds for command execution.
        """
        self.models_path = Path("models")
        self.sqlmesh_config = Path("sqlmesh.yaml")
        self.timeout = timeout

    def plan(self, **kwargs: Any) -> dict[str, Any]:
        """Run sqlmesh plan command to preview changes.

        Returns:
            dict with stdout, stderr, and returncode
        """
        cmd = ["sqlmesh", "plan"]
        logger.info(f"Running command: {' '.join(cmd)}")
        try:
            result = subprocess.run(  # noqa: S603
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            logger.info(f"SQLMesh plan completed with return code: {result.returncode}")
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            logger.error(f"SQLMesh plan timed out after {self.timeout} seconds")
            return {
                "stdout": "",
                "stderr": f"Command timed out after {self.timeout} seconds",
                "returncode": -1,
            }

    def apply(self, **kwargs: Any) -> dict[str, Any]:
        """Run sqlmesh plan --apply command to execute transformations.

        Returns:
            dict with stdout, stderr, and returncode
        """
        cmd = ["sqlmesh", "plan", "--apply"]
        logger.info(f"Running command: {' '.join(cmd)}")
        try:
            result = subprocess.run(  # noqa: S603
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            logger.info(
                f"SQLMesh apply completed with return code: {result.returncode}"
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            logger.error(f"SQLMesh apply timed out after {self.timeout} seconds")
            return {
                "stdout": "",
                "stderr": f"Command timed out after {self.timeout} seconds",
                "returncode": -1,
            }

    def test(self) -> dict[str, Any]:
        """Run sqlmesh test command to run model tests.

        Returns:
            dict with stdout, stderr, and returncode
        """
        cmd = ["sqlmesh", "test"]
        logger.info(f"Running command: {' '.join(cmd)}")
        try:
            result = subprocess.run(  # noqa: S603
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            logger.info(f"SQLMesh test completed with return code: {result.returncode}")
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            logger.error(f"SQLMesh test timed out after {self.timeout} seconds")
            return {
                "stdout": "",
                "stderr": f"Command timed out after {self.timeout} seconds",
                "returncode": -1,
            }
