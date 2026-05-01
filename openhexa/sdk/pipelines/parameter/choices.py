"""Dynamic choices classes for pipeline parameters."""

from openhexa.sdk.pipelines.exceptions import InvalidParameterError

_SUPPORTED_FORMATS = {"csv", "json", "yaml", "yml"}


class FileChoices:
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
        self.format = self._detect_format(path)
        self.validate_spec()

    def _detect_format(self, path: str) -> str:
        if not path or not isinstance(path, str):
            raise InvalidParameterError("FileChoices path must be a non-empty string.")
        ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""
        if ext not in _SUPPORTED_FORMATS:
            raise InvalidParameterError(
                f"Cannot determine file format from path '{path}'. "
                f"Supported extensions: {', '.join(sorted(_SUPPORTED_FORMATS))}."
            )
        return "yaml" if ext == "yml" else ext

    def validate_spec(self):
        if not self.path or not isinstance(self.path, str):
            raise InvalidParameterError("FileChoices path must be a non-empty string.")
        if self.column is not None and not isinstance(self.column, str):
            raise InvalidParameterError("FileChoices column must be a string.")

    def to_dict(self) -> dict:
        return {
            "format": self.format,
            "path": self.path,
            "column": self.column,
        }
