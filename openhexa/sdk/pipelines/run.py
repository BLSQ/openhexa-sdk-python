import datetime
import typing


class CurrentRun:
    @staticmethod
    def add_file_output(path: str, *, name: str = None):
        print(f"Sending output with path {path} and name: {name}")

    @staticmethod
    def add_database_output(table_name: str, *, name: str = None):
        print(f"Sending output with table_name {table_name} and name: {name}")

    def log_debug(self, message: str):
        self._log_message("DEBUG", message)

    def log_info(self, message: str):
        self._log_message("DEBUG", message)

    def log_warning(self, message: str):
        self._log_message("DEBUG", message)

    def log_error(self, message: str):
        self._log_message("DEBUG", message)

    def log_critical(self, message: str):
        self._log_message("DEBUG", message)

    @staticmethod
    def _log_message(
        priority: typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        message: str,
    ):
        valid_priorities = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if priority not in valid_priorities:
            raise ValueError(f"priority must be one of {', '.join(valid_priorities)}")

        now = (
            datetime.datetime.now(tz=datetime.timezone.utc)
            .replace(microsecond=0)
            .isoformat()
        )
        print(now, priority, message)


current_run = CurrentRun()
