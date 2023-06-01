import enum
import os


class Environments(enum.Enum):
    LOCAL = "LOCAL"
    PIPELINE = "PIPELINE"
    DOCKER = "DOCKER"
    JUPYTER = "JUPYTER"


def get_environment():
    env = os.environ.get("HEXA_ENVIRONMENT", "LOCAL").upper()
    if env not in Environments.__members__:
        raise ValueError(f"Invalid environment: {env}")
    return Environments[env]
