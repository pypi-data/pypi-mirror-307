from typing import Literal, Optional

from prefect import flow
from prefect.flows import EntrypointType

import pyoneai_ops.mlops.core.evaluation
from pyoneai_ops.mlops.mlops.types import SupportedEntities
from pyoneai_ops.mlops.workflows.utils import (
    generate_flow_run_name,
    get_session,
)


# #########################
#          FLOWS
# #########################
@flow(
    name="Model Training and Validation with predefined model",
    description="Train and validate models on real datasets",
    generate_flow_run_name=generate_flow_run_name,
)
async def evaluate_predefined_model_on_real_data(
    weights: Optional[str] = None,
    entity: Literal["virtualmachine", "host"] = "virtualmachine",
    metric_name: Literal["cpu_usage"] = "cpu_usage",
    start_date: str = "-3d",
    end_date: str = "-1d",
    resolution: str = "10s",
    mae_score: bool = True,
    mse_score: bool = True,
    rmse_score: bool = True,
    nrmse_score: bool = True,
    r2_score: bool = True,
    spearman_correlation: bool = True,
    mape_score: bool = True,
):
    session = get_session()
    period = slice(start_date, end_date, resolution)

    mlops.core.evaluation.evaluate_predefined_model_on_real_data(
        session=session,
        weights=weights,
        entity=entity,
        metric_name=metric_name,
        period=period,
        mae_score=mae_score,
        mse_score=mse_score,
        rmse_score=rmse_score,
        nrmse_score=nrmse_score,
        r2_score=r2_score,
        spearman_correlation=spearman_correlation,
        mape_score=mape_score,
    )


async def evaluate_predefined_model_on_synthetic_data(
    weights: Optional[str] = None,
    entity: SupportedEntities = "virtualmachine",
    metric_name: Literal["cpu_usage"] = "cpu_usage",
    data_profile: Literal[
        "random_workload",
        "high_loads_on_weekdays",
        "high_loads_on_weekends",
        "high_loads_on_working_hours_on_weekdays",
        "high_loads_on_specific_working_hours_on_weekdays",
        "high_usage_during_off_hours",
        "intensive_usage",
        "low_usage",
        "random_usage_with_periodic_spikes",
        "seasonal_workload_variation",
        "continuous_growth",
        "daily_seasonal_exponential",
    ] = "random_workload",
    start_date: str = "-3d",
    end_date: str = "-1d",
    resolution: str = "10s",
    data_profile_kwargs: dict | None = None,
    mae_score: bool = True,
    mse_score: bool = True,
    rmse_score: bool = True,
    nrmse_score: bool = True,
    r2_score: bool = True,
    spearman_correlation: bool = True,
    mape_score: bool = True,
):
    session = get_session()
    period = slice(start_date, end_date, resolution)

    mlops.core.evaluation.evaluate_predefined_model_on_synthetic_data(
        session=session,
        entity=entity,
        metric_name=metric_name,
        data_profile=data_profile,
        period=period,
        weights=weights,
        data_profile_kwargs=data_profile_kwargs,
        mae_score=mae_score,
        mse_score=mse_score,
        rmse_score=rmse_score,
        nrmse_score=nrmse_score,
        r2_score=r2_score,
        spearman_correlation=spearman_correlation,
        mape_score=mape_score,
    )


async def evaluate_custom_model_on_real_data(
    ml_import_path: str,
    weights: str,
    entity: SupportedEntities,
    metric_name: Literal["cpu_usage"],
    start_date: str = "-3d",
    end_date: str = "-1d",
    resolution: str = "10s",
    mae_score: bool = True,
    mse_score: bool = True,
    rmse_score: bool = True,
    nrmse_score: bool = True,
    r2_score: bool = True,
    spearman_correlation: bool = True,
    mape_score: bool = True,
):
    session = get_session()
    period = slice(start_date, end_date, resolution)

    mlops.core.evaluation.evaluate_custom_model_on_real_data(
        session=session,
        ml_import_path=ml_import_path,
        weights=weights,
        entity=entity,
        metric_name=metric_name,
        period=period,
        mae_score=mae_score,
        mse_score=mse_score,
        rmse_score=rmse_score,
        nrmse_score=nrmse_score,
        r2_score=r2_score,
        spearman_correlation=spearman_correlation,
        mape_score=mape_score,
    )


async def evaluate_custom_model_on_synthetic_data(
    ml_import_path: str,
    weights: str,
    entity: SupportedEntities,
    metric_name: Literal["cpu_usage"],
    data_profile: Literal[
        "random_workload",
        "high_loads_on_weekdays",
        "high_loads_on_weekends",
        "high_loads_on_working_hours_on_weekdays",
        "high_loads_on_specific_working_hours_on_weekdays",
        "high_usage_during_off_hours",
        "intensive_usage",
        "low_usage",
        "random_usage_with_periodic_spikes",
        "seasonal_workload_variation",
        "continuous_growth",
        "daily_seasonal_exponential",
    ],
    start_date: str = "-3d",
    end_date: str = "-1d",
    resolution: str = "10s",
    data_profile_kwargs: dict | None = None,
    mae_score: bool = True,
    mse_score: bool = True,
    rmse_score: bool = True,
    nrmse_score: bool = True,
    r2_score: bool = True,
    spearman_correlation: bool = True,
    mape_score: bool = True,
):
    session = get_session()
    period = slice(start_date, end_date, resolution)

    mlops.core.evaluation.evaluate_custom_model_on_synthetic_data(
        session=session,
        ml_import_path=ml_import_path,
        weights=weights,
        entity=entity,
        metric_name=metric_name,
        data_profile=data_profile,
        period=period,
        data_profile_kwargs=data_profile_kwargs,
        mae_score=mae_score,
        mse_score=mse_score,
        rmse_score=rmse_score,
        nrmse_score=nrmse_score,
        r2_score=r2_score,
        spearman_correlation=spearman_correlation,
        mape_score=mape_score,
    )


# #########################
#       DEPLOYMENTS
# #########################
def _apply_validating_deployments():
    evaluate_predefined_model_on_real_data.to_deployment(
        name="validate-predefined-model-on-real-data",
        description="Validate one of the predefined ANN models on the actual "
        "OpenNebula data",
        tags=["validation", "real-data", "predefined-model"],
        version="0.0.1",
        work_pool_name="default-agent-pool",
        work_queue_name="default",
        entrypoint_type=EntrypointType.MODULE_PATH,
    ).apply()

    evaluate_custom_model_on_real_data.to_deployment(
        name="validate-custom-model-on-real-data",
        description="Validate custom ANN model on the actual OpenNebula data",
        tags=["validation", "real-data", "custom-model"],
        version="0.0.1",
        work_pool_name="default-agent-pool",
        work_queue_name="default",
        entrypoint_type=EntrypointType.MODULE_PATH,
    ).apply()

    evaluate_predefined_model_on_synthetic_data.to_deployment(
        name="validate-predefined-model-on-synthetic-data",
        description="Validate one of the predefined ANN models on synthetic "
        "data following one of the predefined profiles",
        tags=["validation", "synthetic-data", "predefined-model"],
        version="0.0.1",
        work_pool_name="default-agent-pool",
        work_queue_name="default",
        entrypoint_type=EntrypointType.MODULE_PATH,
    ).apply()

    evaluate_custom_model_on_synthetic_data.to_deployment(
        name="validate-custom-model-on-synthetic-data",
        description="Validate custom ANN model on synthetic data following "
        "one of the predefined profiles",
        tags=["validation", "real-data", "predefined-model"],
        version="0.0.1",
        work_pool_name="default-agent-pool",
        work_queue_name="default",
        entrypoint_type=EntrypointType.MODULE_PATH,
    ).apply()


def apply_deployments():
    """Apply predefined deployments to be accessible via the dashboard."""
    _apply_validating_deployments()
