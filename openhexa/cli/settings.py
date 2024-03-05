"""User settings for the OpenHexa CLI."""
import os
from configparser import ConfigParser

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
    def api_url(self):
        """Return the API URL from the settings file or environment variables."""
        url_from_env = os.getenv("HEXA_API_URL") or os.getenv("HEXA_SERVER_URL")
        if url_from_env is None:
            return self._file_config["openhexa"]["url"]

    @property
    def public_api_url(self):
        """Return the public API URL from the settings file or environment variables."""
        url_from_env = os.getenv("HEXA_API_URL") or os.getenv("HEXA_SERVER_URL")
        if url_from_env is not None:
            return url_from_env
        return self._file_config["openhexa"]["url"].replace("api", "app")

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


settings = Settings()
