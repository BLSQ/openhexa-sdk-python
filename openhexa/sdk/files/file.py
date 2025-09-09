"""File-related classes and functions.

See https://github.com/BLSQ/openhexa/wiki/Writing-OpenHEXA-pipelines#using-file-parameters
"""


class File:
    """File class.

    See https://github.com/BLSQ/openhexa/wiki/Writing-OpenHEXA-pipelines#using-file-parameters
    """

    def __init__(
        self,
        key: str,
        name: str,
        path: str,
        size: int,
        type: str,
    ):
        self.key = key
        self.name = name
        self.path = path
        self.size = size
        self.type = type

    def __repr__(self) -> str:
        """Safe representation of a file instance."""
        return f"<File key={self.key} name={self.name} path={self.path}>"
