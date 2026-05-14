"""Dynamic choices classes for pipeline parameters."""

from openhexa.sdk.pipelines.exceptions import InvalidParameterError

from .ast_constructible import AstConstructible

_SUPPORTED_FORMATS = {"csv", "json", "yaml"}


class ChoicesFromFile(AstConstructible):
    """Descriptor for choices loaded dynamically from a file in the workspace file system.

    Parameters
    ----------
    path : str
        Path to the file in the workspace file system (e.g. "data/districts.csv").
    column : str, optional
        Column name (CSV) or key (JSON/YAML) to use as choice values.
        Required when the file has more than one column/key.
    format : str, optional
        File format (e.g. "csv", "json", "yaml"). Sent as-is to the platform.
    """

    def __init__(self, path: str, column: str | None = None, format: str | None = None):
        self.path = path
        self.column = column
        self.format = format
        self._validate_spec()

    def _validate_spec(self):
        """Validate the path and column specification."""
        if not self.path or not isinstance(self.path, str):
            raise InvalidParameterError("ChoicesFromFile path must be a non-empty string.")
        if self.column is not None and not isinstance(self.column, str):
            raise InvalidParameterError("ChoicesFromFile column must be a string.")
        if self.format is not None and self.format not in _SUPPORTED_FORMATS:
            raise InvalidParameterError(
                f"ChoicesFromFile format '{self.format}' is not supported. "
                f"Supported formats: {', '.join(sorted(_SUPPORTED_FORMATS))}."
            )

    def __repr__(self) -> str:
        """Return a string representation of the ChoicesFromFile instance."""
        parts = [repr(self.path)]
        if self.column is not None:
            parts.append(f"column={self.column!r}")
        if self.format is not None:
            parts.append(f"format={self.format!r}")
        return f"ChoicesFromFile({', '.join(parts)})"

    def __eq__(self, other: object) -> bool:
        """Check equality based on path, column, and format."""
        if not isinstance(other, ChoicesFromFile):
            return NotImplemented
        return self.path == other.path and self.column == other.column and self.format == other.format

    def __hash__(self) -> int:
        """Return hash based on path, column, and format."""
        return hash((self.path, self.column, self.format))

    def to_dict(self) -> dict:
        """Return a dictionary representation of the choices spec."""
        return {
            "format": self.format,
            "path": self.path,
            "column": self.column,
        }
