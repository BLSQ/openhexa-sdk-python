"""Pipeline parameters classes and functions.

See https://github.com/BLSQ/openhexa/wiki/Writing-OpenHEXA-pipelines#pipeline-parameters for more information.
"""

import typing
from enum import StrEnum

from openhexa.sdk.datasets import Dataset
from openhexa.sdk.files import File
from openhexa.sdk.pipelines.exceptions import InvalidParameterError, ParameterValueError
from openhexa.sdk.pipelines.utils import validate_pipeline_parameter_code
from openhexa.sdk.workspaces import workspace
from openhexa.sdk.workspaces.connection import (
    Connection,
    CustomConnection,
    DHIS2Connection,
    GCSConnection,
    IASOConnection,
    PostgreSQLConnection,
    S3Connection,
)
from openhexa.sdk.workspaces.current_workspace import ConnectionDoesNotExist


class ParameterType:
    """Base class for parameter types. Those parameter types are used when using the @parameter decorator."""

    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        raise NotImplementedError

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        raise NotImplementedError

    @property
    def accepts_choices(self) -> bool:
        """Return True only if the parameter type supports the "choices" optional argument."""
        return True

    @property
    def accepts_multiple(self) -> bool:
        """Return True only if the parameter type supports multiple values."""
        return True

    @staticmethod
    def normalize(value: typing.Any) -> typing.Any:
        """If appropriate, subclasses can override this method to normalize empty values to None.

        This can be used to handle empty values and normalize them to None, or to perform type conversions, allowing us
        to allow multiple input types but still normalize everything to a single type.
        """
        return value

    def validate(self, value: typing.Any | None) -> typing.Any | None:
        """Validate the provided value for this type."""
        if not isinstance(value, self.expected_type):
            raise ParameterValueError(
                f"Invalid type for value {value} (expected {self.expected_type}, got {type(value)})"
            )
        return value

    def validate_default(self, value: typing.Any | None):
        """Validate the default value configured for this type."""
        self.validate(value)

    def __str__(self) -> str:
        """Cast parameter as string."""
        return str(self.expected_type)


class StringType(ParameterType):
    """Type class for string parameters."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "str"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return str

    @staticmethod
    def normalize(value: typing.Any) -> str | None:
        """Strip leading and trailing whitespaces and convert empty strings to None."""
        if isinstance(value, str):
            normalized_value = value.strip()
        else:
            normalized_value = value

        if normalized_value == "":
            return None

        return normalized_value

    def validate_default(self, value: typing.Any | None):
        """Validate the default value configured for this type."""
        if value == "":
            raise ParameterValueError("Empty values are not accepted.")

        super().validate_default(value)


class Boolean(ParameterType):
    """Type class for boolean parameters."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "bool"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return bool

    @property
    def accepts_choices(self) -> bool:
        """Return a type string for the specs that are sent to the backend."""
        return False

    @property
    def accepts_multiple(self) -> bool:
        """Return a type string for the specs that are sent to the backend."""
        return False


class Integer(ParameterType):
    """Type class for integer parameters."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "int"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return int


class Float(ParameterType):
    """Type class for float parameters."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "float"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return float

    @staticmethod
    def normalize(value: typing.Any) -> typing.Any:
        """Normalize int values to float values if appropriate."""
        if isinstance(value, int):
            return float(value)

        return value


class ConnectionParameterType(ParameterType):
    """Abstract base class for connection parameter type classes."""

    @property
    def accepts_choices(self) -> bool:
        """Return True only if the parameter type supports the "choice values."""
        return False

    @property
    def accepts_multiple(self) -> bool:
        """Return True only if the parameter type supports multiple values."""
        return False

    def validate_default(self, value: typing.Any | None):
        """Validate the default value configured for this type."""
        if value is None:
            return

        if not isinstance(value, str):
            raise InvalidParameterError("Default value for connection parameter type should be string.")
        elif value == "":
            raise ParameterValueError("Empty values are not accepted.")

    def validate(self, value: typing.Any | None) -> Connection:
        """Validate the provided value for this type."""
        if not isinstance(value, str):
            raise ParameterValueError(f"Invalid type for value {value} (expected {str}, got {type(value)})")

        try:
            return self.to_connection(value)
        except ConnectionDoesNotExist as e:
            raise ParameterValueError(str(e))

    def to_connection(self, value: str) -> Connection:
        """Build a connection instance from the provided value (which should be a connection identifier)."""
        raise NotImplementedError


class PostgreSQLConnectionType(ConnectionParameterType):
    """Type class for PostgreSQL connections."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "postgresql"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return PostgreSQLConnection

    def to_connection(self, value: str) -> PostgreSQLConnection:
        """Build a PostgreSQL connection instance from the provided value (which should be a connection identifier)."""
        return workspace.postgresql_connection(value)


class S3ConnectionType(ConnectionParameterType):
    """Type class for S3 connections."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "s3"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return S3Connection

    def to_connection(self, value: str) -> S3Connection:
        """Build a S3 connection instance from the provided value (which should be a connection identifier)."""
        return workspace.s3_connection(value)


class GCSConnectionType(ConnectionParameterType):
    """Type class for GCS connections."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "gcs"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return GCSConnection

    def to_connection(self, value: str) -> GCSConnection:
        """Build a GCS connection instance from the provided value (which should be a connection identifier)."""
        return workspace.gcs_connection(value)


class DHIS2ConnectionType(ConnectionParameterType):
    """Type class for DHIS2 connections."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "dhis2"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return DHIS2Connection

    def to_connection(self, value: str) -> DHIS2Connection:
        """Build a DHIS2 connection instance from the provided value (which should be a connection identifier)."""
        return workspace.dhis2_connection(value)


class IASOConnectionType(ConnectionParameterType):
    """Type class for IASO connections."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "iaso"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return IASOConnection

    def to_connection(self, value: str) -> IASOConnection:
        """Build a IASO connection instance from the provided value (which should be a connection identifier)."""
        return workspace.iaso_connection(value)


class CustomConnectionType(ConnectionParameterType):
    """Type class for custom connections."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "custom"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return CustomConnection

    def to_connection(self, value: str) -> CustomConnection:
        """Build a custom connection instance from the provided value (which should be a connection identifier)."""
        return workspace.custom_connection(value)


class DatasetType(ParameterType):
    """Type class for dataset parameter."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "dataset"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return Dataset

    def validate_default(self, value: typing.Any | None):
        """Validate the default value configured for this type."""
        if value is None:
            return

        if not isinstance(value, str):
            raise InvalidParameterError("Default value for dataset parameter type should be string.")
        elif value == "":
            raise ParameterValueError("Empty values are not accepted.")

    def validate(self, value: typing.Any | None) -> Dataset:
        """Validate the provided value for this type."""
        if not isinstance(value, str):
            raise ParameterValueError(f"Invalid type for value {value} (expected {str}, got {type(value)})")

        try:
            return workspace.get_dataset(value)
        except ValueError as e:
            raise ParameterValueError(str(e))


class FileType(ParameterType):
    """Type class for file parameter."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "file"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return File

    def validate_default(self, value: typing.Any | None):
        """Validate the default value configured for this type."""
        if value is None:
            return

        if not isinstance(value, str):
            raise InvalidParameterError("Default value for file parameter type should be string.")
        elif value == "":
            raise ParameterValueError("Empty values are not accepted.")

    def validate(self, value: typing.Any | None) -> File:
        """Validate the provided value for this type."""
        if not isinstance(value, str):
            raise ParameterValueError(f"Invalid type for value {value} (expected {str}, got {type(value)})")

        try:
            return workspace.get_file(value)
        except ValueError as e:
            raise ParameterValueError(str(e))


TYPES_BY_PYTHON_TYPE = {
    "str": StringType,
    "bool": Boolean,
    "int": Integer,
    "float": Float,
    "DHIS2Connection": DHIS2ConnectionType,
    "PostgreSQLConnection": PostgreSQLConnectionType,
    "IASOConnection": IASOConnectionType,
    "S3Connection": S3ConnectionType,
    "GCSConnection": GCSConnectionType,
    "CustomConnection": CustomConnectionType,
    "Dataset": DatasetType,
    "File": FileType,
}


class IASOWidget(StrEnum):
    """Enum for IASO widgets."""

    IASO_FORMS = "IASO_FORMS"
    IASO_ORG_UNITS = "IASO_ORG_UNITS"
    IASO_PROJECTS = "IASO_PROJECTS"


class DHIS2Widget(StrEnum):
    """Enum for DHIS2 widgets."""

    ORG_UNITS = "DHIS2_ORG_UNITS"
    ORG_UNIT_GROUPS = "DHIS2_ORG_UNIT_GROUPS"
    ORG_UNIT_LEVELS = "DHIS2_ORG_UNIT_LEVELS"
    DATASETS = "DHIS2_DATASETS"
    DATA_ELEMENTS = "DHIS2_DATA_ELEMENTS"
    DATA_ELEMENT_GROUPS = "DHIS2_DATA_ELEMENT_GROUPS"
    INDICATORS = "DHIS2_INDICATORS"
    INDICATOR_GROUPS = "DHIS2_INDICATOR_GROUPS"


class Parameter:
    """Pipeline parameter class. Contains validation logic specs generation logic."""

    def __init__(
        self,
        code: str,
        *,
        type: type[
            str
            | int
            | bool
            | float
            | DHIS2Connection
            | IASOConnection
            | PostgreSQLConnection
            | GCSConnection
            | S3Connection
            | CustomConnection
            | Dataset
        ],
        name: str | None = None,
        choices: typing.Sequence | None = None,
        help: str | None = None,
        default: typing.Any | None = None,
        widget: DHIS2Widget | IASOWidget | None = None,
        connection: str | None = None,
        required: bool = True,
        multiple: bool = False,
    ):
        validate_pipeline_parameter_code(code)
        self.code = code

        try:
            self.type = TYPES_BY_PYTHON_TYPE[type.__name__]()
        except (KeyError, AttributeError):
            valid_parameter_types = [k for k in TYPES_BY_PYTHON_TYPE.keys()]
            raise InvalidParameterError(
                f"Invalid parameter type provided ({type}). "
                f"Valid parameter types are {', '.join(valid_parameter_types)}"
            )

        if choices is not None:
            if not self.type.accepts_choices:
                raise InvalidParameterError(f"Parameters of type {self.type} don't accept choices.")
            elif len(choices) == 0:
                raise InvalidParameterError("Choices, if provided, cannot be empty.")

            try:
                for choice in choices:
                    self.type.validate(choice)
            except ParameterValueError:
                raise InvalidParameterError(f"The provided choices are not valid for the {self.type} parameter type.")
        self.choices = choices

        self.name = name
        self.help = help
        self.required = required

        if multiple is True and not self.type.accepts_multiple:
            raise InvalidParameterError(f"Parameters of type {self.type} can't have multiple values.")
        self.multiple = multiple

        self.widget = widget
        self.connection = connection

        self._validate_default(default, multiple)
        self.default = default

    def validate(self, value: typing.Any) -> typing.Any:
        """Validate the provided value against the parameter, taking required / default options into account."""
        if self.multiple:
            return self._validate_multiple(value)
        else:
            return self._validate_single(value)

    def to_dict(self) -> dict[str, typing.Any]:
        """Return a dictionary representation of the Parameter instance."""
        return {
            "code": self.code,
            "type": self.type.spec_type,
            "name": self.name,
            "choices": self.choices,
            "help": self.help,
            "default": self.default,
            "widget": self.widget.value if self.widget else None,
            "connection": self.connection,
            "required": self.required,
            "multiple": self.multiple,
        }

    def _validate_single(self, value: typing.Any):
        # Normalize empty values to None and handles default
        normalized_value = self.type.normalize(value)
        if normalized_value is None and self.default is not None:
            normalized_value = self.default

        if normalized_value is None:
            if self.required:
                raise ParameterValueError(f"{self.code} is required")

            return None

        pre_validated = self.type.validate(normalized_value)
        if self.choices is not None and pre_validated not in self.choices:
            raise ParameterValueError(f"The provided value for {self.code} is not included in the provided choices.")

        return pre_validated

    def _validate_multiple(self, value: typing.Any):
        # Reject values that are not lists
        if value is not None and not isinstance(value, list):
            raise InvalidParameterError("If provided, value should be a list when parameter is multiple.")

        # Normalize empty values to an empty list
        if value is None:
            normalized_value = []
        else:
            normalized_value = [self.type.normalize(v) for v in value]
            normalized_value = list(filter(lambda v: v is not None, normalized_value))
        if len(normalized_value) == 0 and self.default is not None:
            normalized_value = self.default

        if len(normalized_value) == 0 and self.required:
            raise ParameterValueError(f"{self.code} is required")

        pre_validated = [self.type.validate(single_value) for single_value in normalized_value]
        if self.choices is not None and any(v not in self.choices for v in pre_validated):
            raise ParameterValueError(
                f"One of the provided values for {self.code} is not included in the provided choices."
            )

        return pre_validated

    def _validate_default(self, default: typing.Any, multiple: bool):
        if default is None:
            return

        try:
            if multiple:
                if not isinstance(default, list):
                    raise InvalidParameterError("Default values should be lists when using multiple=True")
                for default_value in default:
                    self.type.validate_default(default_value)
            else:
                self.type.validate_default(default)
        except ParameterValueError:
            raise InvalidParameterError(f"The default value for {self.code} is not valid.")

        if self.choices is not None:
            if isinstance(default, list):
                if not all(d in self.choices for d in default):
                    raise InvalidParameterError(
                        f"The default list of values for {self.code} is not included in the provided choices."
                    )
            elif default not in self.choices:
                raise InvalidParameterError(
                    f"The default value for {self.code} is not included in the provided choices."
                )


def validate_parameters(parameters: list[Parameter]):
    """Validate the provided connection parameters if they relate to existing connection parameter."""
    supported_connection_types = {DHIS2ConnectionType, IASOConnectionType}
    connection_parameters = {p.code for p in parameters if type(p.type) in supported_connection_types}

    for parameter in parameters:
        if parameter.connection and parameter.connection not in connection_parameters:
            raise InvalidParameterError(
                f"Connection field '{parameter.code}' references a non-existing connection parameter '{parameter.connection}'"
            )
        if (
            parameter.widget
            and (parameter.widget in DHIS2Widget or parameter.widget in IASOWidget)
            and not parameter.connection
        ):
            raise InvalidParameterError(
                f"Widgets require a connection parameter. Please provide a connection parameter for {parameter.code}. "
                f"Example: @parameter('my_connection', ...)"
                f"Example: @parameter('{parameter.code}', widget = ..., connection='my_connection')"
            )


def parameter(
    code: str,
    *,
    type: type[
        str
        | int
        | bool
        | float
        | DHIS2Connection
        | IASOConnection
        | PostgreSQLConnection
        | GCSConnection
        | S3Connection
        | CustomConnection
        | Dataset
    ],
    name: str | None = None,
    choices: typing.Sequence | None = None,
    help: str | None = None,
    widget: DHIS2Widget | IASOWidget | None = None,
    connection: str | None = None,
    default: typing.Any | None = None,
    required: bool = True,
    multiple: bool = False,
):
    """Decorate a pipeline function by attaching a parameter to it..

    This decorator must be used on a function decorated by the @pipeline decorator.

    Parameters
    ----------
    code : str
        The parameter identifier (must be unique for a given pipeline)
    type : {str, int, bool, float, DHIS2Connection, IASOConnection, PostgreSQLConnection, GCSConnection, S3Connection}
        The parameter Python type
    name : str, optional
        A name for the parameter (will be used instead of the code in the web interface)
    choices : list, optional
        An optional list or tuple of choices for the parameter (will be used to build a choice widget in the web
        interface)
    help : str, optional
        An optional help text to be displayed in the web interface
    widget : DHIS2Widget|IASOWidget, optional
        An optional widget type for the parameter (only used if the parameter type is DHIS2Connection, IASOConnection)
    connection : str, optional
        An optional connection parameter that will be used to link widget to the connection.
    default : any, optional
        An optional default value for the parameter (should be of the type defined by the type parameter)
    required : bool, default=True
        Whether the parameter is mandatory
    multiple : bool, default=True
        Whether this parameter should be provided multiple values (if True, the value must be provided as a list of
        values of the chosen type)

    Returns
    -------
    typing.Callable
        A decorator that returns the Pipeline with the parameter attached

    """

    def decorator(fun):
        return FunctionWithParameter(
            fun,
            Parameter(
                code,
                type=type,
                name=name,
                choices=choices,
                help=help,
                default=default,
                required=required,
                widget=widget,
                connection=connection,
                multiple=multiple,
            ),
        )

    return decorator


class FunctionWithParameter:
    """Wrapper class for pipeline functions decorated with the @parameter decorator."""

    def __init__(self, function, added_parameter: Parameter):
        self.function = function
        self.parameter = added_parameter

    def get_all_parameters(self) -> list[Parameter]:
        """Go through the decorators chain to find all pipeline parameters."""
        if isinstance(self.function, FunctionWithParameter):
            return [self.parameter, *self.function.get_all_parameters()]

        return [self.parameter]

    def __call__(self, *args, **kwargs):
        """Call the decorated pipeline function."""
        return self.function(*args, **kwargs)
