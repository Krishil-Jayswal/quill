from enum import StrEnum

class LogLevel(StrEnum):
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"

class LoggerBackendType(StrEnum):
    KAFKA = "kafka"
    CONSOLE = "console"