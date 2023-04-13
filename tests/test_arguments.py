import pytest

from openhexa.sdk.pipelines.arguments import String, Integer, Boolean


def test_argument_type_validation():
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
