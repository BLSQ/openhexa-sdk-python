import pytest

from openhexa.sdk.pipelines.arguments import (
    Argument,
    ArgumentValueError,
    Boolean,
    Float,
    Integer,
    InvalidArgumentError,
    String,
)


def test_argument_types_validate():
    # String
    string_argument_type = String()
    assert string_argument_type.validate("a string") == "a string"
    with pytest.raises(ArgumentValueError):
        string_argument_type.validate(86)

    # Integer
    integer_argument_type = Integer()
    assert integer_argument_type.validate(99) == 99
    with pytest.raises(ArgumentValueError):
        integer_argument_type.validate("not an int")

    # Float
    float_argument_type = Float()
    assert float_argument_type.validate(3.14) == 3.14
    assert float_argument_type.validate(3) == 3.0
    with pytest.raises(ArgumentValueError):
        float_argument_type.validate("3.14")

    # Boolean
    boolean_argument_type = Boolean()
    assert boolean_argument_type.validate(True) is True
    assert boolean_argument_type.validate(False) is False
    with pytest.raises(ArgumentValueError):
        boolean_argument_type.validate(86)


def test_argument_init():
    # Wrong type
    with pytest.raises(InvalidArgumentError):
        Argument("arg", type="string")

    # Empty choices
    with pytest.raises(InvalidArgumentError):
        Argument("arg", type=str, choices=[1, 2, 3])


def test_argument_validate():
    # required is True by default
    argument_1 = Argument("arg1", type=str)
    assert argument_1.validate("a valid string") == "a valid string"
    with pytest.raises(ValueError):
        argument_1.validate(None)

    # still required, but a default is provided
    argument_2 = Argument("arg2", type=int, default=3)
    assert argument_2.validate(None) == 3

    # not required, no default
    argument_3 = Argument("arg3", type=bool, required=False)
    assert argument_3.validate(None) is None


def test_argument_parameters_specs():
    # required is True by default
    argument = Argument("arg", type=str)

    assert argument.parameter_specs() == {
        "code": "arg",
        "name": None,
        "type": "str",
        "required": True,
        "choices": None,
        "help": None,
    }
