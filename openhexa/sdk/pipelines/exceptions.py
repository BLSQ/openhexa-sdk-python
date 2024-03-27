"""Exceptions for the pipelines module."""


class PipelineNotFound(Exception):
    """Errors related to pipeline not found in a file."""

    pass


class InvalidParameterError(Exception):
    """Raised whenever parameter options (usually passed to the @parameter decorator) are invalid."""

    pass


class ParameterValueError(Exception):
    """Raised whenever values for a parameter provided for a pipeline run are invalid."""

    pass
