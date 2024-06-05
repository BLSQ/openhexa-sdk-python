"""Workspace-related classes and functions.

See https://github.com/BLSQ/openhexa/wiki/User-manual#about-workspaces for more information.
"""

import os
import typing
from dataclasses import make_dataclass
from warnings import warn

import stringcase

from ..datasets import Dataset
from ..utils import graphql
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
            raise WorkspaceConfigError(
                "The workspace token is not available in this environment."
            )

    @property
    def slug(self) -> str:
        """The unique slug of the workspace.

        Slugs are used to identify the workspace.
        """
        try:
            return os.environ["HEXA_WORKSPACE"]
        except KeyError:
            raise WorkspaceConfigError(
                "The workspace slug is not available in this environment."
            )

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
        # We can remove this once we deprecate this way of running pipelines
        return (
            os.environ["WORKSPACE_FILES_PATH"]
            if "WORKSPACE_FILES_PATH" in os.environ
            else "/home/hexa/workspace"
        )

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
        return (
            os.environ["WORKSPACE_TMP_PATH"]
            if "WORKSPACE_TMP_PATH" in os.environ
            else "/home/hexa/tmp"
        )

    def get_connection(self, identifier: str) -> typing.Union[
        DHIS2Connection,
        PostgreSQLConnection,
        IASOConnection,
        S3Connection,
        S3Connection,
        CustomConnection,
        None,
    ]:
        """Get a connection by its identifier. This method

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
        response = graphql(
            """
            query getConnection($slug: String!) {
                connectionBySlug(slug: $slug) {
                    type
                    fields {
                        code
                        value
                    }
                }
            }
        """,
            {"slug": identifier},
        )

        data = response["connectionBySlug"]
        if data is None:
            raise ValueError(f"Connection {identifier} does not exist.")

        fields = {}
        for d in data["fields"]:
            fields[d.get("code")] = d.get("value")

        connection_type = data["type"].upper()
        if connection_type in ConnectionClasses.keys():
            if connection_type == "S3":
                secret_access_key = fields.pop("access_key_secret")
                return S3Connection(secret_access_key=secret_access_key, **fields)

            if connection_type == "POSTGRESQL":
                db_name = fields.pop("db_name")
                port = int(fields.pop("port"))
                return PostgreSQLConnection(database_name=db_name, port=port, **fields)

            if connection_type == "CUSTOM":
                dataclass = make_dataclass(
                    stringcase.pascalcase(identifier),
                    fields.keys(),
                    bases=(CustomConnection,),
                    repr=False,
                )
                return dataclass(**fields)

            return ConnectionClasses[connection_type](**fields)

    def dhis2_connection(
        self, identifier: str = None, slug: str = None
    ) -> DHIS2Connection:
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
            if self._connected:
                connection = self.get_connection(identifier)
                if not isinstance(connection, DHIS2Connection):
                    raise ValueError
            else:
                env_variable_prefix = stringcase.constcase(identifier.lower())
                url = os.environ[f"{env_variable_prefix}_URL"]
                username = os.environ[f"{env_variable_prefix}_USERNAME"]
                password = os.environ[f"{env_variable_prefix}_PASSWORD"]
                connection = DHIS2Connection(
                    url=url, username=username, password=password
                )
            return connection
        except (ValueError, KeyError):
            raise ConnectionDoesNotExist(f'No DHIS2 connection for "{identifier}"')

    def postgresql_connection(
        self, identifier: str = None, slug: str = None
    ) -> PostgreSQLConnection:
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
            if self._connected:
                connection = self.get_connection(identifier)
                if not isinstance(connection, PostgreSQLConnection):
                    raise ValueError
            else:
                env_variable_prefix = stringcase.constcase(identifier.lower())
                host = os.environ[f"{env_variable_prefix}_HOST"]
                port = int(os.environ[f"{env_variable_prefix}_PORT"])
                username = os.environ[f"{env_variable_prefix}_USERNAME"]
                password = os.environ[f"{env_variable_prefix}_PASSWORD"]
                dbname = os.environ[f"{env_variable_prefix}_DB_NAME"]

                connection = PostgreSQLConnection(
                    host=host,
                    port=port,
                    username=username,
                    password=password,
                    database_name=dbname,
                )

            return connection
        except (ValueError, KeyError) as e:
            print(e, flush=True)
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
            if self._connected:
                connection = self.get_connection(identifier)
                if not isinstance(connection, S3Connection):
                    raise ValueError
            else:
                env_variable_prefix = stringcase.constcase(identifier.lower())
                secret_access_key = os.environ[
                    f"{env_variable_prefix}_SECRET_ACCESS_KEY"
                ]
                access_key_id = os.environ[f"{env_variable_prefix}_ACCESS_KEY_ID"]
                bucket_name = os.environ[f"{env_variable_prefix}_BUCKET_NAME"]

                connection = S3Connection(
                    access_key_id=access_key_id,
                    secret_access_key=secret_access_key,
                    bucket_name=bucket_name,
                )

            return connection
        except (ValueError, KeyError):
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
            if self._connected:
                connection = self.get_connection(identifier)
                if not isinstance(connection, GCSConnection):
                    raise ValueError
            else:
                env_variable_prefix = stringcase.constcase(identifier.lower())
                service_account_key = os.environ[
                    f"{env_variable_prefix}_SERVICE_ACCOUNT_KEY"
                ]
                bucket_name = os.environ[f"{env_variable_prefix}_BUCKET_NAME"]

                connection = GCSConnection(
                    service_account_key=service_account_key,
                    bucket_name=bucket_name,
                )

            return connection
        except (ValueError, KeyError):
            raise ConnectionDoesNotExist(f'No GCS connection for "{identifier}"')

    def iaso_connection(
        self, identifier: str = None, slug: str = None
    ) -> IASOConnection:
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
            if self._connected:
                connection = self.get_connection(identifier)
                if not isinstance(connection, IASOConnection):
                    raise ValueError
            else:
                env_variable_prefix = stringcase.constcase(identifier.lower())
                url = os.environ[f"{env_variable_prefix}_URL"]
                username = os.environ[f"{env_variable_prefix}_USERNAME"]
                password = os.environ[f"{env_variable_prefix}_PASSWORD"]

                connection = IASOConnection(
                    url=url, username=username, password=password
                )

            return connection
        except (ValueError, KeyError):
            raise ConnectionDoesNotExist(f'No IASO connection for "{identifier}"')

    def custom_connection(
        self, identifier: str = None, slug: str = None
    ) -> CustomConnection:
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
            if self._connected:
                connection = self.get_connection(identifier)
                if not isinstance(connection, CustomConnection):
                    raise ValueError
            else:
                env_variable_prefix = stringcase.constcase(identifier.lower())
                fields = {}
                for key, value in os.environ.items():
                    if key.startswith(env_variable_prefix):
                        field_key = key[len(f"{env_variable_prefix}_") :].lower()
                        fields[field_key] = value

                if len(fields) == 0:
                    raise KeyError

                dataclass = make_dataclass(
                    stringcase.pascalcase(identifier),
                    fields.keys(),
                    bases=(CustomConnection,),
                    repr=False,
                )
                connection = dataclass(**fields)

            return connection
        except (ValueError, KeyError):
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

    def get_dataset(self, identifier: str) -> Dataset:
        """Get a dataset by its identifier.

        Parameters
        ----------
        identifier : str
            The identifier of the dataset in the OpenHEXA backend

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
                    workspace {
                        slug
                        name
                    }
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
                    }
                }
            }
        """,
            {"datasetSlug": identifier, "workspaceSlug": self.slug},
        )
        data = response["datasetLinkBySlug"]

        if data is None:
            raise ValueError(f"Dataset {identifier} does not exist.")

        return Dataset(
            id=data["dataset"]["id"],
            slug=data["dataset"]["slug"],
            name=data["dataset"]["name"],
            description=data["dataset"]["description"],
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
            )
            for d in data
        ]

        return datasets
