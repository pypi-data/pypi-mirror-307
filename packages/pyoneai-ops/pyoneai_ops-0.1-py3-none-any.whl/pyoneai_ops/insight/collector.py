__all__ = ("generate_predictions",)
from abc import ABC, abstractmethod
from typing import Generator, Iterable, Literal

import pandas as pd
import prometheus_client
from prometheus_client.core import CollectorRegistry, GaugeMetricFamily
from pyoneai import Session
from pyoneai.core import HostState, One, VirtualMachineState

from .config import get_config

_SupportedEntityes = Literal["virtualmachine", "host", "cluster"]


class MetricsCollector(ABC):

    def __init__(
        self,
        session: Session,
        metric_name: str,
        resolution: str,
        steps: int = 1,
    ):
        if not isinstance(steps, int) or steps < 1:
            raise ValueError("'steps' must be a positive integer")
        self.metric_name = metric_name
        self.resolution = resolution
        self.session = session
        self.predictions_nbr = steps
        self.one = One(self.session)

    @property
    @abstractmethod
    def export_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def iter_over_entities(self) -> Iterable:
        raise NotImplementedError

    @abstractmethod
    def generate_predictions(self, entity) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def labels(self) -> list[str]:
        raise NotImplementedError

    def collect(self) -> Generator[GaugeMetricFamily, None, None]:
        gauge = GaugeMetricFamily(
            self.export_name, self.export_name, labels=self.labels
        )
        for entity in self.iter_over_entities():
            predictions = self.generate_predictions(entity)
            for horizon, value in predictions.items():
                gauge.add_metric([str(entity.id), horizon], str(value))
        yield gauge


class BaseCollector(MetricsCollector):

    @property
    def period(self) -> str:
        return slice(
            pd.Timedelta(self.resolution),
            pd.Timedelta(self.resolution) * self.predictions_nbr,
            pd.Timedelta(self.resolution),
        )

    def generate_predictions(self, entity) -> dict:
        MINUTE_CHAR = "m"
        prediction_horizons = [
            f"+{int((pd.Timedelta(self.resolution) * i).total_seconds() // 60)}{MINUTE_CHAR}"
            for i in range(1, self.predictions_nbr + 1)
        ]
        predictions_values = (
            entity.metrics[self.metric_name][self.period].to_array().flatten()
        )
        return {
            horizon: value
            for horizon, value in zip(prediction_horizons, predictions_values)
        }


class VirtualMachineCollector(BaseCollector):

    @property
    def export_name(self) -> str:
        return f"opennebula_vm_{self.metric_name}"

    @property
    def labels(self) -> list[str]:
        return ["one_vm_id", "forecast"]

    def iter_over_entities(self) -> Iterable:
        return self.one.vms[
            self.one.vms.metrics["state"]["0"] == VirtualMachineState.ACTIVE
        ]


class HostCollector(BaseCollector):

    @property
    def export_name(self) -> str:
        return f"opennebula_host_{self.metric_name}"

    @property
    def labels(self) -> list[str]:
        return ["one_host_id", "forecast"]

    def iter_over_entities(self) -> Iterable:
        return self.one.hosts[
            self.one.hosts.metrics["state"]["0"] == HostState.MONITORED
        ]


class Registry:
    registry: CollectorRegistry
    collector_class = {
        "virtualmachine": VirtualMachineCollector,
        "host": HostCollector,
    }

    def __init__(
        self,
        entity: _SupportedEntityes,
        metric_names: list[str] | None,
        resolution: str,
        steps: int,
    ):

        self.registry = CollectorRegistry()
        self.session = Session(get_config().config_path)
        if metric_names is None:
            # TODO: to update when the issue
            # https://github.com/OpenNebula/one-aiops/issues/390 is resolved
            metric_names = list(self.session.config.registry[entity].keys())

        collector_cls = self.collector_class[entity]

        for name in metric_names:
            self.registry.register(
                collector_cls(self.session, name, resolution, steps)
            )

    @property
    def latest(self):
        return prometheus_client.generate_latest(self.registry)


def generate_predictions(
    entity: _SupportedEntityes,
    metric_names: list[str] | None,
    resolution: str,
    steps: int,
):
    return Registry(entity, metric_names, resolution, steps).latest
