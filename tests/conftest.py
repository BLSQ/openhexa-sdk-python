"""Module-level test fixtures."""

import pytest

from openhexa.sdk import workspace as global_workspace


@pytest.fixture(scope="module")
def workspace():
    return global_workspace
