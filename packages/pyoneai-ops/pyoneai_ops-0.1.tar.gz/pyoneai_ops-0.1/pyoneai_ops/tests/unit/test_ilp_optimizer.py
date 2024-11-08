# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from collections.abc import Collection, Mapping
from importlib.resources import files
from typing import Literal
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
import yaml
from pyoneai.core import (
    Entity,
    Host,
    HostPool,
    Metric,
    MetricCollection,
    TimeIndex,
    VirtualMachine,
    VirtualMachinePool,
)

import pyoneai_ops
from pyoneai_ops.orchestrator.mapper import ILPOptimizer


class TestILPOptimizer:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        lib_path = files(pyoneai_ops)
        self.data_path = lib_path.joinpath("tests", "unit", "data", "mapper")

        def read_metric_data(path: str) -> dict[int, Metric]:
            # Reads entity metric data from CSV files.
            data = pd.read_csv(path, parse_dates=["time"]).set_index(["time"])
            miss_freq = data.index.freq is None
            ids = data["id"]
            metrics: dict[int, Metric] = {}
            for id_ in ids.unique().flat:
                single_id = data[ids == id_].drop(columns=["id"])
                if miss_freq:
                    single_id = single_id.asfreq("15s")
                metric = Metric.from_dataframe(data=single_id, copy=False)
                metrics[int(id_)] = metric
            return metrics

        def mock_metric_getitem(metric: Metric):
            # Mocks `Entity.metrics.__getitem__`.
            def mock_getitem(self, names: str | Collection[str]):
                mock_accessor = MagicMock()
                mock_accessor.names = (
                    [names] if isinstance(names, str) else names
                )
                mock_accessor.__getitem__ = (
                    lambda self, time_index: Metric.from_dataframe(
                        data=metric.to_dataframe().loc[:, self.names]
                    )
                )
                return mock_accessor

            return mock_getitem

        def mock_entities(
            metrics: Mapping[int, Metric], spec_set: type[Entity]
        ) -> dict[int, MagicMock]:
            # Mocks `Entity`, in particular `Entity.metrics`.
            mock_out = {}
            for id_, metric in metrics.items():
                mock_entity = MagicMock(spec_set=spec_set)
                mock_entity.id = id_
                mock_entity.metrics = MagicMock(spec_set=MetricCollection)
                mock_entity.metrics.__getitem__ = mock_metric_getitem(metric)
                mock_out[id_] = mock_entity
            return mock_out

        def create_ilp_optimizer(
            test_case: str | int,
            mode: Literal["scheduling", "rescheduling", "scaling"],
            period: TimeIndex | str,
            criteria: str,
            preemptive: bool,
            **kwargs,
        ) -> ILPOptimizer:
            case = str(test_case)
            host_path = self.data_path.joinpath(case, "hosts.csv")
            host_metrics = read_metric_data(path=str(host_path))
            mock_hosts = mock_entities(host_metrics, spec_set=Host)
            vm_path = self.data_path.joinpath(case, "vms.csv")
            vm_metrics = read_metric_data(path=str(vm_path))
            mock_vms = mock_entities(vm_metrics, spec_set=VirtualMachine)
            if not isinstance(period, TimeIndex):
                period = TimeIndex(period)
            with (
                patch.object(
                    HostPool,
                    "_get_entity",
                    autospec=True,
                    side_effect=lambda self, key: mock_hosts[key],
                ),
                patch.object(
                    VirtualMachinePool,
                    "_get_entity",
                    autospec=True,
                    side_effect=lambda self, key: mock_vms[key],
                ),
            ):
                return ILPOptimizer(
                    vmpool=VirtualMachinePool(
                        owner=self.mock_owner, ids=set(mock_vms)
                    ),
                    hostpool=HostPool(
                        owner=self.mock_owner, ids=set(mock_hosts)
                    ),
                    mode=mode,
                    period=period,
                    criteria=criteria,
                    preemptive=preemptive,
                    verbose=0,
                    **kwargs,
                )

        self.mock_owner = MagicMock()
        self.create_ilp_optimizer = create_ilp_optimizer
        self.opt = create_ilp_optimizer(
            test_case="init",
            mode="rescheduling",
            period=TimeIndex(),
            criteria="cpu_usage_balance",
            preemptive=False,
        )

    def test_init(self):
        assert isinstance(self.opt, ILPOptimizer)
        assert self.opt._curr_alloc == {2: 0, 3: 0}
        vm_host_matches = {}
        for vm_id, hostpool in self.opt._vm_host_matches.items():
            vm_host_matches[vm_id] = set(hostpool.ids)
        assert vm_host_matches == {2: {0, 1}, 3: {1}}
        host_vm_matches = {}
        for host_id, vmpool in self.opt._host_vm_matches.items():
            host_vm_matches[host_id] = set(vmpool.ids)
        assert host_vm_matches == {0: {2}, 1: {2, 3}}

    def test_map_cpu_usage_balance(self):
        self.opt.map()
        solutions = [{2: 0, 3: 1}, {2: 1, 3: 0}]
        assert self.opt.placements()[0] in solutions

    def test_map_cpu_ratio_balance(self):
        self.opt._criteria = "cpu_ratio_balance"
        self.opt.map()
        solutions = [{2: 0, 3: 1}, {2: 1, 3: 0}]
        assert self.opt.placements()[0] in solutions

    def test_map_vm_count_balance(self):
        self.opt._criteria = "vm_count_balance"
        self.opt.map()
        solutions = [{2: 0, 3: 1}, {2: 1, 3: 0}]
        assert self.opt.placements()[0] in solutions

    def test_map_pack(self):
        self.opt._criteria = "pack"
        self.opt.map()
        assert self.opt.placements() == [{2: 1, 3: 1}]

    @pytest.mark.parametrize("case", [0, 1, 2, 3, 4])
    def test_map(self, case):
        path = self.data_path.joinpath(str(case), "data.yaml")
        with open(path, encoding="utf-8") as file:
            data = yaml.safe_load(file)
        opt = self.create_ilp_optimizer(case, *data["args"], **data["kwargs"])
        opt.map()
        # TODO: Check and complete the lists of expected solutions.
        assert opt.placements()[0] in data["solutions"], (
            f"test case: {case}\n"
            f"title: {data['title']}\n"
            f"result: {opt.placements()[0]}"
        )
