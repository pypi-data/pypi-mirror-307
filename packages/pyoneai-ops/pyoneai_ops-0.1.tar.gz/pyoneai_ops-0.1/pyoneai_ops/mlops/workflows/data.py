"""The module contains preparation functionalities for training."""

__all__ = ("load_real_data", "load_synthetic_data")

from typing import Callable

from prefect import task

import pyoneai_ops.mlops.core.data
from pyoneai_ops.mlops.config import get_config
from pyoneai_ops.mlops.types import SupportedEntities

config = get_config()


# #########################
#          TASKS
# #########################
@task(retries=config.retries, retry_delay_seconds=config.retry_delay_seconds)
def load_real_data(
    session,
    entity: SupportedEntities,
    period: slice,
    metric: str,
):

    return mlops.core.data.load_real_data(
        session=session, entity=entity, period=period, metric=metric
    )


@task(retries=config.retries, retry_delay_seconds=config.retry_delay_seconds)
def load_synthetic_data(
    session,
    period: slice,
    generator: Callable | str,
    generator_kwargs: dict | None = None,
):
    return mlops.core.data.load_synthetic_data(
        session=session,
        period=period,
        generator=generator,
        generator_kwargs=generator_kwargs,
    )
