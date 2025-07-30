"""File-related classes and functions.

TODO: Add link to wiki
"""


class File:
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
