from abc import ABC, abstractmethod
from config.enums import LogLevel

class Logger(ABC):
    @abstractmethod
    def log(
        self,
        message: str,
        level: LogLevel = LogLevel.INFO,
    ) -> None:
        ...
    
    def debug(self, message: str) -> None:
        self.log(message, LogLevel.DEBUG)

    def info(self, message: str) -> None:
        self.log(message, LogLevel.INFO)

    def warn(self, message: str) -> None:
        self.log(message, LogLevel.WARN)

    def error(self, message: str) -> None:
        self.log(message, LogLevel.ERROR)