from datetime import datetime, timezone

from prefect import flow, task
from prefect.artifacts import create_markdown_artifact

import pyoneai_ops.mlops.core.reporting
from pyoneai_ops.mlops.config import get_config
from pyoneai_ops.mlops.utils import generate_flow_run_name

config = get_config()


# #########################
#          TASKS
# #########################
@task(retries=config.retries, retry_delay_seconds=config.retry_delay_seconds)
def _make_markdown_table(metrics: dict[str, float]):
    return mlops.core.reporting._make_markdown_table(metrics=metrics)


# #########################
#          FLOWS
# #########################
@flow(
    description="Prepare markdown report artifact for synthetic datasets",
    generate_flow_run_name=generate_flow_run_name,
    retries=config.retries,
    retry_delay_seconds=config.retry_delay_seconds,
)
def prepare_markdown_report_for_synthetic_datasets(
    *, ml_model_name: str, scenario_name: str, metrics: dict[str, float]
):
    markdown = (
        mlops.core.reporting.prepare_markdown_report_for_synthetic_datasets(
            ml_model_name=ml_model_name,
            scenario_name=scenario_name,
            metrics=metrics,
        )
    )
    create_markdown_artifact(
        key=f"evaluation-report-real-{ml_model_name}-{scenario_name}-"
        f"{datetime.now(timezone.utc).isoformat()}",
        markdown=markdown,
        description="ML Evaluation report on synthetic data",
    )


@flow(
    description="Prepare markdown report artifact for real datasets",
    generate_flow_run_name=generate_flow_run_name,
    retries=config.retries,
    retry_delay_seconds=config.retry_delay_seconds,
)
def prepare_markdown_report_for_real_datasets(
    *,
    ml_model_name: str,
    entity: str,
    metric_name: str,
    metrics: dict[str, float],
):
    markdown = mlops.core.reporting.prepare_markdown_report_for_real_datasets(
        ml_model_name=ml_model_name,
        entity=entity,
        metric_name=metric_name,
        metrics=metrics,
    )
    create_markdown_artifact(
        key=f"evaluation-report-real-{ml_model_name}-{entity}/{metric_name}-"
        f"{datetime.now(timezone.utc).isoformat()}",
        markdown=markdown,
        description="ML Evaluation report on real data",
    )
