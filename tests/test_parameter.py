import pytest
import os
import stringcase

from openhexa.sdk import (
    DHIS2Connection,
    IASOConnection,
    PostgreSQLConnection,
    GCSConnection,
    S3Connection,
)

from openhexa.sdk.pipelines.parameter import (
    Boolean,
    Float,
    FunctionWithParameter,
    Integer,
    InvalidParameterError,
    Parameter,
    ParameterValueError,
    StringType,
    PostgreSQLConnectionType,
    GCSConnectionType,
    S3ConnectionType,
    IASOConnectionType,
    DHIS2ConnectionType,
    parameter,
)

from unittest import mock


def test_parameter_types_normalize():
    # StringType
    string_parameter_type = StringType()
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
    # StringType
    string_parameter_type = StringType()
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


def test_validate_postgres_connection():
    identifier = "polio-ff3a0d"
    env_variable_prefix = stringcase.constcase(identifier)
    host = "https://172.17.0.1"
    port = "5432"
    username = "dhis2"
    password = "dhis2_pwd"
    database_name = "polio"
    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_HOST": host,
            f"{env_variable_prefix}_USERNAME": username,
            f"{env_variable_prefix}_PASSWORD": password,
            f"{env_variable_prefix}_PORT": port,
            f"{env_variable_prefix}_DB_NAME": database_name,
        },
    ):
        postgres_parameter_type = PostgreSQLConnectionType()
        assert postgres_parameter_type.validate(identifier) == PostgreSQLConnection(
            host, int(port), username, password, database_name
        )
        with pytest.raises(ParameterValueError):
            postgres_parameter_type.validate(86)


def test_validate_dhis2_connection():
    identifier = "dhis2-connection-id"
    env_variable_prefix = stringcase.constcase(identifier)
    url = "https://test.dhis2.org/"
    username = "dhis2"
    password = "dhis2_pwd"

    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_URL": url,
            f"{env_variable_prefix}_USERNAME": username,
            f"{env_variable_prefix}_PASSWORD": password,
        },
    ):
        dhsi2_parameter_type = DHIS2ConnectionType()
        assert dhsi2_parameter_type.validate(identifier) == DHIS2Connection(url, username, password)
        with pytest.raises(ParameterValueError):
            dhsi2_parameter_type.validate(86)


def test_validate_iaso_connection():
    identifier = "iaso-connection-id"
    env_variable_prefix = stringcase.constcase(identifier)
    url = "https://test.iaso.org/"
    username = "iaso"
    password = "iaso_pwd"

    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_URL": url,
            f"{env_variable_prefix}_USERNAME": username,
            f"{env_variable_prefix}_PASSWORD": password,
        },
    ):
        iaso_parameter_type = IASOConnectionType()
        assert iaso_parameter_type.validate(identifier) == IASOConnection(url, username, password)
        with pytest.raises(ParameterValueError):
            iaso_parameter_type.validate(86)


def test_validate_gcs_connection():
    identifier = "gcs-connection-id"
    env_variable_prefix = stringcase.constcase(identifier)
    service_account_key = "HqQBxH0BAI3zF7kANUNlGg"
    bucket_name = "test"

    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_SERVICE_ACCOUNT_KEY": service_account_key,
            f"{env_variable_prefix}_BUCKET_NAME": bucket_name,
        },
    ):
        gcs_parameter_type = GCSConnectionType()
        assert gcs_parameter_type.validate(identifier) == GCSConnection(service_account_key, bucket_name)
        with pytest.raises(ParameterValueError):
            gcs_parameter_type.validate(86)


def test_validate_s3_connection():
    identifier = "s3-connection-id"
    env_variable_prefix = stringcase.constcase(identifier)
    secret_access_key = "HqQBxH0BAI3zF7kANUNlGg"
    access_key_id = "84hVntMaMSYP/RSW9ex04w"
    bucket_name = "test"

    with mock.patch.dict(
        os.environ,
        {
            f"{env_variable_prefix}_SECRET_ACCESS_KEY": secret_access_key,
            f"{env_variable_prefix}_ACCESS_KEY_ID": access_key_id,
            f"{env_variable_prefix}_BUCKET_NAME": bucket_name,
        },
    ):
        s3_parameter_type = S3ConnectionType()
        assert s3_parameter_type.validate(identifier) == S3Connection(access_key_id, secret_access_key, bucket_name)
        with pytest.raises(ParameterValueError):
            s3_parameter_type.validate(86)


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
    assert isinstance(function_parameters[1].type, StringType)
    assert function_parameters[1].name == "Arg 2"
    assert function_parameters[1].help == "Help 2"
    assert function_parameters[1].default == ["yo"]
    assert function_parameters[1].required is False
    assert function_parameters[1].multiple is True
