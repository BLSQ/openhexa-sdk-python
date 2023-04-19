import os
import sys
import typing
from pathlib import Path

import yaml


class WorkspaceDataHelper:
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
            return self._dev_config(
                lambda c: c["development"]["workspace_database"]["host"]
            )

    @property
    def database_username(self):
        if self.connected:
            return os.environ["WORKSPACE_DATABASE_USERNAME"]
        else:
            return self._dev_config(
                lambda c: c["development"]["workspace_database"]["username"]
            )

    @property
    def database_password(self):
        if self.connected:
            return os.environ["WORKSPACE_DATABASE_PASSWORD"]
        else:
            return self._dev_config(
                lambda c: c["development"]["workspace_database"]["password"]
            )

    @property
    def database_name(self):
        if self.connected:
            return os.environ["WORKSPACE_DATABASE_DB_NAME"]
        else:
            return self._dev_config(
                lambda c: c["development"]["workspace_database"]["db_name"]
            )

    @property
    def database_port(self):
        if self.connected:
            return os.environ["WORKSPACE_DATABASE_PORT"]
        else:
            return self._dev_config(
                lambda c: c["development"]["workspace_database"]["port"]
            )

    @property
    def database_url(self):
        if self.connected:
            return os.environ["WORKSPACE_DATABASE_URL"]
        else:
            return f"postgresql://{self.database_username}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

    def files_path(self, path: str) -> str:
        if self.connected:
            return f"/home/hexa/{path}"
        elif len(sys.argv) > 0:
            base_path = Path(sys.argv[0]).parent.resolve()
            local_workspace_path = base_path / Path("workspace")
            if local_workspace_path.exists():
                full_path = local_workspace_path / Path(path)
                return str(full_path.resolve())
            else:
                exception_message = (
                    'Your pipeline directory does not contain a "workspace directory". '
                    'Create a "workspace" directory in the same directory in order to to work '
                    "with local files."
                )
                raise IOError(exception_message)

    def _dev_config(self, accessor: typing.Callable):
        if self.dev_config is None:
            raise ValueError("No dev config")
        try:
            return accessor(self.dev_config)
        except KeyError:
            raise ValueError("Could not find config")


workspace_data = WorkspaceDataHelper()

__all__ = ["workspace_data"]
