import os
from dataclasses import make_dataclass
from warnings import warn

import stringcase

from ..datasets import Dataset
from ..utils import graphql
from .connection import (
    DHIS2Connection,
    GCSConnection,
    IASOConnection,
    PostgreSQLConnection,
    S3Connection,
)


class WorkspaceConfigError(Exception):
    pass


class ConnectionDoesNotExist(Exception):
    pass


class CurrentWorkspace:
    @property
    def _token(self):
        try:
            return os.environ["HEXA_TOKEN"]
        except KeyError:
            raise WorkspaceConfigError("Workspace's token is not available in this environment.")

    @property
    def slug(self):
        try:
            return os.environ["HEXA_WORKSPACE"]
        except KeyError:
            raise WorkspaceConfigError("Workspace's slug is not available in this environment.")

    @property
    def database_host(self):
        try:
            return os.environ["WORKSPACE_DATABASE_HOST"]
        except KeyError:
            raise WorkspaceConfigError(
                "No database has been configured. Did you forget to provide a database entry"
                " in your workspace.yaml file?"
            )

    @property
    def database_username(self):
        try:
            return os.environ["WORKSPACE_DATABASE_USERNAME"]
        except KeyError:
            raise WorkspaceConfigError(
                "No database has been configured. Did you forget to provide a database entry"
                " in your workspace.yaml file?"
            )

    @property
    def database_password(self):
        try:
            return os.environ.get("WORKSPACE_DATABASE_PASSWORD")
        except KeyError:
            raise WorkspaceConfigError(
                "No database has been configured. Did you forget to provide a database entry"
                " in your workspace.yaml file?"
            )

    @property
    def database_name(self):
        try:
            return os.environ["WORKSPACE_DATABASE_DB_NAME"]
        except KeyError:
            raise WorkspaceConfigError(
                "No database has been configured. Did you forget to provide a database entry"
                " in your workspace.yaml file?"
            )

    @property
    def database_port(self):
        try:
            return int(os.environ["WORKSPACE_DATABASE_PORT"])
        except KeyError:
            raise WorkspaceConfigError(
                "No database has been configured. Did you forget to provide a database entry"
                " in your workspace.yaml file?"
            )

    @property
    def database_url(self):
        return (
            f"postgresql://{self.database_username}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    @property
    def files_path(self) -> str:
        """Return the base path to the filesystem, without trailing slash"""

        # FIXME: This is a hack to make the SDK work in the context of the `python pipeline.py` command.
        # We can remove this once we deprecate this way of running pipelines
        return os.environ["WORKSPACE_FILES_PATH"] if "WORKSPACE_FILES_PATH" in os.environ else "/home/hexa/workspace"

    @property
    def tmp_path(self) -> str:
        """Return the base path to the tmp directory, without trailing slash"""

        # FIXME: This is a hack to make the SDK work in the context of the `python pipeline.py` command.
        # We can remove this once we deprecate this way of running pipelines
        return os.environ["WORKSPACE_TMP_PATH"] if "WORKSPACE_TMP_PATH" in os.environ else "/home/hexa/tmp"

    def dhis2_connection(self, identifier: str = None, slug: str = None) -> DHIS2Connection:
        identifier = identifier or slug
        if slug is not None:
            warn("'slug' is deprecated. Use 'identifier' instead.", DeprecationWarning, stacklevel=2)
        try:
            env_variable_prefix = stringcase.constcase(identifier.lower())
            url = os.environ[f"{env_variable_prefix}_URL"]
            username = os.environ[f"{env_variable_prefix}_USERNAME"]
            password = os.environ[f"{env_variable_prefix}_PASSWORD"]
        except KeyError:
            raise ConnectionDoesNotExist(f'No DHIS2 connection for "{identifier}"')

        return DHIS2Connection(url=url, username=username, password=password)

    def postgresql_connection(self, identifier: str = None, slug: str = None) -> PostgreSQLConnection:
        identifier = identifier or slug
        if slug is not None:
            warn("'slug' is deprecated. Use 'identifier' instead.", DeprecationWarning, stacklevel=2)
        try:
            env_variable_prefix = stringcase.constcase(identifier.lower())
            host = os.environ[f"{env_variable_prefix}_HOST"]
            port = int(os.environ[f"{env_variable_prefix}_PORT"])
            username = os.environ[f"{env_variable_prefix}_USERNAME"]
            password = os.environ[f"{env_variable_prefix}_PASSWORD"]
            dbname = os.environ[f"{env_variable_prefix}_DB_NAME"]
        except KeyError:
            raise ConnectionDoesNotExist(f'No PostgreSQL connection for "{identifier}"')

        return PostgreSQLConnection(
            host=host,
            port=port,
            username=username,
            password=password,
            database_name=dbname,
        )

    def s3_connection(self, identifier: str = None, slug: str = None) -> S3Connection:
        identifier = identifier or slug
        if slug is not None:
            warn("'slug' is deprecated. Use 'identifier' instead.", DeprecationWarning, stacklevel=2)
        try:
            env_variable_prefix = stringcase.constcase(identifier.lower())
            secret_access_key = os.environ[f"{env_variable_prefix}_SECRET_ACCESS_KEY"]
            access_key_id = os.environ[f"{env_variable_prefix}_ACCESS_KEY_ID"]
            bucket_name = os.environ[f"{env_variable_prefix}_BUCKET_NAME"]
        except KeyError:
            raise ConnectionDoesNotExist(f'No S3 connection for "{identifier}"')

        return S3Connection(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            bucket_name=bucket_name,
        )

    def gcs_connection(self, identifier: str = None, slug: str = None) -> GCSConnection:
        identifier = identifier or slug
        if slug is not None:
            warn("'slug' is deprecated. Use 'identifier' instead.", DeprecationWarning, stacklevel=2)
        try:
            env_variable_prefix = stringcase.constcase(identifier.lower())
            service_account_key = os.environ[f"{env_variable_prefix}_SERVICE_ACCOUNT_KEY"]
            bucket_name = os.environ[f"{env_variable_prefix}_BUCKET_NAME"]
        except KeyError:
            raise ConnectionDoesNotExist(f'No GCS connection for "{identifier}"')

        return GCSConnection(
            service_account_key=service_account_key,
            bucket_name=bucket_name,
        )

    def iaso_connection(self, identifier: str = None, slug: str = None) -> IASOConnection:
        identifier = identifier or slug
        if slug is not None:
            warn("'slug' is deprecated. Use 'identifier' instead.", DeprecationWarning, stacklevel=2)
        try:
            env_variable_prefix = stringcase.constcase(identifier.lower())
            url = os.environ[f"{env_variable_prefix}_URL"]
            username = os.environ[f"{env_variable_prefix}_USERNAME"]
            password = os.environ[f"{env_variable_prefix}_PASSWORD"]
        except KeyError:
            raise ConnectionDoesNotExist(f'No IASO connection for "{identifier}"')

        return IASOConnection(url=url, username=username, password=password)

    def custom_connection(self, identifier: str = None, slug: str = None):
        identifier = identifier or slug
        if slug is not None:
            warn("'slug' is deprecated. Use 'identifier' instead.", DeprecationWarning, stacklevel=2)
        identifier = identifier.lower()
        env_variable_prefix = stringcase.constcase(identifier)
        fields = {}
        for key, value in os.environ.items():
            if key.startswith(env_variable_prefix):
                field_key = key[len(f"{env_variable_prefix}_") :].lower()
                fields[field_key] = value

        dataclass = make_dataclass(identifier, fields.keys())

        class CustomConnection(dataclass):
            def __repr__(self):
                return f"CustomConnection(name='{identifier}')"

        return CustomConnection(**fields)

    def create_dataset(self, identifier: str, name: str, description: str):
        raise NotImplementedError("create_dataset is not implemented yet.")

    def get_dataset(self, identifier: str):
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


# Once we deprecate the `python pipeline.py` command, we can enhance this to only load the workspace
# if we're in a pipeline/jupyter context
workspace = CurrentWorkspace()
