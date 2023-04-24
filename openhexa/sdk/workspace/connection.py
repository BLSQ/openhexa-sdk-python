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
    dbname: str
