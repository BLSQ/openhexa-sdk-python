import pytest

from openhexa.sdk.pipelines.arguments import Argument, Boolean, Integer, String


def test_argument_types_validate():
    # String
    string_argument_type = String()
    assert string_argument_type.validate("a string") == "a string"
    with pytest.raises(ValueError):
        string_argument_type.validate(86)

    # Integer
    string_argument_type = Integer()
    assert string_argument_type.validate(99) == 99
    with pytest.raises(ValueError):
        string_argument_type.validate("not an int")

    # Boolean
    string_argument_type = Boolean()
    assert string_argument_type.validate(True) is True
    assert string_argument_type.validate(False) is False
    with pytest.raises(ValueError):
        string_argument_type.validate(86)


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
