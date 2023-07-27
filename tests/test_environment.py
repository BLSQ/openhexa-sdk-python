import os
from unittest.mock import Mock, patch

from openhexa.sdk.pipelines.pipeline import Pipeline


@patch.dict(os.environ, {"WORKSPACE_FILES_PATH": "/workspace/path"})
def test_workspace_local_files_path():
    from openhexa.sdk.workspaces import workspace

    assert workspace.files_path == "/workspace/path"


@patch.dict(os.environ, {"HEXA_ENVIRONMENT": "LOCAL_PIPELINE"})
def test_workspace_pipeline_files_path():
    from openhexa.sdk.workspaces import workspace

    assert workspace.files_path == "/home/hexa/workspace"


@patch.dict(
    os.environ,
    {"HEXA_ENVIRONMENT": "CLOUD_PIPELINE", "HEXA_SERVER_URL": "https://test.openhexa.org"},
)
def test_connected():
    from openhexa.sdk.pipelines import current_run

    assert current_run._connected is True


@patch.dict(
    os.environ,
    {
        "HEXA_ENVIRONMENT": "LOCAL_PIPELINE",
    },
)
def test_not_connected():
    from openhexa.sdk.pipelines import current_run

    assert current_run._connected is False


@patch.dict(
    os.environ,
    {
        "HEXA_ENVIRONMENT": "LOCAL_PIPELINE",
    },
)
def test_not_connected_missing_url():
    from openhexa.sdk.pipelines import current_run

    assert current_run._connected is False


@patch.dict(
    os.environ,
    {
        "HEXA_ENVIRONMENT": "LOCAL_PIPELINE",
    },
)
def test_pipeline_local():
    pipeline_func = Mock()

    pipeline = Pipeline("code", "pipeline", pipeline_func, [])
    assert pipeline._connected is False


@patch.dict(
    os.environ,
    {
        "HEXA_ENVIRONMENT": "CLOUD_PIPELINE",
        "HEXA_SERVER_URL": "https://test.openhexa.org",
    },
)
def test_pipeline_pipeline():
    pipeline_func = Mock()

    pipeline = Pipeline("code", "pipeline", pipeline_func, [])
    assert pipeline._connected is True
