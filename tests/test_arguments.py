import pytest

from openhexa.sdk.pipelines.arguments import (
    Argument,
    ArgumentValueError,
    Boolean,
    Float,
    FunctionWithArgument,
    Integer,
    InvalidArgumentError,
    String,
    argument,
)


def test_argument_types_normalize():
    # String
    string_argument_type = String()
    assert string_argument_type.normalize("a string") == "a string"
    assert string_argument_type.normalize(" a string ") == "a string"
    assert string_argument_type.normalize("") is None
    assert string_argument_type.normalize(" ") is None

    # Integer
    integer_argument_type = Integer()
    assert integer_argument_type.normalize(99) == 99
    assert integer_argument_type.normalize("abc") == "abc"

    # Float
    float_argument_type = Float()
    assert float_argument_type.normalize(3.14) == 3.14
    assert float_argument_type.normalize(3) == 3.0

    # Boolean
    boolean_argument_type = Boolean()
    assert boolean_argument_type.normalize(True) is True
    assert boolean_argument_type.normalize(False) is False
    assert boolean_argument_type.normalize(3) == 3


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
        Argument("arg", type=str, choices=[])

    # Invalid choices
    with pytest.raises(InvalidArgumentError):
        Argument("arg", type=str, choices=[1, 2, 3])

    # Boolean can't have choices
    with pytest.raises(InvalidArgumentError):
        Argument("arg", type=bool, choices=[True, False])

    # Boolean can't be multiple
    with pytest.raises(InvalidArgumentError):
        Argument("arg", type=bool, multiple=True)

    # Invalid defaults
    with pytest.raises(InvalidArgumentError):
        Argument("arg", type=bool, default=3)
    with pytest.raises(InvalidArgumentError):
        Argument("arg", type=str, default=[1, 2], multiple=True)
    with pytest.raises(InvalidArgumentError):
        Argument("arg", type=str, default="yolo", multiple=True)
    with pytest.raises(InvalidArgumentError):
        Argument("arg", type=str, default="")
    with pytest.raises(InvalidArgumentError):
        Argument("arg", type=str, default=[""], multiple=True)


def test_argument_validate_single():
    # required is True by default
    argument_1 = Argument("arg1", type=str)
    assert argument_1.validate("a valid string") == "a valid string"
    with pytest.raises(ArgumentValueError):
        argument_1.validate(None)
    with pytest.raises(ArgumentValueError):
        argument_1.validate("")

    # still required, but a default is provided
    argument_2 = Argument("arg2", type=int, default=3)
    assert argument_2.validate(None) == 3

    # not required, no default
    argument_3 = Argument("arg3", type=bool, required=False)
    assert argument_3.validate(None) is None

    # choices
    argument_4 = Argument("arg4", type=str, choices=["ab", "cd"])
    assert argument_4.validate("ab") == "ab"
    with pytest.raises(ArgumentValueError):
        argument_4.validate("xy")


def test_argument_validate_multiple():
    # required is True by default
    argument_1 = Argument("arg1", type=str, multiple=True)
    assert argument_1.validate(["Valid string", "Another valid string"]) == [
        "Valid string",
        "Another valid string",
    ]
    with pytest.raises(ArgumentValueError):
        argument_1.validate(None)
    with pytest.raises(ArgumentValueError):
        argument_1.validate([])
    with pytest.raises(ArgumentValueError):
        argument_1.validate(["", ""])

    # still required, but a default is provided
    argument_2 = Argument("arg2", type=int, multiple=True, default=[2, 3])
    assert argument_2.validate(None) == [2, 3]

    # not required, no default
    argument_3 = Argument("arg3", type=int, required=False, multiple=True)
    assert argument_3.validate(None) == []
    assert argument_3.validate([]) == []

    # choices
    argument_4 = Argument("arg4", type=str, choices=["ab", "cd"], multiple=True)
    assert argument_4.validate(["ab"]) == ["ab"]
    assert argument_4.validate(["ab", "cd"]) == ["ab", "cd"]
    with pytest.raises(ArgumentValueError):
        argument_4.validate(["xy"])
    with pytest.raises(ArgumentValueError):
        argument_4.validate(["ab", "xy"])


def test_argument_parameters_specs():
    # required is True by default
    an_argument = Argument("arg1", type=str, default="yep")
    another_argument = Argument(
        "arg2",
        type=str,
        name="Arg 2",
        help="Help 2",
        choices=["ab", "cd"],
        required=False,
        multiple=True,
    )

    assert an_argument.parameter_spec() == {
        "code": "arg1",
        "name": None,
        "type": "str",
        "required": True,
        "choices": None,
        "help": None,
        "multiple": False,
        "default": "yep",
    }

    assert another_argument.parameter_spec() == {
        "code": "arg2",
        "name": "Arg 2",
        "type": "str",
        "required": False,
        "choices": ["ab", "cd"],
        "help": "Help 2",
        "multiple": True,
        "default": None,
    }


def test_argument_decorator():
    @argument("arg1", type=int)
    @argument(
        "arg2",
        type=str,
        name="Arg 2",
        help="Help 2",
        default=["yo"],
        required=False,
        multiple=True,
    )
    def a_function():
        pass

    assert isinstance(a_function, FunctionWithArgument)
    function_arguments = a_function.get_all_arguments()
    assert len(function_arguments) == 2
    assert all(isinstance(a, Argument) for a in function_arguments)

    assert function_arguments[0].code == "arg1"
    assert isinstance(function_arguments[0].type, Integer)
    assert function_arguments[0].name is None
    assert function_arguments[0].help is None
    assert function_arguments[0].default is None
    assert function_arguments[0].required is True
    assert function_arguments[0].multiple is False

    assert function_arguments[1].code == "arg2"
    assert isinstance(function_arguments[1].type, String)
    assert function_arguments[1].name == "Arg 2"
    assert function_arguments[1].help == "Help 2"
    assert function_arguments[1].default == ["yo"]
    assert function_arguments[1].required is False
    assert function_arguments[1].multiple is True
