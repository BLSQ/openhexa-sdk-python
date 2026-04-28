"""Parameter type classes for pipeline parameters."""

import typing

from openhexa.sdk.datasets import Dataset
from openhexa.sdk.files import File
from openhexa.sdk.pipelines.exceptions import InvalidParameterError, ParameterValueError
from openhexa.sdk.workspaces import workspace
from openhexa.sdk.workspaces.connection import (
    Connection,
    CustomConnection,
    DHIS2Connection,
    GCSConnection,
    IASOConnection,
    PostgreSQLConnection,
    S3Connection,
)
from openhexa.sdk.workspaces.current_workspace import ConnectionDoesNotExist


class ParameterType:
    """Base class for parameter types. Those parameter types are used when using the @parameter decorator."""

    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        raise NotImplementedError

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        raise NotImplementedError

    @property
    def accepts_choices(self) -> bool:
        """Return True only if the parameter type supports the "choices" optional argument."""
        return True

    @property
    def accepts_multiple(self) -> bool:
        """Return True only if the parameter type supports multiple values."""
        return True

    @staticmethod
    def normalize(value: typing.Any) -> typing.Any:
        """If appropriate, subclasses can override this method to normalize empty values to None.

        This can be used to handle empty values and normalize them to None, or to perform type conversions, allowing us
        to allow multiple input types but still normalize everything to a single type.
        """
        return value

    def validate(self, value: typing.Any | None) -> typing.Any | None:
        """Validate the provided value for this type."""
        if not isinstance(value, self.expected_type):
            raise ParameterValueError(
                f"Invalid type for value {value} (expected {self.expected_type}, got {type(value)})"
            )
        return value

    def validate_default(self, value: typing.Any | None):
        """Validate the default value configured for this type."""
        self.validate(value)

    def __str__(self) -> str:
        """Cast parameter as string."""
        return str(self.expected_type)


class StringType(ParameterType):
    """Type class for string parameters."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "str"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return str

    @staticmethod
    def normalize(value: typing.Any) -> str | None:
        """Strip leading and trailing whitespaces and convert empty strings to None."""
        if isinstance(value, str):
            normalized_value = value.strip()
        else:
            normalized_value = value

        if normalized_value == "":
            return None

        return normalized_value

    def validate_default(self, value: typing.Any | None):
        """Validate the default value configured for this type."""
        if value == "":
            raise ParameterValueError("Empty values are not accepted.")

        super().validate_default(value)


class Boolean(ParameterType):
    """Type class for boolean parameters."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "bool"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return bool

    @property
    def accepts_choices(self) -> bool:
        """Return a type string for the specs that are sent to the backend."""
        return False

    @property
    def accepts_multiple(self) -> bool:
        """Return a type string for the specs that are sent to the backend."""
        return False


class Integer(ParameterType):
    """Type class for integer parameters."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "int"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return int


class Float(ParameterType):
    """Type class for float parameters."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "float"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return float

    @staticmethod
    def normalize(value: typing.Any) -> typing.Any:
        """Normalize int values to float values if appropriate."""
        if isinstance(value, int):
            return float(value)

        return value


class ConnectionParameterType(ParameterType):
    """Abstract base class for connection parameter type classes."""

    @property
    def accepts_choices(self) -> bool:
        """Return True only if the parameter type supports the "choice values."""
        return False

    @property
    def accepts_multiple(self) -> bool:
        """Return True only if the parameter type supports multiple values."""
        return False

    def validate_default(self, value: typing.Any | None):
        """Validate the default value configured for this type."""
        if value is None:
            return

        if not isinstance(value, str):
            raise InvalidParameterError("Default value for connection parameter type should be string.")
        elif value == "":
            raise ParameterValueError("Empty values are not accepted.")

    def validate(self, value: typing.Any | None) -> Connection:
        """Validate the provided value for this type."""
        if not isinstance(value, str):
            raise ParameterValueError(f"Invalid type for value {value} (expected {str}, got {type(value)})")

        try:
            return self.to_connection(value)
        except ConnectionDoesNotExist as e:
            raise ParameterValueError(str(e))

    def to_connection(self, value: str) -> Connection:
        """Build a connection instance from the provided value (which should be a connection identifier)."""
        raise NotImplementedError


class PostgreSQLConnectionType(ConnectionParameterType):
    """Type class for PostgreSQL connections."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "postgresql"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return PostgreSQLConnection

    def to_connection(self, value: str) -> PostgreSQLConnection:
        """Build a PostgreSQL connection instance from the provided value (which should be a connection identifier)."""
        return workspace.postgresql_connection(value)


class S3ConnectionType(ConnectionParameterType):
    """Type class for S3 connections."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "s3"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return S3Connection

    def to_connection(self, value: str) -> S3Connection:
        """Build a S3 connection instance from the provided value (which should be a connection identifier)."""
        return workspace.s3_connection(value)


class GCSConnectionType(ConnectionParameterType):
    """Type class for GCS connections."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "gcs"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return GCSConnection

    def to_connection(self, value: str) -> GCSConnection:
        """Build a GCS connection instance from the provided value (which should be a connection identifier)."""
        return workspace.gcs_connection(value)


class DHIS2ConnectionType(ConnectionParameterType):
    """Type class for DHIS2 connections."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "dhis2"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return DHIS2Connection

    def to_connection(self, value: str) -> DHIS2Connection:
        """Build a DHIS2 connection instance from the provided value (which should be a connection identifier)."""
        return workspace.dhis2_connection(value)


class IASOConnectionType(ConnectionParameterType):
    """Type class for IASO connections."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "iaso"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return IASOConnection

    def to_connection(self, value: str) -> IASOConnection:
        """Build a IASO connection instance from the provided value (which should be a connection identifier)."""
        return workspace.iaso_connection(value)


class CustomConnectionType(ConnectionParameterType):
    """Type class for custom connections."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "custom"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return CustomConnection

    def to_connection(self, value: str) -> CustomConnection:
        """Build a custom connection instance from the provided value (which should be a connection identifier)."""
        return workspace.custom_connection(value)


class DatasetType(ParameterType):
    """Type class for dataset parameter."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "dataset"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return Dataset

    def validate_default(self, value: typing.Any | None):
        """Validate the default value configured for this type."""
        if value is None:
            return

        if not isinstance(value, str):
            raise InvalidParameterError("Default value for dataset parameter type should be string.")
        elif value == "":
            raise ParameterValueError("Empty values are not accepted.")

    def validate(self, value: typing.Any | None) -> Dataset:
        """Validate the provided value for this type."""
        if not isinstance(value, str):
            raise ParameterValueError(f"Invalid type for value {value} (expected {str}, got {type(value)})")

        try:
            return workspace.get_dataset(value)
        except ValueError as e:
            raise ParameterValueError(str(e))


class FileType(ParameterType):
    """Type class for file parameter."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "file"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return File

    @property
    def accepts_multiple(self) -> bool:
        """Only allow single file selection."""
        return False

    @property
    def accepts_choices(self) -> bool:
        """Don't allow choices for file."""
        return False

    def validate_default(self, value: typing.Any | None):
        """Validate the default value configured for this type."""
        if value is None:
            return

        if not isinstance(value, str):
            raise InvalidParameterError("Default value for file parameter type should be string.")
        elif value == "":
            raise ParameterValueError("Empty values are not accepted.")

    def validate(self, value: typing.Any | None) -> File:
        """Validate the provided value for this type."""
        if not isinstance(value, str):
            raise ParameterValueError(f"Invalid type for value {value} (expected {str}, got {type(value)})")

        try:
            return workspace.get_file(value)
        except ValueError as e:
            raise ParameterValueError(str(e))


class Secret(str):
    """Marker type for secret/password pipeline parameters.

    Use as the ``type`` argument of the ``@parameter`` decorator to indicate that the parameter value is sensitive
    and should be hidden in the OpenHEXA web interface. The pipeline function will receive the value as a plain
    ``str`` at runtime.

    Example::

        @parameter("iaso_token", type=Secret, name="IASO token", required=True)
        @pipeline("my-pipeline")
        def my_pipeline(iaso_token: str):
            ...
    """

    pass


class SecretType(ParameterType):
    """Type class for secret/password string parameters. Values are treated as plain strings at runtime."""

    @property
    def spec_type(self) -> str:
        """Return a type string for the specs that are sent to the backend."""
        return "secret"

    @property
    def expected_type(self) -> type:
        """Returns the python type expected for values."""
        return Secret

    @property
    def accepts_choices(self) -> bool:
        """Secrets don't support choices."""
        return False

    @property
    def accepts_multiple(self) -> bool:
        """Secrets don't support multiple values."""
        return False

    @staticmethod
    def normalize(value: typing.Any) -> Secret | None:
        """Strip whitespace, convert empty strings to None, and wrap as Secret."""
        if isinstance(value, str):
            normalized_value = value.strip()
        else:
            normalized_value = value

        if normalized_value == "":
            return None

        if isinstance(normalized_value, str):
            return Secret(normalized_value)

        return normalized_value

    def validate_default(self, value: typing.Any | None):
        """Validate the default value configured for this type."""
        if value == "":
            raise ParameterValueError("Empty values are not accepted.")

        super().validate_default(value)


TYPES_BY_PYTHON_TYPE = {
    "str": StringType,
    "bool": Boolean,
    "int": Integer,
    "float": Float,
    "Secret": SecretType,
    "DHIS2Connection": DHIS2ConnectionType,
    "PostgreSQLConnection": PostgreSQLConnectionType,
    "IASOConnection": IASOConnectionType,
    "S3Connection": S3ConnectionType,
    "GCSConnection": GCSConnectionType,
    "CustomConnection": CustomConnectionType,
    "Dataset": DatasetType,
    "File": FileType,
}
