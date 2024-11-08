"""Reporting utilities."""


def _make_markdown_table(metrics: dict[str, float]):
    table = "| Metric | Value |\n|:-------|------:|\n"
    for metric, value in metrics.items():
        table += f"| {metric} | {value:.3f} |\n"
    return table


def prepare_markdown_report_for_synth_eval(
    *, ml_model_name: str, scenario_name: str, metrics: dict[str, float]
):
    markdown_report = f"""# ML method validation report

## Summary

This report presents the evaluation of the {ml_model_name} model on synthetic 
dataset for the {scenario_name} scenario.

Below, you can find the evaluation metrics for the model:
"""
    return markdown_report + _make_markdown_table(metrics)


def prepare_markdown_report_for_real_eval(
    *,
    ml_model_name: str,
    entity: str,
    metric_name: str,
    metrics: dict[str, float],
):
    markdown_report = f"""# ML method validation report

## Summary

This report presents the evaluation of the {ml_model_name} model on real 
dataset for the {entity} entity, {metric_name} metric.

Below, you can find the evaluation metrics for the model:
"""
    return markdown_report + _make_markdown_table(metrics)
