"""Pipeline parameters classes and functions.

See https://github.com/BLSQ/openhexa/wiki/Writing-OpenHEXA-pipelines#pipeline-parameters for more information.
"""

from openhexa.sdk.pipelines.exceptions import InvalidParameterError, ParameterValueError

from .choices import FileChoices
from .decorator import FunctionWithParameter, Parameter, parameter, validate_parameters
from .types import (
    TYPES_BY_PYTHON_TYPE,
    Boolean,
    ConnectionParameterType,
    CustomConnectionType,
    DatasetType,
    DHIS2ConnectionType,
    FileType,
    Float,
    GCSConnectionType,
    IASOConnectionType,
    Integer,
    ParameterType,
    PostgreSQLConnectionType,
    S3ConnectionType,
    Secret,
    SecretType,
    StringType,
)
from .widgets import DHIS2Widget, IASOWidget

__all__ = [
    # Decorator and core classes
    "parameter",
    "Parameter",
    "FunctionWithParameter",
    "validate_parameters",
    # Type base classes
    "ParameterType",
    "ConnectionParameterType",
    # Primitive types
    "StringType",
    "Boolean",
    "Integer",
    "Float",
    # Connection types
    "PostgreSQLConnectionType",
    "S3ConnectionType",
    "GCSConnectionType",
    "DHIS2ConnectionType",
    "IASOConnectionType",
    "CustomConnectionType",
    # Resource types
    "DatasetType",
    "FileType",
    # Secret
    "Secret",
    "SecretType",
    # Registry
    "TYPES_BY_PYTHON_TYPE",
    # Dynamic choices
    "FileChoices",
    # Widgets
    "DHIS2Widget",
    "IASOWidget",
    # Exceptions (re-exported for backward compat)
    "InvalidParameterError",
    "ParameterValueError",
]
