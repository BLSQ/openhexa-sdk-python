import pytest

from openhexa.sdk.pipelines.parameter import (
    Boolean,
    Float,
    FunctionWithParameter,
    Integer,
    InvalidParameterError,
    Parameter,
    ParameterValueError,
    String,
    parameter,
)


def test_parameter_types_normalize():
    # String
    string_parameter_type = String()
    assert string_parameter_type.normalize("a string") == "a string"
    assert string_parameter_type.normalize(" a string ") == "a string"
    assert string_parameter_type.normalize("") is None
    assert string_parameter_type.normalize(" ") is None

    # Integer
    integer_parameter_type = Integer()
    assert integer_parameter_type.normalize(99) == 99
    assert integer_parameter_type.normalize("abc") == "abc"

    # Float
    float_parameter_type = Float()
    assert float_parameter_type.normalize(3.14) == 3.14
    assert float_parameter_type.normalize(3) == 3.0

    # Boolean
    boolean_parameter_type = Boolean()
    assert boolean_parameter_type.normalize(True) is True
    assert boolean_parameter_type.normalize(False) is False
    assert boolean_parameter_type.normalize(3) == 3


def test_parameter_types_validate():
    # String
    string_parameter_type = String()
    assert string_parameter_type.validate("a string") == "a string"
    with pytest.raises(ParameterValueError):
        string_parameter_type.validate(86)

    # Integer
    integer_parameter_type = Integer()
    assert integer_parameter_type.validate(99) == 99
    with pytest.raises(ParameterValueError):
        integer_parameter_type.validate("not an int")

    # Float
    float_parameter_type = Float()
    assert float_parameter_type.validate(3.14) == 3.14
    with pytest.raises(ParameterValueError):
        float_parameter_type.validate("3.14")

    # Boolean
    boolean_parameter_type = Boolean()
    assert boolean_parameter_type.validate(True) is True
    assert boolean_parameter_type.validate(False) is False
    with pytest.raises(ParameterValueError):
        boolean_parameter_type.validate(86)


def test_parameter_init():
    # Wrong type
    with pytest.raises(InvalidParameterError):
        Parameter("arg", type="string")

    # Wrong code
    with pytest.raises(InvalidParameterError):
        Parameter("-123", type=str)
    with pytest.raises(InvalidParameterError):
        Parameter("Abc", type=str)
    with pytest.raises(InvalidParameterError):
        Parameter("0_z", type=str)

    # Empty choices
    with pytest.raises(InvalidParameterError):
        Parameter("arg", type=str, choices=[])

    # Invalid choices
    with pytest.raises(InvalidParameterError):
        Parameter("arg", type=str, choices=[1, 2, 3])

    # Boolean can't have choices
    with pytest.raises(InvalidParameterError):
        Parameter("arg", type=bool, choices=[True, False])

    # Boolean can't be multiple
    with pytest.raises(InvalidParameterError):
        Parameter("arg", type=bool, multiple=True)

    # Invalid defaults
    with pytest.raises(InvalidParameterError):
        Parameter("arg", type=bool, default=3)
    with pytest.raises(InvalidParameterError):
        Parameter("arg", type=str, default=[1, 2], multiple=True)
    with pytest.raises(InvalidParameterError):
        Parameter("arg", type=str, default="yolo", multiple=True)
    with pytest.raises(InvalidParameterError):
        Parameter("arg", type=str, default="")
    with pytest.raises(InvalidParameterError):
        Parameter("arg", type=str, default=[""], multiple=True)


def test_parameter_validate_single():
    # required is True by default
    parameter_1 = Parameter("arg1", type=str)
    assert parameter_1.validate("a valid string") == "a valid string"
    with pytest.raises(ParameterValueError):
        parameter_1.validate(None)
    with pytest.raises(ParameterValueError):
        parameter_1.validate("")

    # still required, but a default is provided
    parameter_2 = Parameter("arg2", type=int, default=3)
    assert parameter_2.validate(None) == 3

    # not required, no default
    parameter_3 = Parameter("arg3", type=bool, required=False)
    assert parameter_3.validate(None) is None

    # choices
    parameter_4 = Parameter("arg4", type=str, choices=["ab", "cd"])
    assert parameter_4.validate("ab") == "ab"
    with pytest.raises(ParameterValueError):
        parameter_4.validate("xy")


def test_parameter_validate_multiple():
    # required is True by default
    parameter_1 = Parameter("arg1", type=str, multiple=True)
    assert parameter_1.validate(["Valid string", "Another valid string"]) == [
        "Valid string",
        "Another valid string",
    ]
    with pytest.raises(ParameterValueError):
        parameter_1.validate(None)
    with pytest.raises(ParameterValueError):
        parameter_1.validate([])
    with pytest.raises(ParameterValueError):
        parameter_1.validate(["", ""])

    # still required, but a default is provided
    parameter_2 = Parameter("arg2", type=int, multiple=True, default=[2, 3])
    assert parameter_2.validate(None) == [2, 3]

    # not required, no default
    parameter_3 = Parameter("arg3", type=int, required=False, multiple=True)
    assert parameter_3.validate(None) == []
    assert parameter_3.validate([]) == []

    # choices
    parameter_4 = Parameter("arg4", type=str, choices=["ab", "cd"], multiple=True)
    assert parameter_4.validate(["ab"]) == ["ab"]
    assert parameter_4.validate(["ab", "cd"]) == ["ab", "cd"]
    with pytest.raises(ParameterValueError):
        parameter_4.validate(["xy"])
    with pytest.raises(ParameterValueError):
        parameter_4.validate(["ab", "xy"])


def test_parameter_parameters_spec():
    # required is True by default
    an_parameter = Parameter("arg1", type=str, default="yep")
    another_parameter = Parameter(
        "arg2",
        type=str,
        name="Arg 2",
        help="Help 2",
        choices=["ab", "cd"],
        required=False,
        multiple=True,
    )

    assert an_parameter.parameter_spec() == {
        "code": "arg1",
        "name": None,
        "type": "str",
        "required": True,
        "choices": None,
        "help": None,
        "multiple": False,
        "default": "yep",
    }

    assert another_parameter.parameter_spec() == {
        "code": "arg2",
        "name": "Arg 2",
        "type": "str",
        "required": False,
        "choices": ["ab", "cd"],
        "help": "Help 2",
        "multiple": True,
        "default": None,
    }


def test_parameter_decorator():
    @parameter("arg1", type=int)
    @parameter(
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

    assert isinstance(a_function, FunctionWithParameter)
    function_parameters = a_function.get_all_parameters()
    assert len(function_parameters) == 2
    assert all(isinstance(a, Parameter) for a in function_parameters)

    assert function_parameters[0].code == "arg1"
    assert isinstance(function_parameters[0].type, Integer)
    assert function_parameters[0].name is None
    assert function_parameters[0].help is None
    assert function_parameters[0].default is None
    assert function_parameters[0].required is True
    assert function_parameters[0].multiple is False

    assert function_parameters[1].code == "arg2"
    assert isinstance(function_parameters[1].type, String)
    assert function_parameters[1].name == "Arg 2"
    assert function_parameters[1].help == "Help 2"
    assert function_parameters[1].default == ["yo"]
    assert function_parameters[1].required is False
    assert function_parameters[1].multiple is True
