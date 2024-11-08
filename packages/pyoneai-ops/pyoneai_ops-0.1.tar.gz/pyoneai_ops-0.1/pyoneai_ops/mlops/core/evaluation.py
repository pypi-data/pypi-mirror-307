__all__ = [
    "evaluate_predefined_model_on_real_data",
    "evaluate_predefined_model_on_synthetic_data",
    "evaluate_custom_model_on_real_data",
    "evaluate_custom_model_on_synthetic_data",
]
import os
from typing import Any, Literal

from pyoneai import Session

from pyoneai_ops.mlops.const import SupportedModels
from pyoneai_ops.mlops.core.data import load_real_data, load_synthetic_data
from pyoneai_ops.mlops.core.models import test_model
from pyoneai_ops.mlops.types import SupportedEntities, SupportedProfiles


def evaluate_on_real_data(
    session: Session,
    entity: SupportedEntities,
    metric_name: Literal["cpu_usage"],
    period: slice,
    model: SupportedModels,
    weights_path: os.PathLike | None = None,
    model_kwargs: dict[str, Any] | None = None,
    data_profile_kwargs: dict | None = None,
    metrics: list[str] | None = None,
) -> dict[str, float]:
    data_profile_kwargs = data_profile_kwargs or {}

    dataset = load_real_data(
        session=session, entity=entity, period=period, metric=metric_name
    )
    driver = model.driver(
        session=session,
        entity=entity,
        metric=metric_name,
        model_path=model.qualified_name,
        model_kwargs=model_kwargs,
    )

    return test_model(
        driver=driver,
        weights=weights_path,
        dataset=dataset,
        validation_metrics=metrics,
    )


def evaluate_on_synthetic_data(
    session: Session,
    entity: SupportedEntities,
    metric_name: Literal["cpu_usage"],
    data_profile: SupportedProfiles,
    period: slice,
    model: SupportedModels,
    weights_path: os.PathLike | None = None,
    model_kwargs: dict[str, Any] | None = None,
    data_profile_kwargs: dict | None = None,
    metrics: list[str] | None = None,
) -> dict[str, float]:
    data_profile_kwargs = data_profile_kwargs or {}

    dataset = load_synthetic_data(
        session=session,
        period=period,
        generator=data_profile,
        generator_kwargs=data_profile_kwargs,
    )

    driver = model.driver(
        session=session,
        entity=entity,
        metric=metric_name,
        model_path=model.qualified_name,
        model_kwargs=model_kwargs,
    )

    return test_model(
        driver=driver,
        weights=weights_path,
        dataset=dataset,
        validation_metrics=metrics,
    )
