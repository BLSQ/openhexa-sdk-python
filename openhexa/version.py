"""Openhexa SDK version module."""
from importlib.metadata import version

try:
    __version__ = version("openhexa.sdk")
except Exception:
    __version__ = "unknown"
