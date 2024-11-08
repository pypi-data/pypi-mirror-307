import logging
from abc import ABCMeta, abstractmethod
from functools import cached_property
from typing import Callable, Iterable

import numpy as np
import pandas as pd

try:
    import torch
except ImportError:
    _HAS_TORCH = False
else:
    _HAS_TORCH = True

from pyoneai import One
from pyoneai.core import Metric, PoolMetric
from pyoneai.core.virtual_machine import VirtualMachinePool

from pyoneai_ops.mlops.config import get_config
from pyoneai_ops.mlops.generators import synthetic
from pyoneai_ops.mlops.types import SupportedEntities

# TODO: we should define how to define validation split based on iterators
log = logging.getLogger("pyoneai-ops.mlops.dataset")


class TimeSeriesDataset(Iterable, metaclass=ABCMeta):
    def __init__(self, session, history, n: int = 1):
        self.session = session
        self.history = history
        self._metrics = self.get_metrics()
        self.n = n

    @cached_property
    def _sequence_length(self) -> int:
        return get_config().sequence_length

    @abstractmethod
    def get_metrics(self) -> PoolMetric:
        raise NotImplementedError

    def __iter__(self) -> Iterable[tuple[Metric, Metric]]:
        # TODO: to be updated when issue
        # https://github.com/OpenNebula/one-aiops/issues/262 is resolved
        for entity_id, m in self._metrics._metrics.items():
            for i in range(len(m) - self._sequence_length - self.n + 1):
                history_subset = m._df.iloc[i : i + self._sequence_length]
                prediction_subset = m._df.iloc[
                    i
                    + self._sequence_length : i
                    + self._sequence_length
                    + self.n
                ]
                yield (
                    Metric(
                        time_index=history_subset.index, data=history_subset
                    ),
                    Metric(
                        time_index=prediction_subset.index,
                        data=prediction_subset,
                    ),
                )


class OneTimeSeriesDataset(TimeSeriesDataset):
    def __init__(
        self,
        session,
        entity: SupportedEntities,
        history: slice,
        metric: str,
    ):
        self.entity = entity
        self.metric = metric
        super().__init__(session, history)

    def get_metrics(self) -> PoolMetric:
        _one = One(self.session)
        match self.entity:
            case "virtualmachine":
                return _one.vms.metrics[self.metric][self.history]
            case "host":
                return _one.hosts.metrics[self.metric][self.history]
            case _:
                raise ValueError(f"Invalid entity {self.entity}")


class SyntheticTimeSeriesDataset(TimeSeriesDataset):
    _DUMMY_ID: int = 0

    def __init__(
        self,
        session,
        history: slice,
        generator: Callable | str,
        generator_kwargs: dict | None = None,
    ):
        if isinstance(generator, str):
            if not hasattr(synthetic, generator):
                raise ValueError(
                    f"Generator '{generator}' not found in synthetic module."
                )
            generator = getattr(synthetic, generator)

        self.generator = generator
        self.generator_kwargs = generator_kwargs or {}
        super().__init__(session, history)

    def get_metrics(self) -> PoolMetric:
        start_time = pd.Timestamp.now(tz="UTC") + pd.Timedelta(
            self.history.start
        )
        end_time = pd.Timestamp.now(tz="UTC") + pd.Timedelta(self.history.stop)
        time_resolution = pd.Timedelta(self.history.step)

        timestamps = pd.date_range(
            start=start_time, end=end_time, freq=time_resolution
        )

        synthetic_generator = self.generator(
            start_time=start_time,
            time_resolution=time_resolution,
            **self.generator_kwargs,
        )

        datetimes, usages = zip(
            *[next(synthetic_generator) for _ in range(len(timestamps))]
        )
        synthetic_metric = Metric(
            time_index=datetimes, data={"metric_usage": usages}
        )

        metrics_collection = {self._DUMMY_ID: synthetic_metric}
        return PoolMetric(
            pool=VirtualMachinePool(One(self.session), ids=[self._DUMMY_ID]),
            metrics=metrics_collection,
        )
