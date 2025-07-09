"""Pipeline run module."""

import datetime
import errno
import os

from openhexa.sdk.pipelines.log_level import LogLevel
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

    def id(self):
        """Exposes pipeline run id."""
        if "HEXA_RUN_ID" in os.environ:
            return os.environ["HEXA_RUN_ID"]
        else:
            raise RuntimeError("Current run ID is not set. Make sure you are running this in a pipeline context.")

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
        """Log a message with the DEBUG level."""
        self._log_message(LogLevel.DEBUG, message)

    def log_info(self, message: str):
        """Log a message with the INFO level."""
        self._log_message(LogLevel.INFO, message)

    def log_warning(self, message: str):
        """Log a message with the WARNING level."""
        self._log_message(LogLevel.WARNING, message)

    def log_error(self, message: str):
        """Log a message with the ERROR level."""
        self._log_message(LogLevel.ERROR, message)

    def log_critical(self, message: str):
        """Log a message with the CRITICAL level."""
        self._log_message(LogLevel.CRITICAL, message)

    def _log_message(
        self,
        log_level: LogLevel,
        message: str,
    ):
        from openhexa.cli.settings import settings

        if log_level < settings.log_level:  # Ignore messages with lower log level than the settings
            return
        if self._connected:
            graphql(
                """
                mutation logPipelineMessage ($input: LogPipelineMessageInput!) {
                    logPipelineMessage(input: $input) { success errors }
                }""",
                {"input": {"priority": log_level.name, "message": str(message)}},
            )
        else:
            now = datetime.datetime.now(tz=datetime.UTC).replace(microsecond=0).isoformat()
            print(now, log_level.name, message)


if get_environment() == Environment.CLOUD_JUPYTER:
    current_run = None
else:
    current_run = CurrentRun()
