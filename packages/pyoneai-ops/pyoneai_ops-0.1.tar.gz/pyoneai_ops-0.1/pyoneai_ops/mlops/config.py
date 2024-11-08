__all__ = (
    "Config",
    "get_config",
)
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import yaml

MLOPS_CONF_PATH: str = os.environ.get(
    "PYONEAIOPS_MLOPS_CONF_PATH", "/etc/one/aiops/mlops.conf"
)


@dataclass(frozen=True)
class _ModelConf:
    training: dict[str, Any]
    hparams: dict[str, Any]


@dataclass(frozen=False)
class Config:
    sequence_length: int
    models: dict[str, _ModelConf]

    def __post_init__(self):
        self.models = {k: _ModelConf(**v) for k, v in self.models.items()}


@lru_cache(maxsize=1)
def get_config() -> Config:
    with open(MLOPS_CONF_PATH, "r") as file:
        return Config(**yaml.safe_load(file))
