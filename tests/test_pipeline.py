"""Pipeline test module."""

import os
import time
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
from openhexa.sdk.pipelines.heartbeat import HeartbeatThread
from openhexa.sdk.pipelines.log_level import LogLevel
from openhexa.sdk.pipelines.parameter import Parameter, ParameterValueError
from openhexa.sdk.pipelines.pipeline import Pipeline
from openhexa.sdk.utils import Environment


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
@patch("openhexa.sdk.pipelines.heartbeat.OpenHexaClient")
@patch("openhexa.sdk.utils.get_environment")
def test_pipeline_sends_heartbeats_during_execution(mock_get_environment, mock_client_class):
    """Test that pipeline sends heartbeats during execution and stops thread on completion."""
    mock_get_environment.return_value = Environment.CLOUD_PIPELINE
    mock_client_instance = Mock()
    mock_result = Mock(success=True, errors=[])
    mock_client_instance.update_pipeline_heartbeat.return_value = mock_result
    mock_client_class.return_value = mock_client_instance

    def slow_pipeline(arg1):
        time.sleep(0.2)  # Sleep to allow heartbeats to be sent

    parameter_1 = Parameter("arg1", type=str, default="default")
    pipeline = Pipeline("pipeline", slow_pipeline, [parameter_1])

    original_init = HeartbeatThread.__init__

    def fast_init(self, run_context, interval=30):
        original_init(self, run_context, interval=0.05)  # 50ms interval for testing

    with patch.object(HeartbeatThread, "__init__", fast_init):
        pipeline.run({"arg1": "test_value"})

    assert (
        mock_client_instance.update_pipeline_heartbeat.call_count >= 2
    ), "Verify multiple heartbeats were sent (should be at least 2-3 in 200ms)"


@patch.dict(
    os.environ,
    {
        "HEXA_SERVER_URL": "https://test.openhexa.org",
        "HEXA_TOKEN": "test-token",
        "HEXA_RUN_ID": "test-run-id",
    },
)
@patch("openhexa.sdk.pipelines.heartbeat.OpenHexaClient")
@patch("openhexa.sdk.utils.get_environment")
def test_pipeline_continues_execution_when_heartbeat_fails(mock_get_environment, mock_client_class):
    """Test that pipeline execution continues even when heartbeats fail."""
    mock_get_environment.return_value = Environment.CLOUD_PIPELINE
    mock_client_instance = Mock()
    # Simulate heartbeat failure
    mock_client_instance.update_pipeline_heartbeat.side_effect = Exception("Network error")
    mock_client_class.return_value = mock_client_instance

    execution_completed = False

    def pipeline_with_side_effect(arg1):
        nonlocal execution_completed
        time.sleep(0.2)  # Sleep to allow heartbeat attempts
        execution_completed = True

    parameter_1 = Parameter("arg1", type=str, default="default")
    pipeline = Pipeline("pipeline", pipeline_with_side_effect, [parameter_1])

    original_init = HeartbeatThread.__init__

    def fast_init(self, run_context, interval=30):
        original_init(self, run_context, interval=0.05)  # 50ms interval for testing

    with patch.object(HeartbeatThread, "__init__", fast_init):
        pipeline.run({"arg1": "test_value"})

    assert execution_completed, "Pipeline should complete even when heartbeats fail"

    assert (
        mock_client_instance.update_pipeline_heartbeat.call_count >= 2
    ), "Heartbeat should have been attempted multiple times despite failures"


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
