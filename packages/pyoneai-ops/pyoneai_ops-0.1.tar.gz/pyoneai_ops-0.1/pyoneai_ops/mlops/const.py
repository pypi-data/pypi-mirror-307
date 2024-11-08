__all__ = [
    "Variables",
]
from enum import Enum, StrEnum
from typing import Self, Type

try:
    import torch
except ImportError:
    _HAS_TORCH = False
else:
    from pyoneai_ops.mlops.drivers import LightningDriver
    _HAS_TORCH = True

from pyoneai_ops.mlops.drivers import PersistenceModelDriver, StatsmodelsDriver


class Variables(StrEnum):
    DEFAULT_LSTM_WEIGHTS = "default_lstm_weights"
    DEFAULT_TRANSFORMER_WEIGHTS = "default_transformer_weights"


# TODO: to support collecting models dynamically (all subclasses of some
# base driver, refer to: https://github.com/OpenNebula/one-aiops/issues/219)
class SupportedModels(Enum):
    if _HAS_TORCH:
        LSTM = "pyoneai.mlmodels.ConvLSTMModel", LightningDriver
        TRANSFORMER = "pyoneai.mlmodels.TransformerModel", LightningDriver
    ARIMA = "pyoneai.mlmodels.ArimaModel", StatsmodelsDriver
    PERSISTENCE = "pyoneai.mlmodels.PersistenceModel", PersistenceModelDriver

    @classmethod
    def keys(cls) -> list[str]:
        return list(map(lambda c: c.name.lower(), cls))

    @property
    def driver(self) -> Type:
        return self.value[1]

    @property
    def qualified_name(self) -> str:
        return self.value[0]

    @classmethod
    def get(cls, name: str) -> Self:
        """Get the model qualified name."""
        if (name_up := name.upper()) in cls.__members__:
            return cls[name_up]
        return cls(name)
