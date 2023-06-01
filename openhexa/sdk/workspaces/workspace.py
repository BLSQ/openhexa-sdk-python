import os
from dataclasses import make_dataclass

import stringcase

from openhexa.sdk.utils import Environments, get_environment

from .connection import (
    DHIS2Connection,
    GCSConnection,
    PostgreSQLConnection,
    S3Connection,
)


class WorkspaceConfigError(Exception):
    pass


class ConnectionDoesNotExist(Exception):
    pass


class CurrentWorkspace:
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
        env = get_environment()
        if env == Environments.LOCAL:
            if "WORKSPACE_FILES_PATH" not in os.environ:
                raise WorkspaceConfigError(
                    "No filesystem has been configured. Did you forget to provide a files.path"
                    "key in your workspace.yaml file?"
                )
            return os.environ["WORKSPACE_FILES_PATH"]
        else:
            return "/home/hexa/workspace"

    def dhis2_connection(self, slug: str) -> DHIS2Connection:
        try:
            env_variable_prefix = stringcase.constcase(slug.lower())
            url = os.environ[f"{env_variable_prefix}_URL"]
            username = os.environ[f"{env_variable_prefix}_USERNAME"]
            password = os.environ[f"{env_variable_prefix}_PASSWORD"]
        except KeyError:
            raise ConnectionDoesNotExist(f'No DHIS2 connection for "{slug}"')

        return DHIS2Connection(url=url, username=username, password=password)

    def postgresql_connection(self, slug: str) -> PostgreSQLConnection:
        try:
            env_variable_prefix = stringcase.constcase(slug.lower())
            host = os.environ[f"{env_variable_prefix}_HOST"]
            port = int(os.environ[f"{env_variable_prefix}_PORT"])
            username = os.environ[f"{env_variable_prefix}_USERNAME"]
            password = os.environ[f"{env_variable_prefix}_PASSWORD"]
            dbname = os.environ[f"{env_variable_prefix}_DB_NAME"]
        except KeyError:
            raise ConnectionDoesNotExist(f'No PostgreSQL connection for "{slug}"')

        return PostgreSQLConnection(
            host=host,
            port=port,
            username=username,
            password=password,
            database_name=dbname,
        )

    def s3_connection(self, slug: str) -> S3Connection:
        try:
            env_variable_prefix = stringcase.constcase(slug.lower())
            secret_access_key = os.environ[f"{env_variable_prefix}_SECRET_ACCESS_KEY"]
            access_key_id = os.environ[f"{env_variable_prefix}_ACCESS_KEY_ID"]
            bucket_name = os.environ[f"{env_variable_prefix}_BUCKET_NAME"]
        except KeyError:
            raise ConnectionDoesNotExist(f'No S3 connection for "{slug}"')

        return S3Connection(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            bucket_name=bucket_name,
        )

    def gcs_connection(self, slug: str) -> GCSConnection:
        try:
            env_variable_prefix = stringcase.constcase(slug.lower())
            service_account_key = os.environ[
                f"{env_variable_prefix}_SERVICE_ACCOUNT_KEY"
            ]
            bucket_name = os.environ[f"{env_variable_prefix}_BUCKET_NAME"]
        except KeyError:
            raise ConnectionDoesNotExist(f'No GCS connection for "{slug}"')

        return GCSConnection(
            service_account_key=service_account_key,
            bucket_name=bucket_name,
        )

    def custom_connection(self, slug: str):
        slug = slug.lower()
        env_variable_prefix = stringcase.constcase(slug)
        fields = {}
        for key, value in os.environ.items():
            if key.startswith(env_variable_prefix):
                field_key = key[len(f"{env_variable_prefix}_") :].lower()
                fields[field_key] = value
        CustomConnection = make_dataclass(slug, fields.keys())
        return CustomConnection(**fields)


workspace = CurrentWorkspace()
