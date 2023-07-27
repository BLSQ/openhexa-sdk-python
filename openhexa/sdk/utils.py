import enum
import os


class Environments(enum.Enum):
    LOCAL_PIPELINE = "LOCAL_PIPELINE"
    CLOUD_PIPELINE = "CLOUD_PIPELINE"
    CLOUD_JUPYTER = "CLOUD_JUPYTER"
    STANDALONE = "STANDALONE"


def get_environment():
    env = os.environ.get("HEXA_ENVIRONMENT", "STANDALONE").upper()
    if env not in Environments.__members__:
        raise ValueError(f"Invalid environment: {env}")
    return Environments[env]
