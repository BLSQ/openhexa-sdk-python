"""Parameter class, decorator, and validation logic for pipeline parameters."""

import typing

from openhexa.sdk.datasets import Dataset
from openhexa.sdk.files import File
from openhexa.sdk.pipelines.exceptions import InvalidParameterError, ParameterValueError
from openhexa.sdk.pipelines.utils import validate_pipeline_parameter_code
from openhexa.sdk.workspaces.connection import (
    CustomConnection,
    DHIS2Connection,
    GCSConnection,
    IASOConnection,
    PostgreSQLConnection,
    S3Connection,
)

from .choices import FileChoices
from .types import TYPES_BY_PYTHON_TYPE, Boolean, DHIS2ConnectionType, IASOConnectionType, Secret
from .widgets import DHIS2Widget, IASOWidget


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
            | Secret
            | DHIS2Connection
            | IASOConnection
            | PostgreSQLConnection
            | GCSConnection
            | S3Connection
            | CustomConnection
            | Dataset
            | File
        ],
        name: str | None = None,
        choices: typing.Sequence | FileChoices | None = None,
        help: str | None = None,
        default: typing.Any | None = None,
        widget: DHIS2Widget | IASOWidget | None = None,
        connection: str | None = None,
        required: bool = True,
        multiple: bool = False,
        directory: str | None = None,
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
            if isinstance(choices, FileChoices):
                # validate_spec() already ran in FileChoices.__init__; nothing more to check here
                pass
            else:
                if len(choices) == 0:
                    raise InvalidParameterError("Choices, if provided, cannot be empty.")
                try:
                    for choice in choices:
                        self.type.validate(choice)
                except ParameterValueError:
                    raise InvalidParameterError(
                        f"The provided choices are not valid for the {self.type} parameter type."
                    )
        self.choices = choices

        self.name = name
        self.help = help
        self.required = required

        if multiple is True and not self.type.accepts_multiple:
            raise InvalidParameterError(f"Parameters of type {self.type} can't have multiple values.")
        self.multiple = multiple

        self.widget = widget
        self.connection = connection
        self.directory = directory

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
        d = {
            "code": self.code,
            "type": self.type.spec_type,
            "name": self.name,
            "choices": None if isinstance(self.choices, FileChoices) else self.choices,
            "help": self.help,
            "default": self.default,
            "widget": self.widget.value if self.widget else None,
            "connection": self.connection,
            "required": self.required,
            "multiple": self.multiple,
            "directory": self.directory,
        }
        if isinstance(self.choices, FileChoices):
            d["file_choices"] = self.choices.to_dict()
        return d

    def _validate_single(self, value: typing.Any):
        # Normalize empty values to None and handles default
        normalized_value = self.type.normalize(value)
        if normalized_value is None and self.default is not None:
            normalized_value = self.default

        if normalized_value is None:
            if isinstance(self.type, Boolean):
                normalized_value = False
            elif self.required:
                raise ParameterValueError(f"{self.code} is required")
            else:
                return None

        pre_validated = self.type.validate(normalized_value)
        if self.choices is not None and not isinstance(self.choices, FileChoices) and pre_validated not in self.choices:
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
        if (
            self.choices is not None
            and not isinstance(self.choices, FileChoices)
            and any(v not in self.choices for v in pre_validated)
        ):
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

        if self.choices is not None and not isinstance(self.choices, FileChoices):
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
        | Secret
        | DHIS2Connection
        | IASOConnection
        | PostgreSQLConnection
        | GCSConnection
        | S3Connection
        | CustomConnection
        | Dataset
        | File
    ],
    name: str | None = None,
    choices: typing.Sequence | FileChoices | None = None,
    help: str | None = None,
    widget: DHIS2Widget | IASOWidget | None = None,
    connection: str | None = None,
    default: typing.Any | None = None,
    required: bool = True,
    multiple: bool = False,
    directory: str | None = None,
):
    """Decorate a pipeline function by attaching a parameter to it..

    This decorator must be used on a function decorated by the @pipeline decorator.

    Parameters
    ----------
    code : str
        The parameter identifier (must be unique for a given pipeline)
    type : {str, int, bool, float, DHIS2Connection, IASOConnection, PostgreSQLConnection, GCSConnection, S3Connection, CustomConnection, Dataset, File}
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
    directory : str, optional
        An optional parameter to force file selection to specific directory (only used for parameter type File). If the directory does not exist, it will be ignored.

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
                directory=directory,
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
