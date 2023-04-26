import os

import stringcase

from .connection import DHIS2Connection, PostgreSQLConnection


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

        if "WORKSPACE_FILES_PATH" in os.environ:
            return os.environ["WORKSPACE_FILES_PATH"]
        elif "HEXA_SERVER_URL" in os.environ:
            return "/home/hexa/workspace"

        raise WorkspaceConfigError(
            "No filesystem has been configured. Did you forget to provide a files.path"
            "key in your workspace.yaml file?"
        )

    def dhis2_connection(self, slug: str) -> DHIS2Connection:
        try:
            env_variable_prefix = stringcase.constcase(slug)
            url = os.environ[f"{env_variable_prefix}_URL"]
            username = os.environ[f"{env_variable_prefix}_USERNAME"]
            password = os.environ[f"{env_variable_prefix}_PASSWORD"]
        except KeyError:
            raise ConnectionDoesNotExist(f'No DHIS2 connection for "{slug}"')

        return DHIS2Connection(url=url, username=username, password=password)

    def postgresql_connection(self, slug: str) -> PostgreSQLConnection:
        try:
            env_variable_prefix = stringcase.constcase(slug)
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


workspace = CurrentWorkspace()
