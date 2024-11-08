"""The module contains preparation data."""

__all__ = ("load_real_data", "load_synthetic_data")

from typing import Callable

from pyoneai_ops.mlops.dataset import (
    OneTimeSeriesDataset,
    SyntheticTimeSeriesDataset,
)
from pyoneai_ops.mlops.types import SupportedEntities


def load_real_data(
    session,
    entity: SupportedEntities,
    period: slice,
    metric: str,
):
    return OneTimeSeriesDataset(session, entity, period, metric)


def load_synthetic_data(
    session,
    period: slice,
    generator: Callable | str,
    generator_kwargs: dict | None = None,
):
    generator_kwargs = generator_kwargs or {}

    return SyntheticTimeSeriesDataset(
        session, period, generator, generator_kwargs
    )
