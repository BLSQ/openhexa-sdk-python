"""Pipeline test module."""

import os
from unittest.mock import Mock, patch

import pytest

from openhexa.sdk import (
    DHIS2Connection,
    GCSConnection,
    IASOConnection,
    PostgreSQLConnection,
    S3Connection,
)
from openhexa.sdk.pipelines.parameter import Parameter, ParameterValueError
from openhexa.sdk.pipelines.pipeline import Pipeline


def test_pipeline_run_valid_config():
    """Happy path for pipeline run config."""
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    parameter_2 = Parameter("arg2", type=str, multiple=True)
    parameter_3 = Parameter("arg3", type=int, default=33)
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1, parameter_2, parameter_3])
    pipeline.run({"arg1": "ab", "arg2": ["cd", "ef"]})

    assert pipeline.name == "pipeline"
    pipeline_func.assert_called_once_with(arg1="ab", arg2=["cd", "ef"], arg3=33)


def test_pipeline_run_invalid_config():
    """Verify thatinvalid configuration values raise an exception."""
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1])
    with pytest.raises(ParameterValueError):
        pipeline.run({"arg1": 3})


def test_pipeline_run_extra_config():
    """Verify that extra (unexpected) configuration values raise an exception."""
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1])
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
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1])

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
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1])

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
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1])

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
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1])

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

    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1])

    data = PostgreSQLConnection(host, port, username, password, database_name)
    with patch.object(workspace, "get_connection", return_value=data):
        pipeline.run({"connection_param": identifier})
        assert pipeline.name == "pipeline"
        pipeline_func.assert_called_once_with(
            connection_param=PostgreSQLConnection(host, port, username, password, database_name)
        )


def test_pipeline_parameters_spec():
    """Base checks for parameter specs building."""
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    parameter_2 = Parameter("arg2", type=str, multiple=True)
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1, parameter_2])

    assert pipeline.parameters_spec() == [
        {
            "code": "arg1",
            "name": None,
            "type": "str",
            "required": True,
            "choices": None,
            "help": None,
            "multiple": False,
            "default": None,
        },
        {
            "code": "arg2",
            "name": None,
            "type": "str",
            "required": True,
            "choices": None,
            "help": None,
            "multiple": True,
            "default": None,
        },
    ]
