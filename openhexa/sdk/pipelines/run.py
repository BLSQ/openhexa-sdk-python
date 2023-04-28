import datetime
import os
import typing

import requests

from openhexa.sdk.workspaces import workspace


class CurrentRun:
    @property
    def connected(self):
        return "HEXA_SERVER_URL" in os.environ

    def add_file_output(self, path: str):
        stripped_path = path.replace(workspace.files_path, "")
        name = stripped_path.strip("/")
        if self.connected:
            query = """
                    mutation addPipelineOutput ($input: AddPipelineOutputInput!) {
                        addPipelineOutput(input: $input) { success errors }
                    }"""
            variables = {
                "input": {
                    "uri": f"gs://{os.environ['WORKSPACE_BUCKET_NAME']}{stripped_path}",
                    "type": "file",
                    "name": name,
                }
            }
            self._graphql_query(query, variables)
        else:
            print(f"Sending output with path {stripped_path}")

    def add_database_output(self, table_name: str):
        if self.connected:
            query = """
                                mutation addPipelineOutput ($input: AddPipelineOutputInput!) {
                                    addPipelineOutput(input: $input) { success errors }
                                }"""
            variables = {
                "input": {
                    "uri": f"postgresql://{workspace.database_host}/{workspace.database_name}/{table_name}",
                    "type": "db",
                    "name": table_name,
                }
            }
            self._graphql_query(query, variables)
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

        if self.connected:
            query = """
                    mutation logPipelineMessage ($input: LogPipelineMessageInput!) {
                        logPipelineMessage(input: $input) { success errors }
                    }"""
            variables = {"input": {"priority": priority, "message": message}}
            self._graphql_query(query, variables)
        else:
            now = (
                datetime.datetime.now(tz=datetime.timezone.utc)
                .replace(microsecond=0)
                .isoformat()
            )
            print(now, priority, message)

    @staticmethod
    def _graphql_query(
        query: str, variables: typing.Optional[typing.Dict[str, typing.Any]] = None
    ):
        token = os.environ["HEXA_TOKEN"]
        headers = {"Authorization": "Bearer %s" % token}
        r = requests.post(
            f'{os.environ["HEXA_SERVER_URL"]}/graphql/',
            headers=headers,
            json={
                "query": query,
                "variables": variables if variables is not None else {},
            },
        )
        r.raise_for_status()


current_run = CurrentRun()
