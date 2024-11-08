__all__ = ("BaseDriver",)
import inspect
import logging
import os
import warnings
from abc import ABCMeta, abstractmethod
from functools import cached_property
from importlib import import_module
from pathlib import Path
from typing import Any, Callable, Literal, Self, Type

from pyoneai import Session

from pyoneai_ops.mlops import metrics as M
from pyoneai_ops.mlops.config import get_config
from pyoneai_ops.mlops.dataset import TimeSeriesDataset

log = logging.getLogger("oneaiops.mlops.drivers.base")


class BaseDriver(metaclass=ABCMeta):
    model_path: str
    hparams: dict[str, Any]
    metric_name: str
    n: int

    def __init__(
        self,
        session: Session,
        entity: Literal["virtualmachine", "host", "cluster"],
        metric: str,
        model_path: os.PathLike | str | None = None,
        model_kwargs: dict[str, Any] | None = None,
        n: int = 1,
    ) -> None:
        self.session = session
        self._setup_metric_conf(entity, metric)
        self.n = n
        self.metric_name = metric
        self.model_path = model_path

        self.hparams = self._gather_hparams(model_kwargs)

    @property
    def _epochs(self) -> int:
        return get_config().models[self.model_path].training["epochs"]

    @cached_property
    def conf_hparams(self) -> dict:
        return get_config().models[self.model_path].hparams or {}

    def _setup_metric_conf(self, entity: str, metric_name: str) -> None:
        match entity:
            case "virtualmachine":
                self._metric_conf = self.session.config.registry[
                    "virtualmachine"
                ][metric_name]
            case "host":
                self._metric_conf = self.session.config.registry["host"][
                    metric_name
                ]
            case "cluster":
                self._metric_conf = self.session.config.registry["cluster"][
                    metric_name
                ]
            case _:
                raise ValueError(f"Invalid entity {entity}")

    def _gather_hparams(
        self, model_kwargs: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        model_kwargs = model_kwargs or {}
        mlops_conf_kwargs = self.conf_hparams | model_kwargs
        model_signature = inspect.signature(self.ml_class)

        try:
            bound_args = model_signature.bind(**mlops_conf_kwargs)
        except TypeError as e:
            warnings.warn(
                "Provided hyperparameters are not valid for the "
                f"model '{self.ml_class}'. They will be ignored."
            )
            return {}

        bound_args.apply_defaults()

        return dict(bound_args.arguments)

    def validate_weights(self, weights: os.PathLike | str):
        weights = Path(weights)
        if not weights.exists():
            raise FileNotFoundError(
                f"Weights were not found under the {weights}"
            )

    def validate_metrics(self, metrics: list[str]):
        if not metrics:
            raise ValueError(
                "You need to provide a list of metrics to be computed."
            )

    def collect_metrics_callables(self, metrics: list[str]) -> list[Callable]:
        return [M.get_metric_callable(m) for m in metrics]

    @property
    def ml_class(self) -> Type:
        module_name, _, class_name = self.model_path.rpartition(".")
        module = import_module(module_name)
        return getattr(module, class_name)

    @abstractmethod
    def fit(
        self, dataset: TimeSeriesDataset, weights: os.PathLike | str
    ) -> Self:
        raise NotImplementedError

    @abstractmethod
    def test(
        self,
        weights: os.PathLike | str,
        dataset: TimeSeriesDataset,
        metrics: list[str],
    ) -> list[float]:
        raise NotImplementedError
