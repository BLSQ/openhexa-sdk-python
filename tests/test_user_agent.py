"""Collection of tests related to the User-Agent identifying the current pipeline."""

import os
from importlib.metadata import version
from unittest.mock import patch

from openhexa.graphql import BaseOpenHexaClient
from openhexa.utils import create_requests_session, get_user_agent

RUN_ID = "9a4ee4b5-5e0b-4b3b-9d4c-1f2c7b7f0d0e"
SDK_USER_AGENT = f"openhexa-sdk/{version('openhexa.sdk')}"
PIPELINE_ENV = {"HEXA_WORKSPACE": "my-workspace", "HEXA_PIPELINE_CODE": "my-pipeline", "HEXA_RUN_ID": RUN_ID}
PIPELINE_USER_AGENT = f"{SDK_USER_AGENT} (workspace=my-workspace; pipeline=my-pipeline; run_id={RUN_ID})"


@patch.dict(os.environ, PIPELINE_ENV, clear=True)
def test_get_user_agent():
    """The User-Agent identifies the workspace, pipeline and run when they are set."""
    assert get_user_agent() == PIPELINE_USER_AGENT


@patch.dict(os.environ, {"HEXA_WORKSPACE": "my-workspace"}, clear=True)
def test_get_user_agent_partial():
    """The User-Agent only contains the values that are available."""
    assert get_user_agent() == f"{SDK_USER_AGENT} (workspace=my-workspace)"


@patch.dict(os.environ, {}, clear=True)
def test_get_user_agent_outside_pipeline():
    """The User-Agent is the plain SDK one outside of a pipeline context."""
    assert get_user_agent() == SDK_USER_AGENT


@patch.dict(os.environ, PIPELINE_ENV, clear=True)
def test_requests_session_user_agent():
    """Sessions created by the SDK identify the pipeline in their User-Agent."""
    assert create_requests_session().headers["User-Agent"] == PIPELINE_USER_AGENT


@patch.dict(os.environ, PIPELINE_ENV, clear=True)
def test_graphql_client_user_agent():
    """The GraphQL client identifies the pipeline in its User-Agent."""
    client = BaseOpenHexaClient(url="https://test.openhexa.org/graphql/", token="token")
    assert client.http_client.headers["User-Agent"] == PIPELINE_USER_AGENT
