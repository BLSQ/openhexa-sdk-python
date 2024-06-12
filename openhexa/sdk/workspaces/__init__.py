"""Workspaces package.

See https://github.com/BLSQ/openhexa/wiki/User-manual#about-workspaces for more information about OpenHEXA workspaces.
"""

from .current_workspace import CurrentWorkspace

# Once we deprecate the `python pipeline.py` command, we can enhance this to only load the workspace
# if we're in a pipeline/jupyter context
workspace = CurrentWorkspace()


__all__ = ["workspace"]
