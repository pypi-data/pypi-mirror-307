import importlib
import os
from pathlib import Path
from typing import Any, Callable, Literal, Union

import pandas as pd

import pyoneai_ops.mlops.generators.synthetic as synthetic_generators
from pyoneai_ops.mlops.types import SupportedEntities

# TO DO
# 1) Validate data_profile_kwargs
# 2) Validate data_paths for weights and ml_import_path

ML_MODELS_BASE_PATH = "pyoneai.mlmodels"


def validate_literal_param(
    param_name: str, value: Any, valid_values: Union[list, tuple]
):
    if value not in valid_values:
        raise ValueError(
            f"Invalid value for {param_name}: {value}. Expected one of {valid_values}."
        )


def validate_string_param(param_name: str, value: Any):
    if not isinstance(value, str):
        raise TypeError(
            f"Invalid type for {param_name}: {type(value).__name__}. Expected a string."
        )


def validate_boolean_param(param_name: str, value: Any):
    if not isinstance(value, bool):
        raise TypeError(
            f"Invalid type for {param_name}: {type(value).__name__}. Expected a boolean."
        )


def validate_dict_param(param_name: str, value: Any):
    if not isinstance(value, dict):
        raise TypeError(
            f"Invalid type for {param_name}: {type(value).__name__}. Expected a dictionary."
        )


def validate_data_profile(generator: str | Callable):
    if isinstance(generator, str):
        if generator not in synthetic_generators.PROFILES:
            raise ValueError(
                f"Invalid generator name: {generator}. Expected one of {list(synthetic_generators.PROFILES.keys())}."
            )
    elif callable(generator):
        if generator not in [
            getattr(synthetic_generators, gen)
            for gen in synthetic_generators.PROFILES
        ]:
            raise ValueError(
                f"Invalid generator function: {generator.__name__}. The function is not a recognized generator."
            )
    else:
        raise TypeError(
            f"Invalid type for generator: {type(generator).__name__}. Expected a string or a callable."
        )


def validate_path_exist(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path '{path}' does not exist.")


def validate_module_exists(class_path: str):
    try:
        # Split the string to separate the module path from the class name
        module_path, class_name = class_path.rsplit(".", 1)
        print(f"Module path: {module_path}")
        print(f"Class name: {class_name}")

        # Dynamically import the module
        module = importlib.import_module(module_path)

        # Check if the class exists in the module
        if not hasattr(module, class_name):
            raise AttributeError(
                f"The class '{class_name}' does not exist in the module '{module_path}'."
            )

    except ImportError:
        raise ImportError(f"The module '{module_path}' does not exist.")

    except ValueError:
        raise ValueError(
            f"Invalid class path format: {class_path}. Ensure it is in 'module.ClassName' format."
        )

    except AttributeError:
        raise AttributeError(
            f"Failed to find the class '{class_name}' in the module '{module_path}'. Please ensure the class name is correct and properly defined in the module."
        )


def validate_correct_extension(path: str, extension: str):
    if Path(path).suffix != extension:
        raise ValueError(
            f"The file '{path}' does not have the correct extension '{extension}'."
        )


def validate_date_inputs(start_date: str, end_date: str, resolution: str):
    try:
        start_time = pd.Timestamp.now(tz="UTC") + pd.Timedelta(start_date)
    except:
        raise ValueError(
            f"Invalid start date format: '{start_date}'. Expected format is compatible with pandas.Timedelta."
        )

    try:
        end_time = pd.Timestamp.now(tz="UTC") + pd.Timedelta(end_date)
    except:
        raise ValueError(
            f"Invalid end date format: '{end_date}'. Expected format is compatible with pandas.Timedelta."
        )

    try:
        time_resolution = pd.Timedelta(resolution)
    except:
        raise ValueError(
            f"Invalid resolution format: '{resolution}'. Expected format is compatible with pandas.Timedelta."
        )

    try:
        _ = pd.date_range(start=start_time, end=end_time, freq=time_resolution)
    except:
        raise ValueError(
            f"Unable to calculate the timestamps with the given inputs. "
            f"Start date: '{start_date}', End date: '{end_date}', Resolution: '{resolution}'."
        )


def validate_parameters_for_real_data(
    model_name: str | None,
    ml_import_path: str | None,
    weights: str | None,
    entity: SupportedEntities,
    metric_name: Literal["cpu_usage"],
    period: slice,
    mae_score: bool = True,
    mse_score: bool = True,
    rmse_score: bool = True,
    nrmse_score: bool = True,
    r2_score: bool = True,
    spearman_correlation: bool = True,
    mape_score: bool = True,
):
    if model_name:
        validate_string_param("model_name", model_name)
        validate_literal_param(
            "model_name",
            model_name,
            ["transformer", "lstm", "arima", "sarimax", "persistence"],
        )
    validate_literal_param("entity", entity, ["virtualmachine", "host"])
    validate_string_param("entity", entity)
    validate_literal_param("entity", entity, ["virtualmachine", "host"])
    validate_string_param("metric_name", metric_name)
    validate_boolean_param("mae_score", mae_score)
    validate_boolean_param("mse_score", mse_score)
    validate_boolean_param("rmse_score", rmse_score)
    validate_boolean_param("nrmse_score", nrmse_score)
    validate_boolean_param("r2_score", r2_score)
    validate_boolean_param("spearman_correlation", spearman_correlation)
    validate_boolean_param("mape_score", mape_score)
    start_date = period.start
    end_date = period.stop
    resolution = period.step
    validate_string_param("start_date", start_date)
    validate_string_param("end_date", end_date)
    validate_string_param("resolution", resolution)
    validate_date_inputs(start_date, end_date, resolution)
    if ml_import_path is not None:
        validate_string_param("ml_import_path", ml_import_path)
        validate_module_exists(ml_import_path)
        # validate_correct_extension(ml_import_path, "")
    if weights is not None:
        validate_string_param("weights", weights)
        validate_path_exist(weights)
        # validate_correct_extension(weights, "")

    # TO DO -> VALIDATE PERIOD


def validate_parameters_for_synthetic_data(
    model_name: str | None,
    ml_import_path: str | None,
    weights: str | None,
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
    period: slice,
    data_profile_kwargs: dict | None = None,
    mae_score: bool = True,
    mse_score: bool = True,
    rmse_score: bool = True,
    nrmse_score: bool = True,
    r2_score: bool = True,
    spearman_correlation: bool = True,
    mape_score: bool = True,
):
    if model_name:
        validate_string_param("model_name", model_name)
        validate_literal_param(
            "model_name",
            model_name,
            ["transformer", "lstm", "arima", "sarimax", "persistence"],
        )
    validate_literal_param("entity", entity, ["virtualmachine", "host"])
    validate_string_param("entity", entity)
    validate_literal_param("entity", entity, ["virtualmachine", "host"])
    validate_string_param("metric_name", metric_name)
    validate_literal_param("metric_name", metric_name, ["cpu_usage"])
    validate_data_profile(data_profile)
    if data_profile_kwargs is not None:
        validate_dict_param("data_profile_kwargs", data_profile_kwargs)
    validate_boolean_param("mae_score", mae_score)
    validate_boolean_param("mse_score", mse_score)
    validate_boolean_param("rmse_score", rmse_score)
    validate_boolean_param("nrmse_score", nrmse_score)
    validate_boolean_param("r2_score", r2_score)
    validate_boolean_param("spearman_correlation", spearman_correlation)
    validate_boolean_param("mape_score", mape_score)
    start_date = period.start
    end_date = period.stop
    resolution = period.step
    validate_string_param("start_date", start_date)
    validate_string_param("end_date", end_date)
    validate_string_param("resolution", resolution)
    validate_date_inputs(start_date, end_date, resolution)
    if ml_import_path is not None:
        validate_string_param("ml_import_path", ml_import_path)
        validate_module_exists(ml_import_path)
        # validate_correct_extension(ml_import_path, "")
    if weights is not None:
        validate_string_param("weights", weights)
        validate_path_exist(weights)
        # validate_correct_extension(weights, "")

    # TO DO -> VALIDATE PERIOD


def get_predefined_ann_import_path(ann_model: str):
    return f"{ML_MODELS_BASE_PATH}.{ann_model}_model"


def get_selected_validation_metrics(
    mae_score: bool,
    mse_score: bool,
    rmse_score: bool,
    nrmse_score: bool,
    r2_score: bool,
    spearman_correlation: bool,
    mape_score: bool,
):
    metric_flags = {
        "mae": mae_score,
        "mse": mse_score,
        "rmse": rmse_score,
        "nrmse": nrmse_score,
        "r2_score": r2_score,
        "spearman_correlation": spearman_correlation,
        "mape": mape_score,
    }

    return [metric for metric, selected in metric_flags.items() if selected]


def get_model_from_registry(session, entity, metric):
    return session.config.registry[entity][metric]["prediction"]["class"]
