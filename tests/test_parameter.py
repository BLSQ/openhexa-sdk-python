"""Parameter test module."""

from dataclasses import make_dataclass
from unittest import mock

import pytest

from openhexa.sdk import (
    CustomConnection,
    Dataset,
    DHIS2Connection,
    File,
    GCSConnection,
    IASOConnection,
    PostgreSQLConnection,
    S3Connection,
    workspace,
)
from openhexa.sdk.pipelines.parameter import (
    Boolean,
    CustomConnectionType,
    DatasetType,
    DHIS2ConnectionType,
    FileType,
    Float,
    FunctionWithParameter,
    GCSConnectionType,
    IASOConnectionType,
    Integer,
    InvalidParameterError,
    Parameter,
    ParameterValueError,
    PostgreSQLConnectionType,
    S3ConnectionType,
    StringType,
    parameter,
)
from openhexa.utils import stringcase


def test_parameter_types_normalize():
    """Check normalization or basic types."""
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
    """Sanity checks for basic types validation."""
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
    """Check PostgreSQL connection validation."""
    identifier = "polio-ff3a0d"

    host = "https://172.17.0.1"
    port = 5432
    username = "dhis2"
    password = "dhis2_pwd"
    database_name = "polio"
    data = PostgreSQLConnection(host, port, username, password, database_name)
    with mock.patch.object(workspace, "postgresql_connection", return_value=data):
        postgres_parameter_type = PostgreSQLConnectionType()
        assert postgres_parameter_type.validate(identifier) == PostgreSQLConnection(
            host, port, username, password, database_name
        )
        with pytest.raises(ParameterValueError):
            postgres_parameter_type.validate(86)


def test_validate_dhis2_connection():
    """Check DHIS2 connection validation."""
    identifier = "dhis2-connection-id"

    url = "https://test.dhis2.org/"
    username = "dhis2"
    password = "dhis2_pwd"

    data = DHIS2Connection(url, username, password)
    with mock.patch.object(workspace, "dhis2_connection", return_value=data):
        dhis2_parameter_type = DHIS2ConnectionType()
        assert dhis2_parameter_type.validate(identifier) == DHIS2Connection(url, username, password)
        with pytest.raises(ParameterValueError):
            dhis2_parameter_type.validate(86)


def test_validate_iaso_connection():
    """Check IASO connection validation."""
    identifier = "iaso-connection-id"

    url = "https://test.iaso.org/"
    username = "iaso"
    password = "iaso_pwd"

    data = IASOConnection(url, username, password)
    with mock.patch.object(workspace, "iaso_connection", return_value=data):
        iaso_parameter_type = IASOConnectionType()
        assert iaso_parameter_type.validate(identifier) == IASOConnection(url, username, password)
        with pytest.raises(ParameterValueError):
            iaso_parameter_type.validate(86)


def test_validate_gcs_connection():
    """Check GCS connection validation."""
    identifier = "gcs-connection-id"
    service_account_key = "HqQBxH0BAI3zF7kANUNlGg"
    bucket_name = "test"

    data = GCSConnection(service_account_key, bucket_name)
    with mock.patch.object(workspace, "gcs_connection", return_value=data):
        gcs_parameter_type = GCSConnectionType()
        assert gcs_parameter_type.validate(identifier) == GCSConnection(service_account_key, bucket_name)
        with pytest.raises(ParameterValueError):
            gcs_parameter_type.validate(86)


def test_validate_s3_connection():
    """Check S3 connection validation."""
    identifier = "s3-connection-id"

    secret_access_key = "HqQBxH0BAI3zF7kANUNlGg"
    access_key_id = "84hVntMaMSYP/RSW9ex04w"
    bucket_name = "test"

    data = S3Connection(access_key_id, secret_access_key, bucket_name)
    with mock.patch.object(workspace, "s3_connection", return_value=data):
        s3_parameter_type = S3ConnectionType()
        assert s3_parameter_type.validate(identifier) == S3Connection(access_key_id, secret_access_key, bucket_name)
        with pytest.raises(ParameterValueError):
            s3_parameter_type.validate(86)


def test_validate_custom_connection(monkeypatch):
    """Check Custom connection validation."""
    identifier = "custom-connection-id"

    field_1 = "field_1"
    field_2 = "field_2"

    dataclass = make_dataclass(
        stringcase.pascalcase(identifier),
        [field_1, field_2],
        bases=(CustomConnection,),
        repr=False,
    )
    monkeypatch.setenv("HEXA_SERVER_URL", "http://app.openhexa.test")
    with mock.patch.object(workspace, "get_connection", return_value=dataclass(field_1, field_2)):
        custom_co_type = CustomConnectionType()

        custom_co = custom_co_type.validate(identifier)
        _custom_co = workspace.custom_connection(identifier)

        assert str(custom_co) == str(_custom_co)
        with pytest.raises(ParameterValueError):
            custom_co_type.validate(86)


@mock.patch("openhexa.sdk.workspace.get_dataset")
def test_validate_dataset_parameter(mock_get_dataset):
    """Check Dataset parameter validation."""
    identifier = "dataset-slug"

    dataset = Dataset(id="id", slug=identifier, name="name", description="Description")

    mock_get_dataset.return_value = dataset

    dataset_type = DatasetType()

    assert dataset_type.validate(identifier) == dataset
    with pytest.raises(ParameterValueError):
        dataset_type.validate(86)


@mock.patch("openhexa.sdk.workspace.get_file")
def test_validate_file_parameter(mock_get_file):
    """Check File parameter validation."""
    file = File(name="test.csv", path="my_folder/test.csv", size=1024, type="file")
    mock_get_file.return_value = file

    file_type = FileType()

    assert file_type.validate("test.csv") == file
    # Fails when not a string
    with pytest.raises(ParameterValueError):
        file_type.validate(86)


def test_parameter_init():
    """Sanity checks for parameter initialization."""
    # Wrong type
    with pytest.raises(InvalidParameterError):
        Parameter("arg", type="string")  # NOQA

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
    with pytest.raises(InvalidParameterError):
        Parameter("arg", type=str, choices=["foo", "bar"], default="Bar")


def test_parameter_validate_single():
    """Base check for single-value validation."""
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
    """Test multiple values validation rules."""
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
    parameter_4 = Parameter("arg4", type=str, default=["ab", "ef"], choices=["ab", "cd", "ef"], multiple=True)
    assert parameter_4.validate(["ab"]) == ["ab"]
    assert parameter_4.validate(["ab", "cd"]) == ["ab", "cd"]
    with pytest.raises(ParameterValueError):
        parameter_4.validate(["xy"])
    with pytest.raises(ParameterValueError):
        parameter_4.validate(["ab", "xy"])


def test_parameter_decorator():
    """Ensure that the @parameter decorator behaves as expected (options and defaults)."""

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
