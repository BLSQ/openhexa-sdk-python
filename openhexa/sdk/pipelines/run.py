import datetime
import os
import typing
from pathlib import Path

from openhexa.sdk.utils import Environments, get_environment, graphql
from openhexa.sdk.workspaces import workspace


class CurrentRun:
    @property
    def _connected(self):
        return "HEXA_SERVER_URL" in os.environ

    @property
    def tmp_path(self):
        return Path("~/tmp/")

    def add_file_output(self, path: str):
        stripped_path = path.replace(workspace.files_path, "")
        name = stripped_path.strip("/")
        if self._connected:
            graphql(
                """
                mutation addPipelineOutput ($input: AddPipelineOutputInput!) {
                    addPipelineOutput(input: $input) { success errors }
                }""",
                {
                    "input": {
                        "uri": f"gs://{os.environ['WORKSPACE_BUCKET_NAME']}{stripped_path}",
                        "type": "file",
                        "name": name,
                    }
                },
            )
        else:
            print(f"Sending output with path {stripped_path}")

    def add_database_output(self, table_name: str):
        if self._connected:
            graphql(
                """
                mutation addPipelineOutput ($input: AddPipelineOutputInput!) {
                    addPipelineOutput(input: $input) { success errors }
                }""",
                {
                    "input": {
                        "uri": f"postgresql://{workspace.database_host}/{workspace.database_name}/{table_name}",
                        "type": "db",
                        "name": table_name,
                    }
                },
            )
        else:
            print(f"Sending output with table_name {table_name}")

    def log_debug(self, message: str):
        self._log_message("DEBUG", message)

    def log_info(self, message: str):
        self._log_message("INFO", message)

    def log_warning(self, message: str):
        self._log_message("WARNING", message)

    def log_error(self, message: str):
        self._log_message("ERROR", message)

    def log_critical(self, message: str):
        self._log_message("CRITICAL", message)

    def _log_message(
        self,
        priority: typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        message: str,
    ):
        valid_priorities = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if priority not in valid_priorities:
            raise ValueError(f"priority must be one of {', '.join(valid_priorities)}")

        if self._connected:
            graphql(
                """
                mutation logPipelineMessage ($input: LogPipelineMessageInput!) {
                    logPipelineMessage(input: $input) { success errors }
                }""",
                {"input": {"priority": priority, "message": str(message)}},
            )
        else:
            now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).isoformat()
            print(now, priority, message)


if get_environment() == Environments.CLOUD_JUPYTER:
    current_run = None
else:
    current_run = CurrentRun()
