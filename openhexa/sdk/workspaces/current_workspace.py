"""Workspace-related classes and functions.

See https://github.com/BLSQ/openhexa/wiki/User-manual#about-workspaces for more information.
"""

import os
from dataclasses import fields, make_dataclass
from warnings import warn

from openhexa.graphql.graphql_client import WorkspaceWorkspaceCountries
from openhexa.graphql.graphql_client.input_types import UpdateWorkspaceInput
from openhexa.utils import stringcase

from ..datasets import Dataset
from ..files import File
from ..utils import OpenHexaClient, graphql
from .connection import (
    ConnectionClasses,
    CustomConnection,
    DHIS2Connection,
    GCSConnection,
    IASOConnection,
    PostgreSQLConnection,
    S3Connection,
)


class WorkspaceConfigError(Exception):
    """Raised whenever the system cannot find an environment variable required to configure the current workspace."""

    pass


class ConnectionDoesNotExist(Exception):
    """Raised whenever an attempt is made to get a connection through an invalid identifier."""

    pass


class CurrentWorkspace:
    """Represents the currently configured OpenHEXA workspace, with its filesystem, database and connections."""

    @property
    def _connected(self):
        return "HEXA_SERVER_URL" in os.environ

    @property
    def _token(self) -> str:
        try:
            return os.environ["HEXA_TOKEN"]
        except KeyError:
            raise WorkspaceConfigError("The workspace token is not available in this environment.")

    @property
    def slug(self) -> str:
        """The unique slug of the workspace.

        Slugs are used to identify the workspace.
        """
        try:
            return os.environ["HEXA_WORKSPACE"]
        except KeyError:
            raise WorkspaceConfigError("The workspace slug is not available in this environment.")

    @property
    def countries(self) -> list[WorkspaceWorkspaceCountries]:
        """The countries of the workspace."""
        try:
            return OpenHexaClient().workspace(slug=self.slug).countries
        except KeyError:
            raise WorkspaceConfigError("The workspace countries are not available in this environment.")

    @property
    def configuration(self) -> dict[str, str | dict] | None:
        """The workspace configuration as a dictionary.

        Returns a dictionary containing workspace configuration as key-value pairs,
        where keys are strings and values can be either strings or JSON objects.
        Returns None if no configuration is available or if not connected to the API.
        """
        if not self._connected:
            return None
        return OpenHexaClient().workspace(slug=self.slug).configuration

    @configuration.setter
    def configuration(self, value: dict[str, str | dict]) -> None:
        """Set the workspace configuration.

        Parameters
        ----------
        value : dict[str, str | dict]
            The configuration dictionary to set for the workspace.
            Keys must be strings and values can be strings or JSON objects.

        Raises
        ------
        WorkspaceConfigError
            If not connected to the API or if the update fails.

        Examples
        --------
        >>> workspace.configuration = {
        ...     "api_url": "https://api.example.com",
        ...     "debug_mode": "true",
        ...     "SNT_CONFIG": "VERY_GOOD_CONFIG"
        ... }
        """
        if not self._connected:
            raise WorkspaceConfigError("Cannot update configuration: not connected to the API.")

        try:
            client = OpenHexaClient()

            input_data = UpdateWorkspaceInput(slug=self.slug, configuration=value)
            result = client.update_workspace(input=input_data)

            if not result.success:
                raise WorkspaceConfigError("Failed to update workspace configuration.")

        except Exception as e:
            if isinstance(e, WorkspaceConfigError):
                raise
            raise WorkspaceConfigError(f"Failed to update workspace configuration: {str(e)}")

    @property
    def database_host(self) -> str:
        """The workspace database host."""
        try:
            return os.environ["WORKSPACE_DATABASE_HOST"]
        except KeyError:
            raise WorkspaceConfigError(
                "No database has been configured. Did you forget to provide a database entry"
                " in your workspace.yaml file?"
            )

    @property
    def database_username(self) -> str:
        """The workspace database username."""
        try:
            return os.environ["WORKSPACE_DATABASE_USERNAME"]
        except KeyError:
            raise WorkspaceConfigError(
                "No database has been configured. Did you forget to provide a database entry"
                " in your workspace.yaml file?"
            )

    @property
    def database_password(self):
        """The workspace database password."""
        try:
            return os.environ.get("WORKSPACE_DATABASE_PASSWORD")
        except KeyError:
            raise WorkspaceConfigError(
                "No database has been configured. Did you forget to provide a database entry"
                " in your workspace.yaml file?"
            )

    @property
    def database_name(self):
        """The workspace database name."""
        try:
            return os.environ["WORKSPACE_DATABASE_DB_NAME"]
        except KeyError:
            raise WorkspaceConfigError(
                "No database has been configured. Did you forget to provide a database entry"
                " in your workspace.yaml file?"
            )

    @property
    def database_port(self):
        """The workspace database port."""
        try:
            return int(os.environ["WORKSPACE_DATABASE_PORT"])
        except KeyError:
            raise WorkspaceConfigError(
                "No database has been configured. Did you forget to provide a database entry"
                " in your workspace.yaml file?"
            )

    @property
    def database_url(self):
        """The workspace database URL.

        The URL follows the official PostgreSQL specification.
        (See https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING for more information)
        """
        return (
            f"postgresql://{self.database_username}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    @property
    def files_path(self) -> str:
        """The base path to the filesystem, without trailing slash.

        Examples
        --------
        >>> f"{workspace.files_path}/some/path"
        /home/hexa/workspace/some/path
        """
        # FIXME: This is a hack to make the SDK work in the context of the `python pipeline.py` command.
        # We can remove this once we deprecate this way of running pipelines and only use /home/hexa/workspace
        return os.environ.get("WORKSPACE_FILES_PATH", "/home/hexa/workspace")

    @property
    def tmp_path(self) -> str:
        """The base path to the tmp directory, without trailing slash.

        Examples
        --------
        >>> f"{workspace.tmp_path}/some/path"
        /home/hexa/tmp/some/path
        """
        # FIXME: This is a hack to make the SDK work in the context of the `python pipeline.py` command.
        # We can remove this once we deprecate this way of running pipelines
        return os.environ["WORKSPACE_TMP_PATH"] if "WORKSPACE_TMP_PATH" in os.environ else "/home/hexa/tmp"

    def _get_local_connection_fields(self, env_variable_prefix: str):
        connection_fields = {}
        connection_type = os.getenv(env_variable_prefix).upper()

        # Get fields for the connection type
        _fields = fields(ConnectionClasses[connection_type])

        if _fields:
            for field in _fields:
                env_var = f"{env_variable_prefix}_{field.name.upper()}"
                connection_fields[field.name] = os.getenv(env_var)
        else:
            #  custom connections
            prefix = f"{env_variable_prefix}_"
            connection_fields = {
                key[len(prefix) :].lower(): val for key, val in os.environ.items() if key.startswith(prefix)
            }

        # need to map the correct name for s3 and postgres connection to ensure compatibility
        # with the one coming from the API
        if connection_type == "S3":
            connection_fields.pop("secret_access_key")
            connection_fields["access_key_secret"] = os.getenv(f"{env_variable_prefix}_ACCESS_KEY_SECRET")
        if connection_type == "POSTGRESQL":
            connection_fields.pop("database_name")
            connection_fields["db_name"] = os.getenv(f"{env_variable_prefix}_DB_NAME")

        return connection_fields

    def get_connection_from_api(self, identifier: str) -> tuple[dict[str, str], str] | None:
        """Get a connection by its identifier from the OpenHEXA API."""
        connection_fields: dict[str, str] = {}
        connection = OpenHexaClient().get_connection(workspace_slug=self.slug, connection_slug=identifier.lower())
        if not connection:
            return None
        for f in connection.fields:
            connection_fields[f.code] = f.value
        connection_type = connection.type.upper()
        return connection_fields, connection_type

    def get_connection_from_env(self, identifier: str) -> tuple[dict[str, str], str] | None:
        """Get a connection by its identifier from the environment variables."""
        env_variable_prefix = stringcase.constcase(identifier.lower())
        try:
            connection_type = os.environ[f"{env_variable_prefix}"].upper()
            connection_fields = self._get_local_connection_fields(env_variable_prefix)
            return connection_fields, connection_type
        except KeyError:
            return None

    def get_connection(
        self, identifier: str
    ) -> (
        DHIS2Connection | PostgreSQLConnection | IASOConnection | S3Connection | GCSConnection | CustomConnection | None
    ):
        """Get a connection by its identifier.

        Parameters
        ----------
        identifier : str
            The identifier of the connection in the OpenHEXA backend

        Returns
        -------
        Connection
            The connection

        Raises
        ------
        ValueError
            If the connection does not exist
        """
        connection = self.get_connection_from_env(identifier)
        if not connection and self._connected:
            connection = self.get_connection_from_api(identifier)

        if not connection:
            raise ValueError(f"Connection {identifier} does not exist.")

        connection_fields, connection_type = connection

        # In connected mode (API call) the secret_access_key field and db_name name are
        # different from the offline ones
        if connection_type == "S3":
            secret_access_key = connection_fields.pop("access_key_secret")
            return S3Connection(secret_access_key=secret_access_key, **connection_fields)

        if connection_type == "POSTGRESQL":
            db_name = connection_fields.pop("db_name")
            port = int(connection_fields.pop("port"))
            return PostgreSQLConnection(
                database_name=db_name,
                port=port,
                **connection_fields,
            )

        if connection_type == "CUSTOM":
            dataclass = make_dataclass(
                stringcase.pascalcase(identifier),
                connection_fields.keys(),
                bases=(CustomConnection,),
                repr=False,
            )
            return dataclass(**connection_fields)

        return ConnectionClasses[connection_type](**connection_fields)

    def dhis2_connection(self, identifier: str = None, slug: str = None) -> DHIS2Connection:
        """Get a DHIS2 connection by its identifier.

        Parameters
        ----------
        identifier : str
            The identifier of the connection in the OpenHEXA backend
        slug : str
            Deprecated, same as identifier
        """
        identifier = identifier or slug
        if slug is not None:
            warn(
                "'slug' is deprecated. Use 'identifier' instead.",
                DeprecationWarning,
                stacklevel=2,
            )

        try:
            connection = self.get_connection(identifier)
            assert isinstance(connection, DHIS2Connection), "Connection is not a DHIS2Connection"
            return connection

        except ValueError:
            raise ConnectionDoesNotExist(f'No DHIS2 connection for "{identifier}"')

    def postgresql_connection(self, identifier: str = None, slug: str = None) -> PostgreSQLConnection:
        """Get a PostgreSQL connection by its identifier.

        Parameters
        ----------
        identifier : str
            The identifier of the connection in the OpenHEXA backend
        slug : str
            Deprecated, same as identifier
        """
        identifier = identifier or slug
        if slug is not None:
            warn(
                "'slug' is deprecated. Use 'identifier' instead.",
                DeprecationWarning,
                stacklevel=2,
            )

        try:
            connection = self.get_connection(identifier)
            assert isinstance(connection, PostgreSQLConnection), "Connection is not a PostgreSQLConnection"

            return connection
        except ValueError:
            raise ConnectionDoesNotExist(f'No PostgreSQL connection for "{identifier}"')

    def s3_connection(self, identifier: str = None, slug: str = None) -> S3Connection:
        """Get an AWS S3 connection by its identifier.

        Parameters
        ----------
        identifier : str
            The identifier of the connection in the OpenHEXA backend
        slug : str
            Deprecated, same as identifier
        """
        identifier = identifier or slug
        if slug is not None:
            warn(
                "'slug' is deprecated. Use 'identifier' instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        try:
            connection = self.get_connection(identifier)
            assert isinstance(connection, S3Connection), "Connection is not a S3Connection"

            return connection
        except ValueError:
            raise ConnectionDoesNotExist(f'No S3 connection for "{identifier}"')

    def gcs_connection(self, identifier: str = None, slug: str = None) -> GCSConnection:
        """Get a Google Cloud Storage connection by its identifier.

        Parameters
        ----------
        identifier : str
            The identifier of the connection in the OpenHEXA backend
        slug : str
            Deprecated, same as identifier
        """
        identifier = identifier or slug
        if slug is not None:
            warn(
                "'slug' is deprecated. Use 'identifier' instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        try:
            connection = self.get_connection(identifier)
            assert isinstance(connection, GCSConnection), "Connection is not a GCSConnection"

            return connection
        except ValueError:
            raise ConnectionDoesNotExist(f'No GCS connection for "{identifier}"')

    def iaso_connection(self, identifier: str = None, slug: str = None) -> IASOConnection:
        """Get a IASO connection by it identifier.

        Parameters
        ----------
        identifier : str
            The identifier of the connection in the OpenHEXA backend
        slug : str
            Deprecated, same as identifier
        """
        identifier = identifier or slug
        if slug is not None:
            warn(
                "'slug' is deprecated. Use 'identifier' instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        try:
            connection = self.get_connection(identifier)
            assert isinstance(connection, IASOConnection), "Connection is not a IASOConnection"

            return connection
        except ValueError:
            raise ConnectionDoesNotExist(f'No IASO connection for "{identifier}"')

    def custom_connection(self, identifier: str = None, slug: str = None) -> CustomConnection:
        """Get a custom connection by its identifier.

        Parameters
        ----------
        identifier : str
            The identifier of the connection in the OpenHEXA backend
        slug : str
            Deprecated, same as identifier
        """
        identifier = identifier or slug
        if slug is not None:
            warn(
                "'slug' is deprecated. Use 'identifier' instead.",
                DeprecationWarning,
                stacklevel=2,
            )

        try:
            connection = self.get_connection(identifier)
            assert isinstance(connection, CustomConnection), "Connection is not a CustomConnection"
            return connection
        except ValueError:
            raise ConnectionDoesNotExist(f'No Custom connection for "{identifier}"')

    def create_dataset(self, name: str, description: str):
        """Create a new dataset.

        Parameters
        ----------
        name: str
            The name of the dataset
        description: str
            The description of the dataset

        Returns
        -------
        Dataset
            The created dataset

        Raises
        ------
        ValueError
            If the dataset could not be created
        """
        rsp = graphql(
            """
        mutation createDataset($input: CreateDatasetInput!) {
            createDataset(input: $input) {
                success
                errors
                dataset {
                    slug
                }
            }
        }
        """,
            {
                "input": {
                    "workspaceSlug": self.slug,
                    "name": name,
                    "description": description,
                }
            },
        )

        if rsp["createDataset"]["success"] is False:
            raise ValueError(rsp["createDataset"]["errors"][0])

        identifier = rsp["createDataset"]["dataset"]["slug"]
        return self.get_dataset(identifier)

    def get_dataset(self, identifier: str, source_workspace_slug: str = None) -> Dataset:
        """Get a dataset by its identifier.

        Parameters
        ----------
        identifier : str
            The identifier of the dataset in the OpenHEXA backend

        source_workspace_slug : str
            The slug of the workspace the dataset belongs to,  defaults to the current workspace slug

        Returns
        -------
        Dataset
            The dataset

        Raises
        ------
        ValueError
            If the dataset does not exist
        """
        response = graphql(
            """
            query getDataset($datasetSlug: String!, $workspaceSlug: String!) {
                datasetLinkBySlug(datasetSlug: $datasetSlug, workspaceSlug: $workspaceSlug) {
                    id
                    dataset {
                        id
                        slug
                        name
                        description
                        latestVersion {
                            id
                            name
                            description
                        }
                        workspace {
                            slug
                        }
                    }
                }
            }
        """,
            {"datasetSlug": identifier, "workspaceSlug": source_workspace_slug or self.slug},
        )
        data = response["datasetLinkBySlug"]

        if data is None:
            raise ValueError(
                f"Dataset {identifier} does not exist on workspace {source_workspace_slug or self.slug}."
                + (
                    " If you try and get a dataset shared from another workspace, please provide the source_workspace_slug parameter."
                    if not source_workspace_slug
                    else ""
                )
            )

        return Dataset(
            id=data["dataset"]["id"],
            slug=data["dataset"]["slug"],
            name=data["dataset"]["name"],
            description=data["dataset"]["description"],
            source_workspace_slug=data["dataset"]["workspace"]["slug"],
        )

    def list_datasets(self) -> list[Dataset]:
        """List datasets in a workspace.

        Returns
        -------
        List of Datasets
        """
        response = graphql(
            """
            query getWorkspaceDatasets($slug: String!) {
                workspace(slug: $slug) {
                    datasets {
                        items {
                            id
                            dataset {
                                id
                                slug
                                name
                                description
                                workspace {
                                    slug
                                }
                            }
                        }

                    }
                }
            }
        """,
            {"slug": self.slug},
        )
        data = response["workspace"]["datasets"]["items"]
        datasets = [
            Dataset(
                id=d["dataset"]["id"],
                slug=d["dataset"]["slug"],
                name=d["dataset"]["name"],
                description=d["dataset"]["description"],
                source_workspace_slug=d["dataset"]["workspace"]["slug"],
            )
            for d in data
        ]

        return datasets

    def get_file(self, path: str) -> File:
        """Get a file by its path.

        Parameters
        ----------
        path : str
            The path of the file in the OpenHEXA backend

        Returns
        -------
        The file

        Raises
        ------
        ValueError
            If the file does not exist
        """
        result = OpenHexaClient().get_file_by_path(path=path, workspace_slug=self.slug)

        return File(
            name=result.name,
            path=f"{self.files_path}/{result.key}",
            size=result.size,
            type=result.type,
        )
