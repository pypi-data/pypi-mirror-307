__all__ = (
    "Config",
    "get_config",
)
import os
from dataclasses import dataclass
from functools import lru_cache

import yaml

from ...logger import LogConfig

PLAN_EXECUTOR_CONF_PATH: str = os.environ.get(
    "PYONEAIOPS_PLAN_EXECUTOR_CONF_PATH",
    "/etc/one/aiops/plan_executor.conf",
)


@dataclass
class Config:
    host: str
    port: int
    version: str
    retries: int
    backoff: int
    max_time: int
    log: LogConfig = LogConfig()

    def __post_init__(self):
        if isinstance(self.log, dict):
            self.log = LogConfig(**self.log)

    @property
    def path(self) -> str:
        return f"/api/{self.version}"


@lru_cache(maxsize=1)
def get_config() -> Config:
    with open(PLAN_EXECUTOR_CONF_PATH, "r") as file:
        return Config(**yaml.safe_load(file))
