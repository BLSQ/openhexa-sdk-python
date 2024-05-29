"""Connection test module."""

import dataclasses


@dataclasses.dataclass
class Connection:
    """Abstract base class for connections."""

    pass


@dataclasses.dataclass
class DHIS2Connection(Connection):
    """DHIS2 connection.

    See https://docs.dhis2.org/ for more information.
    """

    url: str
    username: str
    password: str

    def __repr__(self):
        """Safe representation of the DHIS2 connection (no credentials)."""
        return f"DHIS2Connection(url='{self.url}', username='{self.username}')"


@dataclasses.dataclass
class PostgreSQLConnection(Connection):
    """PostgreSQL database connection.

    See https://www.postgresql.org/docs/ for more information.
    """

    host: str
    port: int
    username: str
    password: str
    database_name: str

    def __repr__(self):
        """Safe representation of the PostgreSQL connection (no credentials)."""
        return (
            f"PostgreSQLConnection(host='{self.host}', port='{self.port}', username='{self.username}', "
            f"database_name='{self.database_name}')"
        )

    @property
    def url(self):
        """Provide a URL to the PostgreSQL database.

        The URL follows the official PostgreSQL specification.
        (See https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING for more information)
        """
        return f"postgresql://{self.username}:{self.password}" f"@{self.host}:{self.port}/{self.database_name}"


@dataclasses.dataclass
class S3Connection(Connection):
    """AWS S3 connection.

    See https://docs.aws.amazon.com/s3/ for more information.
    """

    access_key_id: str
    secret_access_key: str
    bucket_name: str

    def __repr__(self):
        """Safe representation of the S3 connection (no credentials)."""
        return f"S3Connection(bucket_name='{self.bucket_name}')"


@dataclasses.dataclass
class GCSConnection(Connection):
    """Google Cloud Storage connection.

    See https://cloud.google.com/storage/docs for more information.
    """

    service_account_key: str
    bucket_name: str

    def __repr__(self):
        """Safe representation of the GCS connection (no credentials)."""
        return f"GCSConnection(bucket_name='{self.bucket_name}')"


@dataclasses.dataclass
class CustomConnection(Connection):
    """Marker class for custom connections.

    The actual class will be built dynamically through the Workspace.custom_connection() method.
    """

    def __repr__(self):
        """Safe representation of the custom connection (no credentials)."""
        return f"CustomConnection(name='{self.__class__.__name__.lower()}')"


@dataclasses.dataclass
class IASOConnection:
    """IASO connection.

    See https://github.com/BLSQ/iaso for more information.
    """

    url: str
    username: str
    password: str

    def __repr__(self):
        """Safe representation of the IASO connection (no credentials)."""
        return f"IASOConnection(url='{self.url}', username='{self.username}')"


ConnectionClasses = {
    "S3": S3Connection,
    "GCS": GCSConnection,
    "POSTGRESQL": PostgreSQLConnection,
    "DHIS2": DHIS2Connection,
    "IASO": IASOConnection,
    "CUSTOM": CustomConnection,
}
