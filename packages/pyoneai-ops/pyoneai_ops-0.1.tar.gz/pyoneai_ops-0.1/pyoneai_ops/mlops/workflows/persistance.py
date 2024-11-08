"""The module contains persistance-related tasks and flows."""

__all__ = ("save_model", "deploy_model")

import mlflow
from prefect import task

from pyoneai_ops.mlops.config import get_config
from pyoneai_ops.mlops.drivers.lightning import LightningDriver

# Load configuration once
config = get_config()


# #########################
#          TASKS
# #########################
@task(retries=config.retries, retry_delay_seconds=config.retry_delay_seconds)
def save_model(trainer: LightningDriver, ann_model: str):
    with mlflow.start_run():
        mlflow.pytorch.log_model(trainer.path, ann_model)


@task(retries=config.retries, retry_delay_seconds=config.retry_delay_seconds)
def deploy_model(saved_model):
    # Simulate deploying the model
    return f"deployed_{saved_model}"
