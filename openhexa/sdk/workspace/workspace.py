import os
import sys
from functools import reduce
from pathlib import Path

import stringcase
import yaml

from openhexa.sdk.workspace.connection import DHIS2Connection


class ConfigError(Exception):
    pass


class ConnectionDoesNotExist(Exception):
    pass


class InvalidConnection(Exception):
    pass


class Workspace:
    def __init__(self, connected: bool = False):
        self.connected = connected
        if connected:
            self.dev_config = None
        else:
            pipeline_script_path = Path(sys.argv[0]).parent.resolve()
            try:
                with open(pipeline_script_path / Path(".openhexa.yaml")) as config_file:
                    self.dev_config = yaml.safe_load(config_file)
            except FileNotFoundError:
                self.dev_config = None

    @property
    def database_host(self):
        if self.connected:
            return os.environ["WORKSPACE_DATABASE_HOST"]
        else:
            return self._get_dev_config("development.workspace.database.host")

    @property
    def database_username(self):
        if self.connected:
            return os.environ["WORKSPACE_DATABASE_USERNAME"]
        else:
            return self._get_dev_config("development.workspace.database.username")

    @property
    def database_password(self):
        if self.connected:
            return os.environ["WORKSPACE_DATABASE_PASSWORD"]
        else:
            return self._get_dev_config("development.workspace.database.password")

    @property
    def database_name(self):
        if self.connected:
            return os.environ["WORKSPACE_DATABASE_DB_NAME"]
        else:
            return self._get_dev_config("development.workspace.database.db_name")

    @property
    def database_port(self):
        if self.connected:
            return os.environ["WORKSPACE_DATABASE_PORT"]
        else:
            return self._get_dev_config("development.workspace.database.port")

    @property
    def database_url(self):
        if self.connected:
            return os.environ["WORKSPACE_DATABASE_URL"]
        else:
            return f"postgresql://{self.database_username}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

    @property
    def files_path(self) -> str:
        if self.connected:
            return "/home/hexa/"
        elif len(sys.argv) > 0:
            base_path = Path(sys.argv[0]).parent.resolve()
            local_workspace_path = base_path / Path("workspace")
            if local_workspace_path.exists():
                return str(local_workspace_path.resolve())
            else:
                exception_message = (
                    'Your pipeline directory does not contain a "workspace directory". '
                    'Create a "workspace" directory in the same directory in order to to work '
                    "with local files."
                )
                raise IOError(exception_message)

    def dhis2_connection(self, slug: str) -> DHIS2Connection:

        if self.connected:  # Connected? Rely on env variables - for now
            try:
                env_variable_prefix = stringcase.constcase(slug)
                api_url = os.environ[f"{env_variable_prefix}_API_URL"]
                username = os.environ[f"{env_variable_prefix}_USERNAME"]
                password = os.environ[f"{env_variable_prefix}_PASSWORD"]
            except KeyError:
                raise ConnectionDoesNotExist(f'No DHIS2 connection for "{slug}"')

        else:
            try:
                api_url = self._get_dev_config(
                    f"development.workspace.connections.{slug}.api_url"
                )
                username = self._get_dev_config(
                    f"development.workspace.connections.{slug}.username"
                )
                password = self._get_dev_config(
                    f"development.workspace.connections.{slug}.password"
                )
            except ConfigError:
                raise InvalidConnection(
                    f'Could not find a valid connection for slug "{slug}"'
                )

        return DHIS2Connection(api_url=api_url, username=username, password=password)

    def _get_dev_config(self, key: str):
        if self.dev_config is None:
            raise ConfigError("No dev config file found.")
        try:
            return reduce(lambda d, k: d[k], key.split("."), self.dev_config)
        except KeyError:
            raise ConfigError(f"Could not find key {key} in dev config.")


workspace = Workspace()
