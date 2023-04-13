import typing


class ArgumentType:
    """Base class for argument types. Those argument types are used when using the @argument decorator"""

    def __str__(self):
        raise NotImplementedError

    @property
    def expected_type(self) -> typing.Type:
        raise NotImplementedError

    def validate(self, value: typing.Any) -> typing.Any:
        """Validate the provided value for this type."""

        if not isinstance(value, self.expected_type):
            raise ValueError("Invalid type")

        return value


class String(ArgumentType):
    def __str__(self):
        return "string"

    @property
    def expected_type(self) -> typing.Type:
        return str


class Boolean(ArgumentType):
    def __str__(self):
        return "boolean"

    @property
    def expected_type(self) -> typing.Type:
        return bool


class Integer(ArgumentType):
    def __str__(self):
        return "integer"

    @property
    def expected_type(self) -> typing.Type:
        return int


TYPES_BY_PYTHON_TYPE = {str: String, bool: Boolean, int: Integer}


class Argument:
    """Pipeline argument class. Contains validation logic specs generation logic."""

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
        multiple: bool = True,
    ):
        self.code = code
        self.type = TYPES_BY_PYTHON_TYPE[type]()
        self.choices = choices
        self.name = name
        self.help = help
        self.default = default
        self.required = required
        self.multiple = multiple

    def validate(self, value: typing.Any) -> typing.Any:
        """Validates the provided value against the argument, taking required / default options into account."""

        candidate_value = value if value is not None else self.default
        if candidate_value is None:
            if self.required:
                raise ValueError(f"{self.code} is required")

            return None

        return self.type.validate(candidate_value)

    def parameter_specs(self):
        """Generates specs for this argument, to be provided to the OpenHexa backend."""

        return {
            "type": str(self.type),
            "required": self.required,
            "choices": self.choices,
            "code": self.code,
            "name": self.name,
            "help": self.help,
        }


def argument(
    code: str,
    *,
    type: typing.Union[typing.Type[str], typing.Type[int], typing.Type[bool]],
    name: typing.Optional[str] = None,
    help: typing.Optional[str] = None,
    default: typing.Optional[typing.Any] = None,
    required: bool = True,
    multiple: bool = True,
):
    """Argument decorator."""

    def decorator(fun):
        return FunctionWithArgument(
            fun,
            Argument(
                code,
                type=type,
                name=name,
                help=help,
                default=default,
                required=required,
                multiple=multiple,
            ),
        )

    return decorator


class FunctionWithArgument:
    """This class serves as a wrapper for functions decorated with the @argument decorator."""

    def __init__(self, fun, added_argument: Argument):
        self.fun = fun
        self.argument = added_argument

    def __call__(self, *args, **kwargs):
        return self.fun(*args, **kwargs)

    @property
    def all_arguments(self):
        if isinstance(self.fun, FunctionWithArgument):
            return [self.argument, *self.fun.all_arguments]

        return [self.argument]
