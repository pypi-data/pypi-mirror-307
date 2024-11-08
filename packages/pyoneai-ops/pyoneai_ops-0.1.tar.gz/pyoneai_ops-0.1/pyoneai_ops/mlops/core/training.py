__all__ = [
    "train_model_on_real",
    "train_model_on_syntehtic",
]
from pyoneai import Session

from pyoneai_ops.mlops.const import SupportedModels
from pyoneai_ops.mlops.dataset import (
    OneTimeSeriesDataset,
    SyntheticTimeSeriesDataset,
)
from pyoneai_ops.mlops.types import SupportedEntities


def train_model_on_real(
    session: Session,
    entity: SupportedEntities,
    period: slice,
    metric_name: str,
    model: SupportedModels,
    path: str | None = None,
):
    assert model is not None, "Model must be provided"
    dataset = OneTimeSeriesDataset(session, entity, period, metric_name)
    trainer = model.driver(
        session,
        entity,
        metric_name,
        model_path=model.qualified_name,
    )
    trainer.fit(dataset, path)


def train_model_on_syntehtic(
    session: Session,
    entity: SupportedEntities,
    period: slice,
    metric_name: str,
    scenario: str,
    model: SupportedModels,
    path: str | None = None,
):
    assert model is not None, "Model must be provided"
    dataset = SyntheticTimeSeriesDataset(session, period, scenario)
    trainer = model.driver(
        session,
        entity,
        metric_name,
        model_path=model.qualified_name,
    )
    trainer.fit(dataset, weights=path)
