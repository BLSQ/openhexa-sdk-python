import dataclasses


@dataclasses.dataclass
class DHIS2Connection:
    url: str
    username: str
    password: str

    def __repr__(self):
        return f"DHIS2Connection(url='{self.url}', username='{self.username}')"


@dataclasses.dataclass
class PostgreSQLConnection:
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
    access_key_id: str
    secret_access_key: str
    bucket_name: str

    def __repr__(self):
        return f"S3Connection(bucket_name='{self.bucket_name}')"


@dataclasses.dataclass
class GCSConnection:
    service_account_key: str
    bucket_name: str

    def __repr__(self):
        return f"GCSConnection(bucket_name='{self.bucket_name}')"


@dataclasses.dataclass
class IASOConnection:
    url: str
    username: str
    password: str

    def __repr__(self):
        return f"IASOConnection(url='{self.url}', username='{self.username}')"
