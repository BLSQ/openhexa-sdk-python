import os

import stringcase

from openhexa.sdk.workspace.connection import DHIS2Connection, PostgreSQLConnection


class ConfigError(Exception):
    pass


class ConnectionDoesNotExist(Exception):
    pass


class InvalidConnection(Exception):
    pass


class CurrentWorkspace:
    @property
    def database_host(self):
        return os.environ["WORKSPACE_DATABASE_HOST"]

    @property
    def database_username(self):
        return os.environ["WORKSPACE_DATABASE_USERNAME"]

    @property
    def database_password(self):
        return os.environ.get("WORKSPACE_DATABASE_PASSWORD")

    @property
    def database_name(self):
        return os.environ["WORKSPACE_DATABASE_DBNAME"]

    @property
    def database_port(self):
        return int(os.environ["WORKSPACE_DATABASE_PORT"])

    @property
    def database_url(self):
        return (
            f"postgresql://{self.database_username}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    @property
    def files_path(self) -> str:
        if "WORKSPACE_FILES_PATH" in os.environ:
            return os.environ["WORKSPACE_FILES_PATH"]
        return "/home/hexa/workspace"

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
            dbname = os.environ[f"{env_variable_prefix}_DBNAME"]
        except KeyError:
            raise ConnectionDoesNotExist(f'No PostgreSQL connection for "{slug}"')

        return PostgreSQLConnection(
            host=host, port=port, username=username, password=password, dbname=dbname
        )


workspace = CurrentWorkspace()
