import re
import typing


class ParameterValueError(Exception):
    pass


class ParameterType:
    """Base class for parameter types. Those parameter types are used when using the @parameter decorator"""

    def spec_type(self) -> str:
        """Returns a type string for the specs that are sent to the backend."""

        raise NotImplementedError

    @property
    def expected_type(self) -> typing.Type:
        """Returns the python type expected for values."""

        raise NotImplementedError

    @property
    def accepts_choice(self) -> bool:
        return True

    @property
    def accepts_multiple(self) -> bool:
        return True

    @staticmethod
    def normalize(value: typing.Any) -> typing.Any:
        """If appropriate, subclasses can override this method to normalize empty values to None.

        This can be used to handle empty values and normalize them to None, or to perform type conversions, allowing us
        to allow multiple input types but still normalize everything to a single type.
        """

        return value

    def validate(
        self, value: typing.Optional[typing.Any], allow_empty: bool = True
    ) -> typing.Optional[typing.Any]:
        """Validate the provided value for this type."""

        if not isinstance(value, self.expected_type):
            raise ParameterValueError(
                f"Invalid type for value {value} (expected {self.expected_type}, got {type(value)})"
            )

        return value

    def __str__(self) -> str:
        return str(self.expected_type)


class String(ParameterType):
    @property
    def spec_type(self) -> str:
        return "str"

    @property
    def expected_type(self) -> typing.Type:
        return str

    @staticmethod
    def normalize(value: typing.Any) -> typing.Optional[str]:
        if isinstance(value, str):
            normalized_value = value.strip()
        else:
            normalized_value = value

        if normalized_value == "":
            return None

        return normalized_value

    def validate(
        self, value: typing.Optional[typing.Any], *, allow_empty: bool = True
    ) -> typing.Optional[str]:
        if not allow_empty and value == "":
            raise ParameterValueError("Empty values are not accepted.")

        return super().validate(value, allow_empty)


class Boolean(ParameterType):
    @property
    def spec_type(self) -> str:
        return "bool"

    @property
    def expected_type(self) -> typing.Type:
        return bool

    @property
    def accepts_choice(self) -> bool:
        return False

    @property
    def accepts_multiple(self) -> bool:
        return False


class Integer(ParameterType):
    @property
    def spec_type(self) -> str:
        return "int"

    @property
    def expected_type(self) -> typing.Type:
        return int


class Float(ParameterType):
    @property
    def spec_type(self) -> str:
        return "float"

    @property
    def expected_type(self) -> typing.Type:
        return float

    @staticmethod
    def normalize(value: typing.Any) -> typing.Any:
        if isinstance(value, int):
            return float(value)

        return value


TYPES_BY_PYTHON_TYPE = {str: String, bool: Boolean, int: Integer}


class InvalidParameterError(Exception):
    pass


class Parameter:
    """Pipeline parameter class. Contains validation logic specs generation logic."""

    def __init__(
        self,
        code: str,
        *,
        type: typing.Union[typing.Type[str], typing.Type[int], typing.Type[bool]],
        name: typing.Optional[str] = None,
        choices: typing.Optional[typing.Sequence] = None,
        help: typing.Optional[str] = None,
        default: typing.Optional[typing.Any] = None,
        required: bool = True,
        multiple: bool = False,
    ):
        if re.match("^[a-z_][a-z_0-9]+$", code) is None:
            raise InvalidParameterError(
                f"Invalid parameter code provided ({code}). Parameter must start with a letter or an underscore, and can only contain lower case letters, numbers and underscores."
            )

        self.code = code

        try:
            self.type = TYPES_BY_PYTHON_TYPE[type]()
        except KeyError:
            valid_parameter_types = [str(k) for k in TYPES_BY_PYTHON_TYPE.keys()]
            raise InvalidParameterError(
                f"Invalid parameter type provided ({type}). Valid parameter types are {', '.join(valid_parameter_types)}"
            )

        if choices is not None:
            if not self.type.accepts_choice:
                raise InvalidParameterError(
                    f"Parameters of type {self.type} don't accept choices."
                )
            elif len(choices) == 0:
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
            raise InvalidParameterError(
                f"Parameters of type {self.type} can't have multiple values."
            )
        self.multiple = multiple

        self._validate_default(default, multiple)
        self.default = default

    def validate(self, value: typing.Any) -> typing.Any:
        """Validates the provided value against the parameter, taking required / default options into account."""

        if self.multiple:
            return self._validate_multiple(value)
        else:
            return self._validate_single(value)

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
            raise ParameterValueError(
                f"The provided value for {self.code} is not included in the provided choices."
            )

        return pre_validated

    def _validate_multiple(self, value: typing.Any):
        # Reject values that are not lists
        if value is not None and not isinstance(value, list):
            raise InvalidParameterError(
                "If provided, value should be a list when parameter is multiple."
            )

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

        pre_validated = [
            self.type.validate(single_value) for single_value in normalized_value
        ]
        if self.choices is not None and any(
            v not in self.choices for v in pre_validated
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
                    raise InvalidParameterError(
                        "Default values should be lists when using multiple=True"
                    )
                for default_value in default:
                    self.type.validate(default_value, allow_empty=False)
            else:
                self.type.validate(default, allow_empty=False)
        except ParameterValueError:
            raise InvalidParameterError(
                f"The default value for {self.code} is not valid."
            )

    def parameter_spec(self):
        """Generates specification for this parameter, to be provided to the OpenHexa backend."""

        return {
            "type": self.type.spec_type,
            "required": self.required,
            "choices": self.choices,
            "code": self.code,
            "name": self.name,
            "help": self.help,
            "multiple": self.multiple,
            "default": self.default,
        }


def parameter(
    code: str,
    *,
    type: typing.Union[typing.Type[str], typing.Type[int], typing.Type[bool]],
    name: typing.Optional[str] = None,
    choices: typing.Optional[typing.Sequence] = None,
    help: typing.Optional[str] = None,
    default: typing.Optional[typing.Any] = None,
    required: bool = True,
    multiple: bool = False,
):
    """parameter decorator."""

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
                multiple=multiple,
            ),
        )

    return decorator


class FunctionWithParameter:
    """This class serves as a wrapper for functions decorated with the @parameter decorator."""

    def __init__(self, function, added_parameter: Parameter):
        self.function = function
        self.parameter = added_parameter

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def get_all_parameters(self):
        if isinstance(self.function, FunctionWithParameter):
            return [self.parameter, *self.function.get_all_parameters()]

        return [self.parameter]
