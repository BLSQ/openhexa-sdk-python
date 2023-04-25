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
