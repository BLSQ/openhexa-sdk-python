import os
from unittest.mock import Mock, patch

from openhexa.sdk import current_run, workspace
from openhexa.sdk.pipelines.pipeline import Pipeline


@patch.dict(os.environ, {"WORKSPACE_FILES_PATH": "/workspace/path"})
def test_workspace_local_files_path():
    assert workspace.files_path == "/workspace/path"


@patch.dict(os.environ, {"HEXA_ENVIRONMENT": "PIPELINE"})
def test_workspace_pipeline_files_path():
    assert workspace.files_path == "/home/hexa/workspace"


@patch.dict(
    os.environ,
    {"HEXA_ENVIRONMENT": "PIPELINE", "HEXA_SERVER_URL": "https://test.openhexa.org"},
)
def test_connected():
    assert current_run.connected is True


@patch.dict(
    os.environ,
    {"HEXA_ENVIRONMENT": "LOCAL", "HEXA_SERVER_URL": "https://test.openhexa.org"},
)
def test_not_connected():
    assert current_run.connected is False


@patch.dict(
    os.environ,
    {
        "HEXA_ENVIRONMENT": "LOCAL",
    },
)
def test_not_connected_missing_url():
    assert current_run.connected is False


@patch.dict(
    os.environ,
    {
        "HEXA_ENVIRONMENT": "LOCAL",
    },
)
def test_pipeline_local():
    pipeline_func = Mock()

    pipeline = Pipeline("code", "pipeline", pipeline_func, [])
    assert pipeline.connected is False


@patch.dict(
    os.environ,
    {
        "HEXA_ENVIRONMENT": "PIPELINE",
        "HEXA_SERVER_URL": "https://test.openhexa.org",
    },
)
def test_pipeline_pipeline():
    pipeline_func = Mock()

    pipeline = Pipeline("code", "pipeline", pipeline_func, [])
    assert pipeline.connected is True
