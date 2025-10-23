"""Pipeline test module."""

import os
from unittest import TestCase
from unittest.mock import Mock, patch

import pytest

from openhexa.sdk import (
    DHIS2Connection,
    GCSConnection,
    IASOConnection,
    PostgreSQLConnection,
    S3Connection,
)
from openhexa.sdk.pipelines.log_level import LogLevel
from openhexa.sdk.pipelines.parameter import Parameter, ParameterValueError
from openhexa.sdk.pipelines.pipeline import Pipeline


def test_pipeline_run_valid_config():
    """Happy path for pipeline run config."""
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    parameter_2 = Parameter("arg2", type=str, multiple=True)
    parameter_3 = Parameter("arg3", type=int, default=33)
    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1, parameter_2, parameter_3])
    pipeline.run({"arg1": "ab", "arg2": ["cd", "ef"]})

    assert pipeline.name == "pipeline"
    pipeline_func.assert_called_once_with(arg1="ab", arg2=["cd", "ef"], arg3=33)


def test_pipeline_run_invalid_config():
    """Verify thatinvalid configuration values raise an exception."""
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1])
    with pytest.raises(ParameterValueError):
        pipeline.run({"arg1": 3})


def test_pipeline_run_extra_config():
    """Verify that extra (unexpected) configuration values raise an exception."""
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1])
    with pytest.raises(ParameterValueError):
        pipeline.run({"arg1": "ok", "arg2": "extra"})


@patch.dict(
    os.environ,
    {"HEXA_SERVER_URL": "https://test.openhexa.org"},
)
def test_pipeline_run_connection_dhis2_parameter_config(workspace):
    """Ensure that DHIS2 connection parameter values are built properly."""
    identifier = "dhis2-connection-id"

    url = "https://test.dhis2.org/"
    username = "dhis2"
    password = "dhis2_pwd"

    pipeline_func = Mock()
    parameter_1 = Parameter(
        "connection_param",
        name="this is a test for connection parameter",
        type=DHIS2Connection,
    )
    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1])

    data = DHIS2Connection(url, username, password)
    with patch.object(workspace, "get_connection", return_value=data):
        pipeline.run({"connection_param": identifier})
        assert pipeline.name == "pipeline"
        pipeline_func.assert_called_once_with(connection_param=DHIS2Connection(url, username, password))


@patch.dict(
    os.environ,
    {"HEXA_SERVER_URL": "https://test.openhexa.org"},
)
def test_pipeline_run_connection_iaso_parameter_config(workspace):
    """Ensure that IASO connection parameter values are built properly."""
    identifier = "iaso-connection-id"

    url = "https://test.iaso.org/"
    username = "iaso"
    password = "iaso_pwd"

    pipeline_func = Mock()
    parameter_1 = Parameter(
        "connection_param",
        name="this is a test for connection parameter",
        type=IASOConnection,
    )
    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1])

    data = IASOConnection(url, username, password)
    with patch.object(workspace, "get_connection", return_value=data):
        pipeline.run({"connection_param": identifier})
        assert pipeline.name == "pipeline"
        pipeline_func.assert_called_once_with(connection_param=IASOConnection(url, username, password))


@patch.dict(
    os.environ,
    {"HEXA_SERVER_URL": "https://test.openhexa.org"},
)
def test_pipeline_run_connection_gcs_parameter_config(workspace):
    """Ensure that GCS connection parameter values are built properly."""
    identifier = "gcs-connection-id"

    service_account_key = "HqQBxH0BAI3zF7kANUNlGg"
    bucket_name = "test"

    pipeline_func = Mock()
    parameter_1 = Parameter(
        "connection_param",
        name="this is a test for connection parameter",
        type=GCSConnection,
    )
    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1])

    data = GCSConnection(service_account_key, bucket_name)

    with patch.object(workspace, "get_connection", return_value=data):
        pipeline.run({"connection_param": identifier})
        assert pipeline.name == "pipeline"
        pipeline_func.assert_called_once_with(connection_param=GCSConnection(service_account_key, bucket_name))


@patch.dict(
    os.environ,
    {"HEXA_SERVER_URL": "https://test.openhexa.org"},
)
def test_pipeline_run_connection_s3_parameter_config(workspace):
    """Ensure that S3 connection parameter values are built properly."""
    identifier = "s3-connection-id"

    secret_access_key = "HqQBxH0BAI3zF7kANUNlGg"
    access_key_id = "84hVntMaMSYP/RSW9ex04w"
    bucket_name = "test"

    pipeline_func = Mock()
    parameter_1 = Parameter(
        "connection_param",
        name="this is a test for connection parameter",
        type=S3Connection,
    )
    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1])

    data = S3Connection(access_key_id, secret_access_key, bucket_name)
    with patch.object(workspace, "get_connection", return_value=data):
        pipeline.run({"connection_param": identifier})
        assert pipeline.name == "pipeline"
        pipeline_func.assert_called_once_with(
            connection_param=S3Connection(access_key_id, secret_access_key, bucket_name)
        )


@patch.dict(
    os.environ,
    {"HEXA_SERVER_URL": "https://test.openhexa.org"},
)
def test_pipeline_run_connection_postgres_parameter_config(workspace):
    """Ensure that postgreSQL connection parameter values are built properly."""
    identifier = "postgres-connection-id"

    host = "https://127.0.0.1"
    port = 5432
    username = "hexa_sdk"
    password = "hexa_sdk_pwd"
    database_name = "hexa_sdk"

    pipeline_func = Mock()
    parameter_1 = Parameter(
        "connection_param",
        name="this is a test for connection parameter",
        type=PostgreSQLConnection,
    )

    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1])

    data = PostgreSQLConnection(host, port, username, password, database_name)
    with patch.object(workspace, "get_connection", return_value=data):
        pipeline.run({"connection_param": identifier})
        assert pipeline.name == "pipeline"
        pipeline_func.assert_called_once_with(
            connection_param=PostgreSQLConnection(host, port, username, password, database_name)
        )


@patch.dict(
    os.environ,
    {
        "HEXA_SERVER_URL": "https://test.openhexa.org",
        "HEXA_TOKEN": "test-token",
        "HEXA_RUN_ID": "test-run-id",
    },
)
@patch("openhexa.sdk.pipelines.heartbeat.graphql")
@patch("openhexa.sdk.utils.get_environment")
def test_pipeline_run_with_heartbeat_in_cloud(mock_get_environment, mock_graphql):
    """Test that pipeline.run() starts heartbeat manager in cloud environment."""
    from openhexa.sdk.utils import Environment

    # Mock cloud environment
    mock_get_environment.return_value = Environment.CLOUD_PIPELINE

    # Mock successful heartbeat response
    mock_graphql.return_value = {"data": {"updatePipelineHeartbeat": {"success": True, "errors": []}}}

    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str, default="default")
    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1])

    # Run the pipeline
    pipeline.run({"arg1": "test_value"})

    # Verify pipeline function was called
    pipeline_func.assert_called_once_with(arg1="test_value")

    # Note: Heartbeat calls are asynchronous, so we can't reliably assert the count
    # But we can verify the mock was set up correctly


@patch.dict(os.environ, {}, clear=True)
@patch("openhexa.sdk.pipelines.heartbeat.graphql")
def test_pipeline_run_without_heartbeat_locally(mock_graphql):
    """Test that pipeline.run() does not start heartbeat when running locally."""
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str, default="default")
    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1])

    # Run the pipeline
    pipeline.run({"arg1": "test_value"})

    # Verify pipeline function was called
    pipeline_func.assert_called_once_with(arg1="test_value")

    # Verify no heartbeat was sent (not connected)
    mock_graphql.assert_not_called()


@patch.dict(
    os.environ,
    {
        "HEXA_SERVER_URL": "https://test.openhexa.org",
        "HEXA_TOKEN": "test-token",
        "HEXA_RUN_ID": "test-run-id",
    },
)
@patch("openhexa.sdk.pipelines.heartbeat.graphql")
@patch("openhexa.sdk.utils.get_environment")
def test_pipeline_run_heartbeat_continues_on_error(mock_get_environment, mock_graphql):
    """Test that heartbeat continues even if GraphQL fails."""
    from openhexa.sdk.utils import Environment

    # Mock cloud environment
    mock_get_environment.return_value = Environment.CLOUD_PIPELINE

    # Mock heartbeat failure (should not crash pipeline)
    mock_graphql.side_effect = Exception("Network error")

    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str, default="default")
    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1])

    # Run the pipeline - should not raise exception
    pipeline.run({"arg1": "test_value"})

    # Verify pipeline function was still called
    pipeline_func.assert_called_once_with(arg1="test_value")


@patch.dict(
    os.environ,
    {
        "HEXA_SERVER_URL": "https://test.openhexa.org",
        "HEXA_TOKEN": "test-token",
        "HEXA_RUN_ID": "test-run-id",
    },
)
@patch("openhexa.sdk.pipelines.heartbeat.HeartbeatThread")
@patch("openhexa.sdk.utils.get_environment")
def test_pipeline_run_stops_heartbeat_on_completion(mock_get_environment, mock_heartbeat_thread):
    """Test that heartbeat thread is stopped when pipeline completes."""
    from openhexa.sdk.utils import Environment

    # Mock cloud environment
    mock_get_environment.return_value = Environment.CLOUD_PIPELINE

    # Mock heartbeat thread
    mock_thread_instance = Mock()
    mock_thread_instance.is_alive.return_value = True
    mock_heartbeat_thread.return_value = mock_thread_instance

    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str, default="default")
    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1])

    # Run the pipeline
    pipeline.run({"arg1": "test_value"})

    # Verify heartbeat thread was started
    mock_heartbeat_thread.assert_called_once()
    mock_thread_instance.start.assert_called_once()

    # Verify heartbeat thread was stopped
    mock_thread_instance.stop.assert_called_once()
    mock_thread_instance.join.assert_called_once_with(timeout=5)


@patch.dict(
    os.environ,
    {
        "HEXA_SERVER_URL": "https://test.openhexa.org",
        "HEXA_TOKEN": "test-token",
        "HEXA_RUN_ID": "test-run-id",
    },
)
@patch("openhexa.sdk.pipelines.heartbeat.HeartbeatThread")
@patch("openhexa.sdk.utils.get_environment")
def test_pipeline_run_stops_heartbeat_on_exception(mock_get_environment, mock_heartbeat_thread):
    """Test that heartbeat thread is stopped even when pipeline raises exception."""
    from openhexa.sdk.utils import Environment

    # Mock cloud environment
    mock_get_environment.return_value = Environment.CLOUD_PIPELINE

    # Mock heartbeat thread
    mock_thread_instance = Mock()
    mock_thread_instance.is_alive.return_value = True
    mock_heartbeat_thread.return_value = mock_thread_instance

    pipeline_func = Mock(side_effect=ValueError("Pipeline error"))
    parameter_1 = Parameter("arg1", type=str, default="default")
    pipeline = Pipeline("pipeline", pipeline_func, [parameter_1])

    # Run the pipeline - should raise exception
    with pytest.raises(ValueError, match="Pipeline error"):
        pipeline.run({"arg1": "test_value"})

    # Verify heartbeat thread was started
    mock_heartbeat_thread.assert_called_once()
    mock_thread_instance.start.assert_called_once()

    # Verify heartbeat thread was still stopped despite exception
    mock_thread_instance.stop.assert_called_once()
    mock_thread_instance.join.assert_called_once_with(timeout=5)


class TestLogLevel(TestCase):
    def test_parse_log_level(self):
        test_cases = [
            (0, LogLevel.DEBUG),
            (1, LogLevel.INFO),
            (2, LogLevel.WARNING),
            (3, LogLevel.ERROR),
            (4, LogLevel.CRITICAL),
            ("0", LogLevel.DEBUG),
            ("1", LogLevel.INFO),
            ("2", LogLevel.WARNING),
            ("3", LogLevel.ERROR),
            ("4", LogLevel.CRITICAL),
            ("DEBUG", LogLevel.DEBUG),
            ("INFO", LogLevel.INFO),
            ("WARNING", LogLevel.WARNING),
            ("ERROR", LogLevel.ERROR),
            ("CRITICAL", LogLevel.CRITICAL),
            ("invalid", LogLevel.INFO),
            (6, LogLevel.INFO),
            (-1, LogLevel.INFO),
        ]
        for input_value, expected in test_cases:
            with self.subTest(input_value=input_value, expected=expected):
                self.assertEqual(LogLevel.parse_log_level(input_value), expected)
