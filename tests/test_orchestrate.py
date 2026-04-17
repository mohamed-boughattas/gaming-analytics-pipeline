"""Tests for Prefect orchestration module."""

from unittest.mock import MagicMock, patch

import pytest

from gaming_pipeline.orchestrate.flows import pipeline_flow
from gaming_pipeline.orchestrate.tasks import (
    exponential_backoff_with_jitter,
    get_load_info_task,
    get_pipeline_schema_task,
    refresh_schema_task,
    run_full_pipeline_task,
    run_sqlmesh_task,
)


class TestExponentialBackoffWithJitter:
    """Test exponential_backoff_with_jitter function."""

    def test_returns_list(self) -> None:
        result = exponential_backoff_with_jitter(0)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_base_delay_for_attempt_zero(self) -> None:
        result = exponential_backoff_with_jitter(0)
        delay = result[0]
        assert 30 <= delay <= 40

    def test_exponential_growth(self) -> None:
        result_0 = exponential_backoff_with_jitter(0)[0]
        result_1 = exponential_backoff_with_jitter(1)[0]
        result_2 = exponential_backoff_with_jitter(2)[0]
        assert result_1 > result_0
        assert result_2 > result_1

    def test_max_delay_cap(self) -> None:
        result = exponential_backoff_with_jitter(10)
        assert result[0] <= 310


class TestRunFullPipelineTask:
    """Test run_full_pipeline_task Prefect task."""

    @patch("gaming_pipeline.orchestrate.tasks.GamingPipeline")
    @patch("gaming_pipeline.orchestrate.tasks.create_markdown_artifact")
    def test_runs_pipeline_with_params(
        self, mock_artifact: MagicMock, mock_pipeline_cls: MagicMock
    ) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline.run_full_load.return_value = {
            "rawg": {"total_games": 10, "genres": 6, "platforms": 5},
            "timestamp": "2024-01-01T00:00:00Z",
        }
        mock_pipeline_cls.return_value = mock_pipeline

        result = run_full_pipeline_task(page_size=25, max_pages=5)

        mock_pipeline.run_full_load.assert_called_once_with(page_size=25, max_pages=5)
        assert "rawg" in result
        assert result["rawg"]["total_games"] == 10

    @patch("gaming_pipeline.orchestrate.tasks.GamingPipeline")
    @patch("gaming_pipeline.orchestrate.tasks.create_markdown_artifact")
    def test_creates_artifact(
        self, mock_artifact: MagicMock, mock_pipeline_cls: MagicMock
    ) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline.run_full_load.return_value = {
            "rawg": {"total_games": 10, "genres": 6, "platforms": 5},
            "timestamp": "2024-01-01T00:00:00Z",
        }
        mock_pipeline_cls.return_value = mock_pipeline

        run_full_pipeline_task(page_size=25, max_pages=5)

        mock_artifact.assert_called_once()
        call_args = mock_artifact.call_args
        assert call_args.kwargs["key"] == "pipeline-execution-summary"

    @patch("gaming_pipeline.orchestrate.tasks.GamingPipeline")
    @patch("gaming_pipeline.orchestrate.tasks.create_markdown_artifact")
    def test_returns_result_dict(
        self, mock_artifact: MagicMock, mock_pipeline_cls: MagicMock
    ) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline.run_full_load.return_value = {
            "rawg": {"total_games": 10, "genres": 6, "platforms": 5},
            "timestamp": "2024-01-01T00:00:00Z",
        }
        mock_pipeline_cls.return_value = mock_pipeline

        result = run_full_pipeline_task()

        assert isinstance(result, dict)
        assert "rawg" in result


class TestGetPipelineSchemaTask:
    """Test get_pipeline_schema_task Prefect task."""

    @patch("gaming_pipeline.orchestrate.tasks.GamingPipeline")
    def test_returns_schema(self, mock_pipeline_cls: MagicMock) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline.get_schema.return_value = {"tables": ["games", "genres"]}
        mock_pipeline_cls.return_value = mock_pipeline

        result = get_pipeline_schema_task()

        assert result == {"tables": ["games", "genres"]}
        mock_pipeline.get_schema.assert_called_once()


class TestGetLoadInfoTask:
    """Test get_load_info_task Prefect task."""

    @patch("gaming_pipeline.orchestrate.tasks.GamingPipeline")
    def test_returns_load_info(self, mock_pipeline_cls: MagicMock) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline.get_load_info.return_value = {"last_load": "2024-01-01"}
        mock_pipeline_cls.return_value = mock_pipeline

        result = get_load_info_task()

        assert result == {"last_load": "2024-01-01"}
        mock_pipeline.get_load_info.assert_called_once()


class TestRefreshSchemaTask:
    """Test refresh_schema_task Prefect task."""

    @patch("gaming_pipeline.orchestrate.tasks.GamingPipeline")
    def test_calls_refresh_schema(self, mock_pipeline_cls: MagicMock) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline_cls.return_value = mock_pipeline

        refresh_schema_task()

        mock_pipeline.refresh_schema.assert_called_once()


class TestRunSQLMeshTask:
    """Test run_sqlmesh_task Prefect task."""

    @patch("subprocess.run")
    @patch("gaming_pipeline.orchestrate.tasks.create_markdown_artifact")
    def test_returns_success_result(
        self, mock_artifact: MagicMock, mock_run: MagicMock
    ) -> None:
        mock_run.return_value = MagicMock(
            returncode=0, stdout="All tests passed", stderr=""
        )

        result = run_sqlmesh_task()

        assert result["returncode"] == 0
        assert "stdout" in result
        mock_artifact.assert_called_once()

    @patch("subprocess.run")
    @patch("gaming_pipeline.orchestrate.tasks.create_markdown_artifact")
    def test_returns_failure_result(
        self, mock_artifact: MagicMock, mock_run: MagicMock
    ) -> None:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Test failed")

        result = run_sqlmesh_task()

        assert result["returncode"] == 1

    @patch("subprocess.run")
    @patch("gaming_pipeline.orchestrate.tasks.create_markdown_artifact")
    def test_handles_timeout(
        self, mock_artifact: MagicMock, mock_run: MagicMock
    ) -> None:
        from subprocess import TimeoutExpired

        mock_run.side_effect = TimeoutExpired("sqlmesh", 300)

        result = run_sqlmesh_task()

        assert result["returncode"] == -1
        assert "Timed out" in result["stderr"]

    @patch("subprocess.run")
    @patch("gaming_pipeline.orchestrate.tasks.create_markdown_artifact")
    def test_handles_exception(
        self, mock_artifact: MagicMock, mock_run: MagicMock
    ) -> None:
        mock_run.side_effect = OSError("sqlmesh not found")

        result = run_sqlmesh_task()

        assert result["returncode"] == 1
        assert "sqlmesh not found" in result["stderr"]


class TestPipelineFlow:
    """Test pipeline_flow Prefect flow."""

    @patch("gaming_pipeline.orchestrate.flows.run_sqlmesh_task")
    @patch("gaming_pipeline.orchestrate.flows.run_full_pipeline_task")
    @patch("gaming_pipeline.orchestrate.flows.get_pipeline_schema_task")
    @patch("gaming_pipeline.orchestrate.flows.get_load_info_task")
    @patch("gaming_pipeline.orchestrate.flows.refresh_schema_task")
    def test_calls_all_tasks(
        self,
        mock_refresh: MagicMock,
        mock_load_info: MagicMock,
        mock_schema: MagicMock,
        mock_run_pipeline: MagicMock,
        mock_sqlmesh: MagicMock,
    ) -> None:
        mock_run_pipeline.return_value = {"rawg": {"total_games": 10}}
        mock_sqlmesh.return_value = {"returncode": 0}
        mock_schema.return_value = {}
        mock_load_info.return_value = {}

        pipeline_flow(page_size=25, max_pages=5)

        mock_run_pipeline.assert_called_once_with(page_size=25, max_pages=5)
        mock_sqlmesh.assert_called_once()
        mock_schema.assert_called_once()
        mock_load_info.assert_called_once()
        mock_refresh.assert_called_once()

    @patch("gaming_pipeline.orchestrate.flows.run_sqlmesh_task")
    @patch("gaming_pipeline.orchestrate.flows.run_full_pipeline_task")
    @patch("gaming_pipeline.orchestrate.flows.get_pipeline_schema_task")
    @patch("gaming_pipeline.orchestrate.flows.get_load_info_task")
    @patch("gaming_pipeline.orchestrate.flows.refresh_schema_task")
    def test_raises_on_sqlmesh_failure(
        self,
        mock_refresh: MagicMock,
        mock_load_info: MagicMock,
        mock_schema: MagicMock,
        mock_run_pipeline: MagicMock,
        mock_sqlmesh: MagicMock,
    ) -> None:
        mock_run_pipeline.return_value = {"rawg": {"total_games": 10}}
        mock_sqlmesh.return_value = {"returncode": 1, "stderr": "failed"}

        with pytest.raises(ValueError, match="SQLMesh transformation failed"):
            pipeline_flow()

    @patch("gaming_pipeline.orchestrate.flows.run_sqlmesh_task")
    @patch("gaming_pipeline.orchestrate.flows.run_full_pipeline_task")
    @patch("gaming_pipeline.orchestrate.flows.get_pipeline_schema_task")
    @patch("gaming_pipeline.orchestrate.flows.get_load_info_task")
    @patch("gaming_pipeline.orchestrate.flows.refresh_schema_task")
    def test_returns_dict_with_results(
        self,
        mock_refresh: MagicMock,
        mock_load_info: MagicMock,
        mock_schema: MagicMock,
        mock_run_pipeline: MagicMock,
        mock_sqlmesh: MagicMock,
    ) -> None:
        mock_run_pipeline.return_value = {"rawg": {"total_games": 10}}
        mock_sqlmesh.return_value = {"returncode": 0}
        mock_schema.return_value = {}
        mock_load_info.return_value = {}

        result = pipeline_flow()

        assert isinstance(result, dict)
        assert "pipeline_result" in result
        assert "sqlmesh_result" in result
        assert "schema" in result
        assert "load_info" in result
        assert "execution_time" in result
