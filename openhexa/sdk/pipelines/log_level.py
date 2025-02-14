"""Log levels for the pipeline runs."""

from enum import IntEnum


class LogLevel(IntEnum):
    """
    Enum representing different log levels.

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

    @classmethod
    def parse_log_level(cls, value) -> "LogLevel":
        """Parse a log level from a string or integer."""
        if isinstance(value, int) and 0 <= value <= 4:
            return LogLevel(value)
        if isinstance(value, str):
            if value.isdigit():
                return cls.parse_log_level(int(value))
            value = value.upper()
            if hasattr(cls, value):
                return getattr(cls, value)
        return cls.INFO
