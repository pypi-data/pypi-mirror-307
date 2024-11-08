from datetime import timezone
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest
import torch
from pyoneai.core import Metric, PoolMetric
from pyoneai.core.virtual_machine import VirtualMachinePool

import pyoneai_ops.mlops.generators.synthetic as synthetic_generator
from pyoneai_ops.mlops.dataset import (
    OneTimeSeriesDataset,
    SyntheticTimeSeriesDataset,
)


class TestDataset:

    def _create_vmpool_metric_mock(self, mocker, length=100):
        one_mock = MagicMock()
        pool_mock = VirtualMachinePool(self.session, ids=[0])

        dummy_timeseries = np.random.randn(length)
        vms_metric = PoolMetric(
            pool=pool_mock,
            metrics=[
                Metric(
                    time_index=pd.date_range(
                        "2019-02-02T01:01:00", periods=length, tz=timezone.utc
                    ),
                    data={"cpu_usage": dummy_timeseries},
                )
            ],
        )
        one_mock.vms.metrics.__getitem__.return_value.__getitem__.return_value = (
            vms_metric
        )
        mocker.patch("pyoneai_ops.mlops.dataset.One", return_value=one_mock)

    @pytest.fixture(autouse=True)
    def setup_config(self):
        # Mocking the get_config function to return a custom configuration
        self.session = MagicMock()
        with patch("pyoneai_ops.mlops.dataset.get_config") as mock_get_config:
            mock_config = MagicMock()
            mock_config.sequence_length = 24
            mock_config.batch_size = 5
            mock_config.num_workers = 0
            mock_config.lr = 0.05
            mock_config.weight_decay = 0.001
            mock_get_config.return_value = mock_config
            yield

    @pytest.fixture(autouse=True)
    def setup_one_time_series_dataset(self, mocker):
        self._create_vmpool_metric_mock(mocker, 100)
        self.vm_dataset = OneTimeSeriesDataset(
            self.session, "virtualmachine", slice("-30d", "-2d"), "cpu_usage"
        )
        yield

    @pytest.fixture(autouse=True)
    def setup_synthetic_time_series_dataset(self):
        session = MagicMock()
        self.vm_synthetic_dataset = SyntheticTimeSeriesDataset(
            session,
            slice("-1h10m", "+1d10m", "1h"),
            "random_workload",
        )
        yield

    def test_iter_over_tensors_tuple_one_time_series(self):
        for x, y in self.vm_dataset:
            assert isinstance(x, Metric)
            assert isinstance(y, Metric)

    def test_iter_over_metrics_tuple_synthetic_time_series(self):
        for x, y in self.vm_synthetic_dataset:
            assert isinstance(x, Metric)
            assert isinstance(y, Metric)

    def test_invalid_generator_name(self):
        oneinisght_obj = MagicMock()
        with pytest.raises(
            ValueError,
            match="Generator 'invalid_generator' not found in synthetic module.",
        ):
            SyntheticTimeSeriesDataset(
                oneinisght_obj,
                slice("-1h10m", "+1d10m", "1h"),
                "invalid_generator",
            )

    def test_valid_generator_name(self):
        oneinisght_obj = MagicMock()
        dataset = SyntheticTimeSeriesDataset(
            oneinisght_obj,
            slice("-1h10m", "+1d10m", "1h"),
            "high_usage_during_off_hours",
        )
        assert isinstance(dataset, SyntheticTimeSeriesDataset)

    def test_callable_generator(self):
        oneinisght_obj = MagicMock()
        dataset = SyntheticTimeSeriesDataset(
            oneinisght_obj,
            slice("-1h10m", "+1d10m", "1h"),
            synthetic_generator.high_usage_during_off_hours,
        )
        assert isinstance(dataset, SyntheticTimeSeriesDataset)

    def test_returned_one_time_series_pool_metric(self):
        assert isinstance(self.vm_dataset.get_metrics(), PoolMetric)

    def test_returned_synthetic_time_series_pool_metric(self):
        assert isinstance(self.vm_synthetic_dataset.get_metrics(), PoolMetric)
