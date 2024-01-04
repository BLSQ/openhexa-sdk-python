"""Workspace test module."""

import os
import re
from tempfile import mkdtemp
from unittest import mock

import pytest
import stringcase

from openhexa.sdk.workspaces.workspace import ConnectionDoesNotExist


def test_workspace_files_path(monkeypatch, workspace):
    """Basic checks for the Workspace.files_path() method."""
    assert workspace.files_path == "/home/hexa/workspace"

    monkeypatch.setenv("WORKSPACE_FILES_PATH", "/Users/John/openhexa/project-1/workspace")
    assert workspace.files_path == "/Users/John/openhexa/project-1/workspace"


def test_workspace_tmp_path(monkeypatch, workspace):
    """Basic checks for the Workspace.tmp_path() method."""
    assert workspace.tmp_path == "/home/hexa/tmp"

    mock_tmp_path = mkdtemp()
    monkeypatch.setenv("WORKSPACE_TMP_PATH", mock_tmp_path)
    assert workspace.tmp_path == mock_tmp_path


def test_workspace_dhis2_connection_not_exist(workspace):
    """Does not exist test case for DHIS2 connections."""
    identifier = "polio-ff3a0d"
    with pytest.raises(ConnectionDoesNotExist):
        workspace.dhis2_connection(identifier=identifier)


def test_workspace_dhis2_connection(workspace):
    """Base test case for DHIS2 connections."""
    identifier = "polio-ff3a0d"
    env_variable_prefix = stringcase.constcase(identifier)
    url = "https://test.dhis2.org/"
    username = "dhis2"
    password = "dhis2_pwd"
    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_URL": url,
            f"{env_variable_prefix}_USERNAME": username,
            f"{env_variable_prefix}_PASSWORD": password,
        },
    ):
        dhis2_connection = workspace.dhis2_connection(identifier=identifier)
        assert dhis2_connection.url == url
        assert dhis2_connection.username == username
        assert dhis2_connection.password == password
        assert re.search("password", repr(dhis2_connection), re.IGNORECASE) is None
        assert re.search("password", str(dhis2_connection), re.IGNORECASE) is None


def test_workspace_postgresql_connection_not_exist(workspace):
    """Does not exist test case for PostgreSQL connections."""
    identifier = "polio-ff3a0d"
    with pytest.raises(ConnectionDoesNotExist):
        workspace.postgresql_connection(identifier=identifier)


def test_workspace_postgresql_connection(workspace):
    """Base test case for PostgreSQL connections."""
    identifier = "polio-ff3a0d"
    env_variable_prefix = stringcase.constcase(identifier)
    host = "https://172.17.0.1"
    port = "5432"
    username = "dhis2"
    password = "dhis2_pwd"
    database_name = "polio"
    url = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"
    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_HOST": host,
            f"{env_variable_prefix}_USERNAME": username,
            f"{env_variable_prefix}_PASSWORD": password,
            f"{env_variable_prefix}_PORT": port,
            f"{env_variable_prefix}_DB_NAME": database_name,
        },
    ):
        postgres_connection = workspace.postgresql_connection(identifier=identifier)
        assert postgres_connection.username == username
        assert postgres_connection.password == password
        assert postgres_connection.host == host
        assert postgres_connection.port == int(port)
        assert postgres_connection.database_name == database_name
        assert postgres_connection.url == url
        assert re.search("password", repr(postgres_connection), re.IGNORECASE) is None
        assert re.search("password", str(postgres_connection), re.IGNORECASE) is None


def test_workspace_S3_connection_not_exist(workspace):
    """Does not exist test case for S3 connections."""
    identifier = "polio-ff3a0d"
    with pytest.raises(ConnectionDoesNotExist):
        workspace.s3_connection(identifier=identifier)


def test_workspace_s3_connection(workspace):
    """Base test case for S3 connections."""
    identifier = "polio-ff3a0d"
    env_variable_prefix = stringcase.constcase(identifier)
    secret_access_key = "HqQBxH0BAI3zF7kANUNlGg"
    access_key_id = "84hVntMaMSYP/RSW9ex04w"
    bucket_name = "test"

    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_SECRET_ACCESS_KEY": secret_access_key,
            f"{env_variable_prefix}_ACCESS_KEY_ID": access_key_id,
            f"{env_variable_prefix}_BUCKET_NAME": bucket_name,
        },
    ):
        s3_connection = workspace.s3_connection(identifier=identifier)
        assert s3_connection.secret_access_key == secret_access_key
        assert s3_connection.access_key_id == access_key_id
        assert s3_connection.bucket_name == bucket_name
        assert re.search("secret_access_key", repr(s3_connection), re.IGNORECASE) is None
        assert re.search("secret_access_key", str(s3_connection), re.IGNORECASE) is None
        assert re.search("access_key_id", repr(s3_connection), re.IGNORECASE) is None
        assert re.search("access_key_id", str(s3_connection), re.IGNORECASE) is None


def test_workspace_gcs_connection_not_exist(workspace):
    """Does not exist test case for GCS connections."""
    identifier = "polio-ff3a0d"
    with pytest.raises(ConnectionDoesNotExist):
        workspace.gcs_connection(identifier=identifier)


def test_workspace_gcs_connection(workspace):
    """Base test case for GCS connections."""
    identifier = "polio-ff3a0d"
    env_variable_prefix = stringcase.constcase(identifier)
    service_account_key = "HqQBxH0BAI3zF7kANUNlGg"
    bucket_name = "test"

    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_SERVICE_ACCOUNT_KEY": service_account_key,
            f"{env_variable_prefix}_BUCKET_NAME": bucket_name,
        },
    ):
        s3_connection = workspace.gcs_connection(identifier=identifier)
        assert s3_connection.service_account_key == service_account_key
        assert s3_connection.bucket_name == bucket_name
        assert re.search("service_account_key", repr(s3_connection), re.IGNORECASE) is None
        assert re.search("service_account_key", str(s3_connection), re.IGNORECASE) is None


def test_workspace_iaso_connection_not_exist(workspace):
    """Does not exist test case for IASO connections."""
    identifier = "iaso-account"
    with pytest.raises(ConnectionDoesNotExist):
        workspace.iaso_connection(identifier=identifier)


def test_workspace_iaso_connection(workspace):
    """Base test case for IASO connections."""
    identifier = "iaso-account"
    env_variable_prefix = stringcase.constcase(identifier)
    url = "https://test.iaso.org/"
    username = "iaso"
    password = "iaso_pwd"

    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_URL": url,
            f"{env_variable_prefix}_USERNAME": username,
            f"{env_variable_prefix}_PASSWORD": password,
        },
    ):
        iaso_connection = workspace.iaso_connection(identifier=identifier)
        assert iaso_connection.url == url
        assert iaso_connection.username == username
        assert iaso_connection.password == password
        assert re.search("password", repr(iaso_connection), re.IGNORECASE) is None
        assert re.search("password", str(iaso_connection), re.IGNORECASE) is None


def test_workspace_custom_connection_not_exist(workspace):
    """Does not exist test case for custom connections."""
    identifier = "custom-stuff"
    with pytest.raises(ConnectionDoesNotExist):
        workspace.custom_connection(identifier=identifier)


def test_workspace_custom_connection(workspace):
    """Base test case for custom connections."""
    identifier = "my_connection"
    env_variable_prefix = stringcase.constcase(identifier)
    username = "kaggle_username"
    password = "root"

    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_USERNAME": username,
            f"{env_variable_prefix}_PASSWORD": password,
        },
    ):
        custom_connection = workspace.custom_connection(identifier=identifier)
        assert custom_connection.username == username
        assert custom_connection.password == password
        assert re.search("username", repr(custom_connection), re.IGNORECASE) is None
        assert re.search("password", str(custom_connection), re.IGNORECASE) is None


def test_connection_by_slug_warning(workspace):
    """Ensure that using the slug keyword argument when getting a connection generates a deprecation warning."""
    identifier = "polio-ff3a0d"
    env_variable_prefix = stringcase.constcase(identifier)
    url = "https://test.dhis2.org/"
    username = "dhis2"
    password = "dhis2_pwd"
    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_URL": url,
            f"{env_variable_prefix}_USERNAME": username,
            f"{env_variable_prefix}_PASSWORD": password,
        },
    ):
        assert workspace.dhis2_connection(identifier).url == url
        with pytest.warns(DeprecationWarning):
            assert workspace.dhis2_connection(slug=identifier).url == url
        assert workspace.dhis2_connection(identifier=identifier).url == url


def test_connection_various_case(workspace):
    """Ensure that identifiers used when getting connections are case-insensitive."""
    env_variable_prefix = stringcase.constcase("polio-123")
    url = "https://test.dhis2.org/"
    username = "dhis2"
    password = "dhis2_pwd"
    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_URL": url,
            f"{env_variable_prefix}_USERNAME": username,
            f"{env_variable_prefix}_PASSWORD": password,
        },
    ):
        assert workspace.dhis2_connection("polio-123").url == url
        assert workspace.dhis2_connection("Polio-123").url == url
        assert workspace.dhis2_connection("POLIO-123").url == url
