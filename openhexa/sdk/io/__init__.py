import sys
from pathlib import Path


class WorkspaceDataHelper:
    def __init__(self):
        self.connected = False

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


workspace_data = WorkspaceDataHelper()

__all__ = ["workspace_data"]
