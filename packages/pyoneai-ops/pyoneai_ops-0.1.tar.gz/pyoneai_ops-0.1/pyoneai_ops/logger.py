import logging
import logging.handlers
from dataclasses import dataclass
from enum import IntEnum
from importlib.resources import files
from pathlib import Path
from typing import Any, Literal, Self

import yaml


class _OneLogLevels(IntEnum):
    ERROR = 0
    WARNING = 1
    INFO = 2
    DEBUG = 3
    DDEBUG = 4
    DDDEBUG = 5


@dataclass(frozen=True)
class LogConfig:
    system: Literal["std", "file", "syslog"] = "std"
    debug_level: _OneLogLevels = _OneLogLevels.INFO

    @property
    def python_log_level(self) -> int:
        match self.debug_level:
            case _OneLogLevels.ERROR:
                return logging.ERROR
            case _OneLogLevels.WARNING:
                return logging.WARNING
            case _OneLogLevels.INFO:
                return logging.INFO
            case (
                _OneLogLevels.DEBUG
                | _OneLogLevels.DDEBUG
                | _OneLogLevels.DDDEBUG
            ):
                return logging.DEBUG
            case _:
                raise NotImplementedError


class LoggingConfig:

    def __init__(self) -> None:
        self.config = LoggingConfig.get_default_config()

    @classmethod
    def get_default_config(cls) -> dict[str, Any]:
        return yaml.safe_load(
            files("pyoneai_ops")
            .joinpath("resources", "logging.yaml")
            .open("r")
        )

    def add_filehandler(self, filename: str | Path) -> Self:
        filename = Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)
        self.config["handlers"]["file"] = {
            "formatter": "access",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": filename,
            "maxBytes": 1024 * 1024,
        }
        self.config["loggers"]["uvicorn.access"]["handlers"].append("file")
        return self

    def add_stdhandler(self) -> Self:
        self.config["handlers"]["std"] = {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        }
        self.config["loggers"]["uvicorn.access"]["handlers"].append("std")
        return self


def get_logger_config(
    filename: str | Path, log_config: LogConfig = LogConfig()
) -> dict[str, Any]:
    """Configure the logger for Insight component."""
    conf = LoggingConfig()
    if log_config.system == "file":
        log_file = Path(f"/var/log/one/{filename}")
        conf.add_filehandler(log_file)
    elif log_config.system == "std":
        conf.add_stdhandler()
    else:
        raise NotImplementedError

    return conf.config
