"""Tests for install_default_user_agent(), which makes the pipeline User-Agent the default of common HTTP libraries."""

import os
import urllib.request
from importlib.metadata import version
from unittest.mock import patch

import httpx
import httpx._client
import pytest
import requests
import requests.utils
import urllib3.connection

from openhexa.utils import get_user_agent, install_default_user_agent

SDK_USER_AGENT = f"openhexa-sdk/{version('openhexa.sdk')}"
PIPELINE_ENV = {"HEXA_WORKSPACE": "my-workspace", "HEXA_PIPELINE_CODE": "my-pipeline", "HEXA_RUN_ID": "my-run-id"}
URL = "https://example.com/"


def default_user_agents():
    """Return the User-Agent each library would send when the caller does not set one."""
    return {
        "requests": requests.Session().prepare_request(requests.Request("GET", URL)).headers["User-Agent"],
        "urllib": dict(urllib.request.build_opener().addheaders)["User-agent"],
        "urllib3": urllib3.connection._get_default_user_agent(),
        "httpx": httpx.Client().build_request("GET", URL).headers["User-Agent"],
    }


@pytest.fixture(autouse=True)
def restore_patched_attributes():
    """Undo the patches after each test so that they do not leak into other tests."""
    saved = (
        requests.utils.default_user_agent,
        urllib.request.OpenerDirector.__init__,
        urllib3.connection._get_default_user_agent,
        httpx._client.USER_AGENT,
    )
    yield
    (
        requests.utils.default_user_agent,
        urllib.request.OpenerDirector.__init__,
        urllib3.connection._get_default_user_agent,
        httpx._client.USER_AGENT,
    ) = saved


@patch.dict(os.environ, PIPELINE_ENV, clear=True)
def test_default_user_agent():
    """Every library defaults to the pipeline User-Agent."""
    install_default_user_agent()
    assert set(default_user_agents().values()) == {get_user_agent()}
    assert "run_id=my-run-id" in get_user_agent()


@patch.dict(os.environ, {}, clear=True)
def test_default_user_agent_outside_pipeline():
    """Without pipeline context, the default is the plain SDK User-Agent."""
    install_default_user_agent()
    assert set(default_user_agents().values()) == {SDK_USER_AGENT}


@patch.dict(os.environ, PIPELINE_ENV, clear=True)
def test_explicit_user_agent_wins():
    """A User-Agent set explicitly by the caller is kept."""
    install_default_user_agent()
    headers = {"User-Agent": "my-client/1.0"}
    request = requests.Session().prepare_request(requests.Request("GET", URL, headers=headers))
    assert request.headers["User-Agent"] == "my-client/1.0"
    assert httpx.Client().build_request("GET", URL, headers=headers).headers["User-Agent"] == "my-client/1.0"


@patch.dict(os.environ, {**PIPELINE_ENV, "HEXA_DISABLE_USER_AGENT_PATCH": "true"}, clear=True)
def test_kill_switch():
    """HEXA_DISABLE_USER_AGENT_PATCH leaves the libraries' own defaults untouched."""
    before = default_user_agents()
    install_default_user_agent()
    assert default_user_agents() == before


@patch.dict(os.environ, PIPELINE_ENV, clear=True)
def test_install_twice():
    """Calling the function twice does not stack the urllib wrapper."""
    original_init = urllib.request.OpenerDirector.__init__
    install_default_user_agent()
    install_default_user_agent()
    assert urllib.request.OpenerDirector.__init__.__wrapped__ is original_init
    assert set(default_user_agents().values()) == {get_user_agent()}
