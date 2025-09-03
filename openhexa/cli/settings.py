"""User settings for the OpenHexa CLI."""

import logging
import os
from configparser import ConfigParser

import click

from openhexa.sdk.pipelines.log_level import LogLevel

CONFIGFILE_PATH = os.path.expanduser("~") + "/.openhexa.ini"


def _open_config():
    """Open the local settings file using configparser.

    A default settings file will be generated if the file does not exist.
    """
    config = ConfigParser()
    if os.path.exists(CONFIGFILE_PATH):
        config.read(CONFIGFILE_PATH)
    else:
        config.read_string(
            """
        [openhexa]
        url=https://api.openhexa.org

        [workspaces]
        """
        )
    return config


def _save_config(config: ConfigParser):
    """Save the provided configparser local settings to disk."""
    with open(CONFIGFILE_PATH, "w") as configfile:
        config.write(configfile)


class Settings:
    """Class that holds the user settings for the CLI."""

    _file_config: ConfigParser = None

    def __init__(self):
        self.refresh()

    @property
    def debug(self):
        """Return the debug flag from the settings file or environment variables."""
        return os.getenv("DEBUG") or os.getenv("HEXA_DEBUG")

    @property
    def verify_ssl(self):
        """Return the SSL verification flag from environment variables."""
        return os.getenv("HEXA_VERIFY_SSL", "True").lower() not in ("0", "false")

    @property
    def api_url(self):
        """Return the API URL from the settings file or environment variables."""
        url_from_env = os.getenv("HEXA_API_URL") or os.getenv("HEXA_SERVER_URL")
        if url_from_env is None:
            url_from_env = self._file_config["openhexa"]["url"]
        return url_from_env.rstrip("/")

    @property
    def public_api_url(self):
        """Return the public API URL from the settings file or environment variables."""
        return self.api_url.replace("api", "app")

    @property
    def current_workspace(self):
        """Return the current workspace from the settings file or environment variables."""
        if os.getenv("HEXA_WORKSPACE"):
            return os.getenv("HEXA_WORKSPACE")
        try:
            return self._file_config["openhexa"]["current_workspace"]
        except KeyError:
            return None

    @property
    def workspaces(self):
        """Return the workspaces from the settings file."""
        return self._file_config["workspaces"]

    @property
    def log_level(self) -> LogLevel:
        """Return the log level from the environment variables."""
        return LogLevel.parse_log_level(os.getenv("HEXA_LOG_LEVEL"))

    def activate(self, workspace: str):
        """Set the current workspace in the settings file."""
        if workspace not in self.workspaces:
            raise ValueError(f"Workspace {workspace} does not exist.")
        self._file_config["openhexa"]["current_workspace"] = workspace
        self.save()

    def add_workspace(self, workspace: str, token: str, enabled: bool = True):
        """Add a workspace to the settings file."""
        self._file_config["workspaces"].update({workspace: token})
        if enabled:
            self._file_config["openhexa"]["current_workspace"] = workspace
        self.save()

    def remove_workspace(self, workspace: str):
        """Remove a workspace from the settings file."""
        del self._file_config["workspaces"][workspace]
        if self._file_config["openhexa"]["current_workspace"] == workspace:
            self._file_config["openhexa"]["current_workspace"] = None
        self.save()

    def set_api_url(self, url: str):
        """Set the API URL in the settings file."""
        self._file_config["openhexa"]["url"] = url
        self.save()

    @property
    def access_token(self):
        """Return the access token from the settings file or environment variables."""
        if os.getenv("HEXA_TOKEN"):
            return os.getenv("HEXA_TOKEN")
        return self._file_config["workspaces"].get(self.current_workspace)

    @property
    def last_version_check(self):
        """Return the last version check timestamp from the settings file."""
        val = self._file_config["openhexa"].get("last_version_check", None)
        if val is not None:
            return int(val)

    @last_version_check.setter
    def last_version_check(self, value: int):
        """Set the last version check timestamp in the settings file."""
        assert isinstance(value, int), "last_version_check must be an integer."
        self._file_config["openhexa"]["last_version_check"] = str(value)
        self.save()

    @property
    def last_breaking_change_check(self):
        """Return the last breaking change check timestamp from the settings file."""
        val = self._file_config["openhexa"].get("last_breaking_change_check", None)
        if val is not None:
            return int(val)

    @last_breaking_change_check.setter
    def last_breaking_change_check(self, value: int):
        """Set the last breaking change check timestamp in the settings file."""
        assert isinstance(value, int), "last_breaking_change_check must be an integer."
        self._file_config["openhexa"]["last_breaking_change_check"] = str(value)
        self.save()

    def save(self):
        """Save the settings to disk."""
        _save_config(self._file_config)
        self.refresh()

    def refresh(self):
        """Refresh the settings file."""
        self._file_config = _open_config()

    def __repr__(self):
        """Return a string representation of the object."""
        return f"<Config(url={self.api_url}, current_workspace={self.current_workspace}, debug={self.debug})>"


class ClickEchoHandler(logging.Handler):
    """Custom logging handler that uses click.echo to print logs."""

    def emit(self, record):
        """Emit the log record."""
        msg = self.format(record)
        click.echo(msg)


def setup_logging():
    """Set up the logging for the CLI."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter("%(message)s")

    # Create an instance of the custom handler
    click_handler = ClickEchoHandler()

    # Set the formatter for the handler
    click_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(click_handler)


settings = Settings()
