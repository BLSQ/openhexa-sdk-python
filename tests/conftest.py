"""Module-level test fixtures."""

from importlib import reload
from unittest import mock

import pytest

import openhexa.cli
import openhexa.sdk
from openhexa.sdk.pipelines.log_level import LogLevel


@pytest.fixture(scope="function")
def workspace():
    """Build workspace fixture."""
    from openhexa.sdk import workspace as global_workspace

    reload(openhexa.sdk)

    return global_workspace


@pytest.fixture(scope="function")
def current_run():
    """Build current run fixture."""
    from openhexa.sdk import current_run as global_current_run

    reload(openhexa.sdk)

    return global_current_run


@pytest.fixture(scope="function", autouse=True)
def settings(monkeypatch):
    """Build settings fixture."""
    settings_mock = mock.MagicMock()
    monkeypatch.setattr("openhexa.cli.settings.settings", settings_mock)
    reload(openhexa.cli.api)
    settings_mock.current_workspace = "workspace-slug"
    settings_mock.api_url = "http://localhost:8000/graphql"
    settings_mock.workspaces = {"workspace-slug": "token", "another-workspace-slug": "token"}
    settings_mock.debug = False
    settings_mock.access_token = "token"
    settings_mock.log_level = LogLevel.INFO
    settings_mock.verify_ssl = True
    return settings_mock
