"""Priority log levels for the pipeline runs."""
from enum import IntEnum


class Priority(IntEnum):
    """
    Enum representing different priority log levels.

     - Attributes:
        DEBUG (int): Debug level, value 0.
        INFO (int): Info level, value 1.
        WARNING (int): Warning level, value 2.
        ERROR (int): Error level, value 3.
        CRITICAL (int): Critical level, value 4.

    """

    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
