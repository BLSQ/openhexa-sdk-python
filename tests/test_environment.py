"""Collection of tests related to environment variables handling."""

import os
from unittest.mock import Mock, patch

from openhexa.sdk.pipelines.pipeline import Pipeline


@patch.dict(os.environ, {"WORKSPACE_FILES_PATH": "/workspace/path"})
def test_workspace_local_files_path(workspace):
    """Test workspace files_path property with explicit environment variable."""
    assert workspace.files_path == "/workspace/path"


@patch.dict(os.environ, {"HEXA_ENVIRONMENT": "LOCAL_PIPELINE"})
def test_workspace_pipeline_files_path(workspace):
    """Test workspace files_path property in local mode."""
    from openhexa.sdk.workspaces import workspace

    assert workspace.files_path == "/home/hexa/workspace"


@patch.dict(
    os.environ,
    {"HEXA_ENVIRONMENT": "CLOUD_PIPELINE", "HEXA_SERVER_URL": "https://test.openhexa.org"},
)
def test_connected(current_run):
    """Test run _connected property in CLOUD_PIPELINE mode."""
    assert current_run._connected is True


@patch.dict(
    os.environ,
    {
        "HEXA_ENVIRONMENT": "CLOUD_PIPELINE",
    },
)
def test_not_connected_missing_url(current_run):
    """Test run _connected property in CLOUD_PIPELINE mode (missing HEXA_SERVER_URL)."""
    assert current_run._connected is False


@patch.dict(
    os.environ,
    {
        "HEXA_ENVIRONMENT": "LOCAL_PIPELINE",
    },
)
def test_not_connected(current_run):
    """Test run _connected property in LOCAL_PIPELINE mode."""
    assert current_run._connected is False


@patch.dict(
    os.environ,
    {
        "HEXA_ENVIRONMENT": "LOCAL_PIPELINE",
    },
)
def test_pipeline_local():
    """Test pipeline _connected property in LOCAL_PIPELINE mode."""
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
    """Test pipeline _connected property in CLOUD_PIPELINE mode."""
    pipeline_func = Mock()

    pipeline = Pipeline("code", "pipeline", pipeline_func, [])
    assert pipeline._connected is True
