from unittest.mock import MagicMock

import pytest


class TestCollector:

    @pytest.fixture(autouse=True, scope="function")
    def setup(self, mocker):
        from pyoneai_ops.insight.collector import VirtualMachineCollector, HostCollector

        self.collector_map = {
            "VirtualMachineCollector": VirtualMachineCollector,
            "HostCollector": HostCollector
        }

    @pytest.mark.parametrize("collector_class, entity_id_label", [
        ("VirtualMachineCollector", "one_vm_id"),
        ("HostCollector", "one_host_id")
    ])
    def test_use_result_format(self, mocker, collector_class, entity_id_label):
        import prometheus_client
        import prometheus_client
        from prometheus_client.core import CollectorRegistry

        ENTITY_ID = 1
        PREDICTIONS = {"+1m": 10, "+2m": 20}
        METRIC_NAME = "dummy_metric"
        RESOLUTION = "2m"

        entity_mock = MagicMock()
        entity_mock.id = ENTITY_ID
        mocker.patch(
            f"pyoneai_ops.insight.collector.{collector_class}.iter_over_entities",
            return_value=iter([entity_mock]),
        )
        mocker.patch(
            f"pyoneai_ops.insight.collector.{collector_class}.generate_predictions",
            return_value=PREDICTIONS,
        )

        collector = self.collector_map[collector_class](
            MagicMock(), METRIC_NAME, RESOLUTION
        )
        registry = CollectorRegistry()
        registry.register(collector)
        result = prometheus_client.generate_latest(registry).decode()
        assert METRIC_NAME in result
        assert f'forecast="+{RESOLUTION}",{entity_id_label}="{ENTITY_ID}"' in result
        for k in PREDICTIONS.keys():
            assert k in result

    @pytest.mark.parametrize(
        "nbr, res, expected, collector_class",
        [
            (10, "1m", slice("+1m", "+10m", "1m"), "VirtualMachineCollector"),
            (14, "5s", slice("+5s", "+70s", "5s"), "VirtualMachineCollector"),
            (1, "10s", slice("+10s", "+10s", "10s"), "VirtualMachineCollector"),
            (10, "1m", slice("+1m", "+10m", "1m"), "HostCollector"),
            (14, "5s", slice("+5s", "+70s", "5s"), "HostCollector"),
            (1, "10s", slice("+10s", "+10s", "10s"), "HostCollector"),
        ],
    )
    def test_period(self, nbr, res, expected, collector_class):
        import pandas as pd

        collector = self.collector_map[collector_class](
            MagicMock(), "dummy_metric", res, steps=nbr
        )
        assert collector.period == slice(
            pd.Timedelta(expected.start),
            pd.Timedelta(expected.stop),
            pd.Timedelta(expected.step),
        )

    @pytest.mark.parametrize("collector_class", ["VirtualMachineCollector", "HostCollector"])
    @pytest.mark.parametrize("steps", [0, -1])
    def test_raise_on_wrong_number_of_predictions(self, collector_class, steps):
        with pytest.raises(ValueError, match=r"'steps' must be a positive integer"):
            _ = self.collector_map[collector_class](
                MagicMock(), "dummy_metric", "1m", steps=steps
            )

    @pytest.mark.parametrize("collector_class", ["VirtualMachineCollector", "HostCollector"])
    def test_generate_predictions_format(self, collector_class):
        import numpy as np

        entity_mock = MagicMock()
        entity_mock.metrics.__getitem__.return_value.__getitem__.return_value.to_array.return_value = np.array(
            [10, 20, 30]
        )
        collector = self.collector_map[collector_class](
            MagicMock(), "dummy_metric", "1m", steps=3
        )
        assert collector.generate_predictions(entity_mock) == {
            "+1m": 10,
            "+2m": 20,
            "+3m": 30,
        }

    @pytest.mark.parametrize("collector_class", ["VirtualMachineCollector", "HostCollector"])
    def test_generate_predictions_for_nested_array_value(self, collector_class):
        from numbers import Number

        import numpy as np

        entity_mock = MagicMock()
        entity_mock.metrics.__getitem__.return_value.__getitem__.return_value.to_array.return_value = np.array(
            np.array([[10]])
        )
        collector = self.collector_map[collector_class](
            MagicMock(), "dummy_metric", "1m", steps=3
        )
        assert isinstance(
            collector.generate_predictions(entity_mock)["+1m"], Number
        )
