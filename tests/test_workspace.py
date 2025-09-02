"""Workspace test module."""

import os
import re
from dataclasses import make_dataclass
from tempfile import mkdtemp
from unittest import mock

import pytest

from openhexa.graphql import GetConnectionConnectionBySlug
from openhexa.sdk.workspaces.connection import (
    CustomConnection,
    DHIS2Connection,
    GCSConnection,
    IASOConnection,
    PostgreSQLConnection,
    S3Connection,
)
from openhexa.sdk.workspaces.current_workspace import ConnectionDoesNotExist
from openhexa.utils import stringcase


class TestWorkspace:
    """Test class for Workspace."""

    def test_workspace_files_path(self, monkeypatch, workspace):
        """Basic checks for the Workspace.files_path() method."""
        assert workspace.files_path == "/home/hexa/workspace"

        monkeypatch.setenv("WORKSPACE_FILES_PATH", "/Users/John/openhexa/project-1/workspace")
        assert workspace.files_path == "/Users/John/openhexa/project-1/workspace"

    def test_workspace_tmp_path(self, monkeypatch, workspace):
        """Basic checks for the Workspace.tmp_path() method."""
        assert workspace.tmp_path == "/home/hexa/tmp"

        mock_tmp_path = mkdtemp()
        monkeypatch.setenv("WORKSPACE_TMP_PATH", mock_tmp_path)
        assert workspace.tmp_path == mock_tmp_path

    def test_workspace_dhis2_connection_not_exist(self, workspace):
        """Does not exist test case for DHIS2 connections."""
        identifier = "polio-ff3a0d"
        with pytest.raises(ConnectionDoesNotExist):
            workspace.dhis2_connection(identifier=identifier)

    def test_workspace_dhis2_connection(self, workspace):
        """Base test case for DHIS2 connections."""
        identifier = "polio-ff3a0d"
        env_variable_prefix = stringcase.constcase(identifier)
        url = "https://test.dhis2.org/"
        username = "dhis2"
        password = "dhis2_pwd"
        with mock.patch.dict(
            os.environ,
            {
                f"{env_variable_prefix}": "dhis2",
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

    def test_workspace_dhis2_connection_similar_prefix(self, workspace):
        """Base test case for DHIS2 connections."""
        identifier = "polio"
        identifier_2 = "polio-test"

        env_variable_prefix = stringcase.constcase(identifier)
        env_variable_prefix_2 = stringcase.constcase(identifier_2)

        url = "https://test.dhis2.org/"
        username = "dhis2"
        password = "dhis2_pwd"

        with mock.patch.dict(
            os.environ,
            {
                f"{env_variable_prefix}": "dhis2",
                f"{env_variable_prefix}_URL": url,
                f"{env_variable_prefix}_USERNAME": username,
                f"{env_variable_prefix}_PASSWORD": password,
                f"{env_variable_prefix_2}": "dhis2",
                f"{env_variable_prefix_2}_URL": "url_2",
                f"{env_variable_prefix_2}_USERNAME": "username_2",
                f"{env_variable_prefix_2}_PASSWORD": "password_2",
            },
        ):
            dhis2_connection = workspace.dhis2_connection(identifier=identifier)
            assert dhis2_connection.url == url
            assert dhis2_connection.username == username
            assert dhis2_connection.password == password

    def test_workspace_postgresql_connection_not_exist(self, workspace):
        """Does not exist test case for PostgreSQL connections."""
        identifier = "polio-ff3a0d"
        with pytest.raises(ConnectionDoesNotExist):
            workspace.postgresql_connection(identifier=identifier)

    def test_workspace_postgresql_connection(self, workspace):
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
                f"{env_variable_prefix}": "postgresql",
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

    def test_workspace_S3_connection_not_exist(self, workspace):
        """Does not exist test case for S3 connections."""
        identifier = "polio-ff3a0d"
        with pytest.raises(ConnectionDoesNotExist):
            workspace.s3_connection(identifier=identifier)

    def test_workspace_s3_connection(self, workspace):
        """Base test case for S3 connections."""
        identifier = "polio-ff3a0d"
        env_variable_prefix = stringcase.constcase(identifier)
        secret_access_key = "HqQBxH0BAI3zF7kANUNlGg"
        access_key_id = "84hVntMaMSYP/RSW9ex04w"
        bucket_name = "test"

        with mock.patch.dict(
            os.environ,
            {
                f"{env_variable_prefix}": "s3",
                f"{env_variable_prefix}_ACCESS_KEY_SECRET": secret_access_key,
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

    def test_workspace_gcs_connection_not_exist(self, workspace):
        """Does not exist test case for GCS connections."""
        identifier = "polio-ff3a0d"
        with pytest.raises(ConnectionDoesNotExist):
            workspace.gcs_connection(identifier=identifier)

    def test_workspace_gcs_connection(self, workspace):
        """Base test case for GCS connections."""
        identifier = "polio-ff3a0d"
        env_variable_prefix = stringcase.constcase(identifier)
        service_account_key = "HqQBxH0BAI3zF7kANUNlGg"
        bucket_name = "test"

        with mock.patch.dict(
            os.environ,
            {
                f"{env_variable_prefix}": "gcs",
                f"{env_variable_prefix}_SERVICE_ACCOUNT_KEY": service_account_key,
                f"{env_variable_prefix}_BUCKET_NAME": bucket_name,
            },
        ):
            s3_connection = workspace.gcs_connection(identifier=identifier)
            assert s3_connection.service_account_key == service_account_key
            assert s3_connection.bucket_name == bucket_name
            assert re.search("service_account_key", repr(s3_connection), re.IGNORECASE) is None
            assert re.search("service_account_key", str(s3_connection), re.IGNORECASE) is None

    def test_workspace_iaso_connection_not_exist(self, workspace):
        """Does not exist test case for IASO connections."""
        identifier = "iaso-account"
        with pytest.raises(ConnectionDoesNotExist):
            workspace.iaso_connection(identifier=identifier)

    def test_workspace_iaso_connection(self, workspace):
        """Base test case for IASO connections."""
        identifier = "iaso-account"
        env_variable_prefix = stringcase.constcase(identifier)
        url = "https://test.iaso.org/"
        username = "iaso"
        password = "iaso_pwd"

        with mock.patch.dict(
            os.environ,
            {
                f"{env_variable_prefix}": "iaso",
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

    def test_workspace_custom_connection_not_exist(self, workspace):
        """Does not exist test case for custom connections."""
        identifier = "custom-stuff"
        with pytest.raises(ConnectionDoesNotExist):
            workspace.custom_connection(identifier=identifier)

    def test_workspace_custom_connection(self, workspace):
        """Base test case for custom connections."""
        identifier = "my_connection"
        env_variable_prefix = stringcase.constcase(identifier)
        username = "kaggle_username"
        password = "root"

        with mock.patch.dict(
            os.environ,
            {
                f"{env_variable_prefix}": "custom",
                f"{env_variable_prefix}_USERNAME": username,
                f"{env_variable_prefix}_PASSWORD": password,
            },
        ):
            custom_connection = workspace.custom_connection(identifier=identifier)
            assert custom_connection.username == username
            assert custom_connection.password == password
            assert re.search("username", repr(custom_connection), re.IGNORECASE) is None
            assert re.search("password", str(custom_connection), re.IGNORECASE) is None

    def test_connection_by_slug_warning(self, workspace):
        """Ensure that using the slug keyword argument when getting a connection generates a deprecation warning."""
        identifier = "polio-ff3a0d"
        env_variable_prefix = stringcase.constcase(identifier)
        url = "https://test.dhis2.org/"
        username = "dhis2"
        password = "dhis2_pwd"
        with mock.patch.dict(
            os.environ,
            {
                f"{env_variable_prefix}": "dhis2",
                f"{env_variable_prefix}_URL": url,
                f"{env_variable_prefix}_USERNAME": username,
                f"{env_variable_prefix}_PASSWORD": password,
            },
        ):
            assert workspace.dhis2_connection(identifier).url == url
            with pytest.warns(DeprecationWarning):
                assert workspace.dhis2_connection(slug=identifier).url == url
            assert workspace.dhis2_connection(identifier=identifier).url == url

    def test_connection_various_case(self, workspace):
        """Ensure that identifiers used when getting connections are case-insensitive."""
        env_variable_prefix = stringcase.constcase("polio-123")
        url = "https://test.dhis2.org/"
        username = "dhis2"
        password = "dhis2_pwd"
        with mock.patch.dict(
            os.environ,
            {
                f"{env_variable_prefix}": "dhis2",
                f"{env_variable_prefix}_URL": url,
                f"{env_variable_prefix}_USERNAME": username,
                f"{env_variable_prefix}_PASSWORD": password,
            },
        ):
            assert workspace.dhis2_connection("polio-123").url == url
            assert workspace.dhis2_connection("Polio-123").url == url
            assert workspace.dhis2_connection("POLIO-123").url == url


class TestConnectedWorkspace:
    """Test class for workspace that rely the graphl API."""

    @pytest.fixture(autouse=True)
    def setup_method(self, monkeypatch):
        """Basics setup for the TestConnectedWorkspace."""
        # Mock the class variable
        monkeypatch.setenv("HEXA_SERVER_URL", "http://app.openhexa.test")
        monkeypatch.setenv("HEXA_WORKSPACE", "workspace")

    def test_workspace_files_path(self, monkeypatch, workspace):
        """Basic checks for the Workspace.files_path() method."""
        assert workspace.files_path == "/home/hexa/workspace"

        monkeypatch.setenv("WORKSPACE_FILES_PATH", "/Users/John/openhexa/project-1/workspace")
        assert workspace.files_path == "/Users/John/openhexa/project-1/workspace"

    def test_workspace_tmp_path(self, monkeypatch, workspace):
        """Basic checks for the Workspace.tmp_path() method."""
        assert workspace.tmp_path == "/home/hexa/tmp"

        mock_tmp_path = mkdtemp()
        monkeypatch.setenv("WORKSPACE_TMP_PATH", mock_tmp_path)
        assert workspace.tmp_path == mock_tmp_path

    def test_workspace_get_connection_not_exist(self, workspace):
        """Test get connection not found."""
        data = None

        with mock.patch(
            "openhexa.sdk.workspaces.current_workspace.OpenHexaClient.get_connection",
            return_value=data,
        ):
            with pytest.raises(ValueError):
                workspace.get_connection("random")

    def test_workspace_get_connection_case_insensitive(self, workspace):
        """Test get connection."""
        data = {
            "__typename": "CustomConnection",
            "type": "CUSTOM",
            "fields": [{"code": "field_1", "value": "field_1_value"}],
        }
        mocked_data = GetConnectionConnectionBySlug(**data)
        with mock.patch(
            "openhexa.sdk.workspaces.current_workspace.OpenHexaClient.get_connection",
            return_value=mocked_data,
        ):
            connection = workspace.get_connection("RaNDom")
            assert isinstance(connection, CustomConnection)

    def test_workspace_get_connection(self, workspace):
        """Test get connection."""
        data = {
            "__typename": "S3Connection",
            "type": "S3",
            "fields": [
                {"code": "bucket_name", "value": "bucket_name"},
                {"code": "access_key_id", "value": "access_key_id"},
                {"code": "access_key_secret", "value": "secret_access_key"},
            ],
        }
        mocked_data = GetConnectionConnectionBySlug(**data)
        with mock.patch(
            "openhexa.sdk.workspaces.current_workspace.OpenHexaClient.get_connection",
            return_value=mocked_data,
        ):
            connection = workspace.get_connection("s3-connection")
            assert isinstance(connection, S3Connection)

    def test_workspace_dhis2_connection_not_exist(self, workspace):
        """Does not exist test case for DHIS2 connections."""
        identifier = "dhis2-play"
        with mock.patch.object(workspace, "get_connection", side_effect=ValueError()):
            with pytest.raises(ConnectionDoesNotExist):
                workspace.dhis2_connection(identifier=identifier)

    def test_workspace_dhis2_connection(self, workspace):
        """Base test case for DHIS2 connections."""
        identifier = "dhis2-play"
        url = "https://test.dhis2.org/"
        username = "dhis2"
        password = "dhis2_pwd"

        data = DHIS2Connection(url, username, password)

        with mock.patch.object(workspace, "get_connection", return_value=data):
            dhis2_connection = workspace.dhis2_connection(identifier=identifier)

            assert dhis2_connection.url == url
            assert dhis2_connection.username == username
            assert dhis2_connection.password == password
            assert re.search("password", repr(dhis2_connection), re.IGNORECASE) is None
            assert re.search("password", str(dhis2_connection), re.IGNORECASE) is None

    def test_workspace_postgres_connection_not_exist(self, workspace):
        """Does not exist test case for Postgres connections."""
        identifier = "pg_data_play"

        with mock.patch.object(workspace, "get_connection", side_effect=ValueError()):
            with pytest.raises(ConnectionDoesNotExist):
                workspace.postgresql_connection(identifier=identifier)

    def test_workspace_postgresql_connection(self, workspace):
        """Base test case for PostgreSQL connections."""
        identifier = "polio-ff3a0d"

        host = "https://172.17.0.1"
        port = 5432
        username = "dhis2"
        password = "dhis2_pwd"
        database_name = "polio"
        url = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"

        data = PostgreSQLConnection(host, port, username, password, database_name)
        with mock.patch.object(workspace, "get_connection", return_value=data):
            postgres_connection = workspace.postgresql_connection(identifier=identifier)
            assert postgres_connection.username == username
            assert postgres_connection.password == password
            assert postgres_connection.host == host
            assert postgres_connection.port == port
            assert postgres_connection.database_name == database_name
            assert postgres_connection.url == url
            assert re.search("password", repr(postgres_connection), re.IGNORECASE) is None
            assert re.search("password", str(postgres_connection), re.IGNORECASE) is None

    def test_workspace_S3_connection_not_exist(self, workspace):
        """Does not exist test case for S3 connections."""
        identifier = "polio-ff3a0d"
        with mock.patch.object(workspace, "get_connection", side_effect=ValueError()):
            with pytest.raises(ConnectionDoesNotExist):
                workspace.s3_connection(identifier=identifier)

    def test_workspace_s3_connection(monkeypatch, workspace):
        """Base test case for S3 connections."""
        identifier = "polio-ff3a0d"

        secret_access_key = "HqQBxH0BAI3zF7kANUNlGg"
        access_key_id = "84hVntMaMSYP/RSW9ex04w"
        bucket_name = "test"

        data = S3Connection(access_key_id, secret_access_key, bucket_name)
        with mock.patch.object(workspace, "get_connection", return_value=data):
            s3_connection = workspace.s3_connection(identifier=identifier)

            assert s3_connection.secret_access_key == secret_access_key
            assert s3_connection.access_key_id == access_key_id
            assert s3_connection.bucket_name == bucket_name
            assert re.search("secret_access_key", repr(s3_connection), re.IGNORECASE) is None
            assert re.search("secret_access_key", str(s3_connection), re.IGNORECASE) is None
            assert re.search("access_key_id", repr(s3_connection), re.IGNORECASE) is None
            assert re.search("access_key_id", str(s3_connection), re.IGNORECASE) is None

    def test_workspace_gcs_connection_not_exist(self, workspace):
        """Does not exist test case for GCS connections."""
        identifier = "polio-ff3a0d"
        with mock.patch.object(workspace, "get_connection", side_effect=ValueError()):
            with pytest.raises(ConnectionDoesNotExist):
                workspace.gcs_connection(identifier=identifier)

    def test_workspace_gcs_connection(self, workspace):
        """Base test case for GCS connections."""
        identifier = "polio-ff3a0d"

        service_account_key = "HqQBxH0BAI3zF7kANUNlGg"
        bucket_name = "test"

        data = GCSConnection(service_account_key, bucket_name)
        with mock.patch.object(workspace, "get_connection", return_value=data):
            s3_connection = workspace.gcs_connection(identifier=identifier)
            assert s3_connection.service_account_key == service_account_key
            assert s3_connection.bucket_name == bucket_name
            assert re.search("service_account_key", repr(s3_connection), re.IGNORECASE) is None
            assert re.search("service_account_key", str(s3_connection), re.IGNORECASE) is None

    def test_workspace_iaso_connection_not_exist(self, workspace):
        """Does not exist test case for IASO connections."""
        identifier = "iaso-account"
        with mock.patch.object(workspace, "get_connection", side_effect=ValueError()):
            with pytest.raises(ConnectionDoesNotExist):
                workspace.iaso_connection(identifier=identifier)

    def test_workspace_iaso_connection(self, workspace):
        """Base test case for IASO connections."""
        identifier = "iaso-account"

        url = "https://test.iaso.org/"
        username = "iaso"
        password = "iaso_pwd"

        data = IASOConnection(url, username, password)
        with mock.patch.object(workspace, "get_connection", return_value=data):
            iaso_connection = workspace.iaso_connection(identifier=identifier)
            assert iaso_connection.url == url
            assert iaso_connection.username == username
            assert iaso_connection.password == password
            assert re.search("password", repr(iaso_connection), re.IGNORECASE) is None
            assert re.search("password", str(iaso_connection), re.IGNORECASE) is None

    def test_workspace_custom_connection_not_exist(self, workspace):
        """Does not exist test case for custom connections."""
        identifier = "custom-stuff"
        with mock.patch.object(workspace, "get_connection", side_effect=ValueError()):
            with pytest.raises(ConnectionDoesNotExist):
                workspace.custom_connection(identifier=identifier)

    def test_workspace_custom_connection(self, workspace):
        """Base test case for custom connections."""
        identifier = "my_connection"

        username = "kaggle_username"
        password = "root"

        dataclass = make_dataclass(
            stringcase.pascalcase(identifier),
            ["username", "password"],
            bases=(CustomConnection,),
            repr=False,
        )
        with mock.patch.object(workspace, "get_connection", return_value=dataclass(username, password)):
            custom_connection = workspace.custom_connection(identifier=identifier)
            assert custom_connection.username == username
            assert custom_connection.password == password
            assert re.search("username", repr(custom_connection), re.IGNORECASE) is None
            assert re.search("password", str(custom_connection), re.IGNORECASE) is None

    def test_connection_by_slug_warning(self, workspace):
        """Ensure that using the slug keyword argument when getting a connection generates a deprecation warning."""
        identifier = "polio-ff3a0d"

        url = "https://test.dhis2.org/"
        username = "dhis2"
        password = "dhis2_pwd"

        data = DHIS2Connection(url, username, password)
        with mock.patch.object(workspace, "get_connection", return_value=data):
            assert workspace.dhis2_connection(identifier).url == url
            with pytest.warns(DeprecationWarning):
                assert workspace.dhis2_connection(slug=identifier).url == url
            assert workspace.dhis2_connection(identifier=identifier).url == url

    def test_connection_various_case(self, workspace):
        """Ensure that identifiers used when getting connections are case-insensitive."""
        url = "https://test.dhis2.org/"
        username = "dhis2"
        password = "dhis2_pwd"
        data = DHIS2Connection(url, username, password)
        with mock.patch.object(workspace, "get_connection", return_value=data):
            assert workspace.dhis2_connection("polio-123").url == url
            assert workspace.dhis2_connection("Polio-123").url == url
            assert workspace.dhis2_connection("POLIO-123").url == url

    def test_workspace_configuration(self, workspace):
        mock_config = {
            "api_url": "https://api.example.com",
            "debug_mode": "true",
            "database_config": {"host": "localhost", "port": 5432},
        }

        mock_workspace_data = mock.Mock()
        mock_workspace_data.configuration = mock_config

        with mock.patch("openhexa.sdk.workspaces.current_workspace.OpenHexaClient") as mock_client:
            mock_client.return_value.workspace.return_value = mock_workspace_data
            assert workspace.configuration == mock_config

    def test_workspace_configuration_setter(self, workspace):
        """Test setting workspace configuration through property setter."""
        new_config = {
            "api_url": "https://new-api.example.com",
            "environment": "development",
            "features": {"feature1": True, "feature2": False},
        }

        mock_result = mock.Mock()
        mock_result.success = True

        with mock.patch("openhexa.sdk.workspaces.current_workspace.OpenHexaClient") as mock_client:
            mock_client.return_value.update_workspace.return_value = mock_result

            workspace.configuration = new_config

            mock_client.return_value.update_workspace.assert_called_once()
            call_args = mock_client.return_value.update_workspace.call_args[1]["input"]
            assert call_args.slug == workspace.slug
            assert call_args.configuration == new_config
