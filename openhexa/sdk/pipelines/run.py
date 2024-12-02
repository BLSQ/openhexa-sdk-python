"""Pipeline run module."""

import datetime
import errno
import os

from openhexa.sdk.pipelines.priority import Priority
from openhexa.sdk.utils import Environment, get_environment, graphql
from openhexa.sdk.workspaces import workspace


class CurrentRun:
    """Represents the current run of a pipeline.

    CurrentRun instances allow pipeline developers to interact with the OpenHEXA backend, by sending messages and
    adding outputs that will be available through the web interface.
    """

    @property
    def _connected(self):
        return "HEXA_SERVER_URL" in os.environ

    def add_file_output(self, path: str):
        """Record a run output for a file creation operation.

        This output will be visible in the web interface, on the pipeline run page.
        """
        stripped_path = path.replace(workspace.files_path, "")
        name = stripped_path.strip("/")
        if self._connected:
            res = graphql(
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
            if not res["addPipelineOutput"]["success"]:
                if "FILE_NOT_FOUND" in res["addPipelineOutput"]["errors"]:
                    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

                raise Exception(res["addPipelineOutput"]["errors"])
        else:
            print(f"Sending output with path {stripped_path}")

    def add_database_output(self, table_name: str):
        """Record a run output for a database operation.

        This output will be visible in the web interface, on the pipeline run page.
        """
        if self._connected:
            res = graphql(
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
            if not res["addPipelineOutput"]["success"]:
                if "TABLE_NOT_FOUND" in res["addPipelineOutput"]["errors"]:
                    raise Exception(f"{table_name} doesn't exist in workspace {workspace.slug}")
        else:
            print(f"Sending output with table_name {table_name}")

    def log_debug(self, message: str):
        """Log a message with the DEBUG priority."""
        self._log_message(Priority.DEBUG, message)

    def log_info(self, message: str):
        """Log a message with the INFO priority."""
        self._log_message(Priority.INFO, message)

    def log_warning(self, message: str):
        """Log a message with the WARNING priority."""
        self._log_message(Priority.WARNING, message)

    def log_error(self, message: str):
        """Log a message with the ERROR priority."""
        self._log_message(Priority.ERROR, message)

    def log_critical(self, message: str):
        """Log a message with the CRITICAL priority."""
        self._log_message(Priority.CRITICAL, message)

    def _log_message(
        self,
        priority: Priority,
        message: str,
    ):
        from openhexa.cli.settings import settings

        if priority < settings.log_level:  # Ignore messages with lower priority than the log level
            return
        if self._connected:
            graphql(
                """
                mutation logPipelineMessage ($input: LogPipelineMessageInput!) {
                    logPipelineMessage(input: $input) { success errors }
                }""",
                {"input": {"priority": priority.name, "message": str(message)}},
            )
        else:
            now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).isoformat()
            print(now, priority.name, message)


if get_environment() == Environment.CLOUD_JUPYTER:
    current_run = None
else:
    current_run = CurrentRun()
