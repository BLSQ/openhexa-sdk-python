import dataclasses


@dataclasses.dataclass
class DHIS2Connection:
    api_url: str
    username: str
    password: str
