"""Module-level test fixtures."""
from importlib import reload

import pytest

import openhexa.sdk


@pytest.fixture(scope="function")
def workspace():
    from openhexa.sdk import workspace as global_workspace

    reload(openhexa.sdk)

    return global_workspace


@pytest.fixture(scope="function")
def current_run():
    from openhexa.sdk import current_run as global_current_run

    reload(openhexa.sdk)

    return global_current_run
