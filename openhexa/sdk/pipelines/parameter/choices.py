"""Dynamic choices classes for pipeline parameters."""

from openhexa.sdk.pipelines.exceptions import InvalidParameterError

from .ast_constructible import AstConstructible

_SUPPORTED_FORMATS = {"csv", "json", "yaml", "yml"}


class ChoicesFromFile(AstConstructible):
    """Descriptor for choices loaded dynamically from a file in the workspace file system.

    The file format is inferred from the path extension (.csv, .json, .yaml, .yml).
    For CSV files with a single column, that column is used automatically.
    For CSV/JSON/YAML files with multiple columns/keys, `column` must be specified.

    Parameters
    ----------
    path : str
        Path to the file in the workspace file system (e.g. "data/districts.csv").
    column : str, optional
        Column name (CSV) or key (JSON/YAML) to use as choice values.
        Required when the file has more than one column/key.
    """

    def __init__(self, path: str, column: str | None = None):
        self.path = path
        self.column = column
        self.validate_spec()
        self.format = self._detect_format(path)

    @staticmethod
    def _detect_format(path: str) -> str:
        ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""
        if ext not in _SUPPORTED_FORMATS:
            raise InvalidParameterError(
                f"Cannot determine file format from path '{path}'. "
                f"Supported extensions: {', '.join(sorted(_SUPPORTED_FORMATS))}."
            )
        return "yaml" if ext == "yml" else ext

    def validate_spec(self):
        """Validate the path and column specification."""
        if not self.path or not isinstance(self.path, str):
            raise InvalidParameterError("ChoicesFromFile path must be a non-empty string.")
        if self.column is not None and not isinstance(self.column, str):
            raise InvalidParameterError("ChoicesFromFile column must be a string.")

    def __repr__(self) -> str:
        if self.column is not None:
            return f"ChoicesFromFile({self.path!r}, column={self.column!r})"
        return f"ChoicesFromFile({self.path!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChoicesFromFile):
            return NotImplemented
        return self.path == other.path and self.column == other.column

    def __hash__(self) -> int:
        return hash((self.path, self.column))

    def to_dict(self) -> dict:
        """Return a dictionary representation of the choices spec."""
        return {
            "format": self.format,
            "path": self.path,
            "column": self.column,
        }
