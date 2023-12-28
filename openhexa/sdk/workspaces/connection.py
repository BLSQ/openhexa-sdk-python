"""Connection test module."""

import dataclasses


@dataclasses.dataclass
class DHIS2Connection:
    """DHIS2 connection.

    See https://docs.dhis2.org/ for more information.
    """

    url: str
    username: str
    password: str

    def __repr__(self):
        return f"DHIS2Connection(url='{self.url}', username='{self.username}')"


@dataclasses.dataclass
class PostgreSQLConnection:
    """PostgreSQL database connection.

    See https://www.postgresql.org/docs/ for more information.
    """

    host: str
    port: int
    username: str
    password: str
    database_name: str

    def __repr__(self):
        return f"PostgreSQLConnection(host='{self.host}', port='{self.port}', username='{self.username}', database_name='{self.database_name}')"

    @property
    def url(self):
        return f"postgresql://{self.username}:{self.password}" f"@{self.host}:{self.port}/{self.database_name}"


@dataclasses.dataclass
class S3Connection:
    """AWS S3 connection.

    See https://docs.aws.amazon.com/s3/ for more information.
    """

    access_key_id: str
    secret_access_key: str
    bucket_name: str

    def __repr__(self):
        return f"S3Connection(bucket_name='{self.bucket_name}')"


@dataclasses.dataclass
class GCSConnection:
    """Google Cloud Storage connection.

    See https://cloud.google.com/storage/docs for more information.
    """

    service_account_key: str
    bucket_name: str

    def __repr__(self):
        return f"GCSConnection(bucket_name='{self.bucket_name}')"


@dataclasses.dataclass
class IASOConnection:
    """IASO connection.

    See https://github.com/BLSQ/iaso for more information.
    """

    url: str
    username: str
    password: str

    def __repr__(self):
        return f"IASOConnection(url='{self.url}', username='{self.username}')"
