import dataclasses


@dataclasses.dataclass
class DHIS2Connection:
    url: str
    username: str
    password: str


@dataclasses.dataclass
class PostgreSQLConnection:
    host: str
    port: int
    username: str
    password: str
    database_name: str

    @property
    def url(self):
        return (
            f"postgresql://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database_name}"
        )


@dataclasses.dataclass
class S3Connection:
    access_key_id: str
    secret_access_key: str
    bucket_name: str


@dataclasses.dataclass
class GCSConnection:
    service_account_key: str
    bucket_name: str


@dataclasses.dataclass
class CustomConnection:
    fields: dict
