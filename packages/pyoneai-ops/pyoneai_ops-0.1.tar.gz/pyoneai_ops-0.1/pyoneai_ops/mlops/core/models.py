"""The module contains models' preparation functionalities."""

__all__ = ("load_driver", "train_model", "test_model")

import os
from typing import Any

from pyoneai_ops.mlops.dataset import TimeSeriesDataset
from pyoneai_ops.mlops.drivers.base import BaseDriver


def train_model(
    driver: BaseDriver,
    dataset: TimeSeriesDataset,
    weights: os.PathLike | str,
):
    driver.fit(dataset=dataset, weights=weights)


def test_model(
    driver: BaseDriver,
    weights: os.PathLike | str,
    dataset: TimeSeriesDataset,
    validation_metrics: list,
) -> dict[str, float]:
    return driver.test(
        weights=weights, dataset=dataset, metrics=validation_metrics
    )
