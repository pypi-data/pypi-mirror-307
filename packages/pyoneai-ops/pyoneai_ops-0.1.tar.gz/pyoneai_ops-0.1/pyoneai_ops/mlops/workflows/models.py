"""The module contains models' preparation functionalities tasks and flows."""

__all__ = ("load_driver", "train_model", "test_model")

from prefect import task

import pyoneai_ops.mlops.core.models
from pyoneai_ops.mlops.config import get_config
from pyoneai_ops.mlops.dataset import TimeSeriesDataset
from pyoneai_ops.mlops.drivers.lightning import LightningDriver

config = get_config()


# #########################
#          TASKS
# #########################
@task(retries=config.retries, retry_delay_seconds=config.retry_delay_seconds)
def load_driver(
    session,
    entity: str,
    metric: str,
    model_path: str,
):
    return mlops.core.models.load_driver(
        session=session,
        entity=entity,
        metric=metric,
        model_path=model_path,
    )


@task(retries=config.retries, retry_delay_seconds=config.retry_delay_seconds)
def train_model(trainer: LightningDriver, dataset: TimeSeriesDataset):
    mlops.core.models.train_model(trainer=trainer, dataset=dataset)


@task(retries=config.retries, retry_delay_seconds=config.retry_delay_seconds)
def test_model(
    trainer: LightningDriver,
    weights: str,
    dataset: TimeSeriesDataset,
    validation_metrics: list,
):
    mlops.core.models.test_model(
        trainer=trainer,
        weights=weights,
        dataset=dataset,
        validation_metrics=validation_metrics,
    )
