__all__ = (
    "Config",
    "get_config",
)
import os
from dataclasses import dataclass
from functools import lru_cache

import yaml

from ...logger import LogConfig

SCHEDULER_CONF_PATH: str = os.environ.get(
    "PYONEAIOPS_SCHEDULER_CONF_PATH", "/etc/one/aiops/scheduler.conf"
)


@dataclass
class Config:
    host: str
    port: int
    version: str
    planexecutor_endpoint: str
    log: LogConfig = LogConfig()

    def __post_init__(self):
        if isinstance(self.log, dict):
            self.log = LogConfig(**self.log)

    @property
    def path(self) -> str:
        return f"/api/{self.version}"


@lru_cache(maxsize=1)
def get_config() -> Config:
    with open(SCHEDULER_CONF_PATH, "r") as file:
        return Config(**yaml.safe_load(file))
