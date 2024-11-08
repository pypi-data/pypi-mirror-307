__all__ = [
    "get_metric_callable",
    "compute_mae",
    "compute_mse",
    "compute_rmse",
    "compute_nrmse",
    "compute_r2_score",
    "compute_spearman_correlation",
    "compute_mape",
    "compute_report",
    "METRICS",
]
import warnings
from typing import Callable, Dict, Union

import numpy as np
import numpy.typing as npt

try:
    import torch
    import torchmetrics.functional as F
except ImportError:
    _HAS_TORCH = False
else:
    _HAS_TORCH = True



def to_tensor(y):
    return torch.tensor(y) if isinstance(y, np.ndarray) else y


def validate_types(y_true, y_pred) -> None:
    if not (
        (isinstance(y_true, torch.Tensor) and isinstance(y_pred, torch.Tensor))
        or (isinstance(y_true, np.ndarray) and isinstance(y_pred, np.ndarray))
    ):
        raise TypeError(
            "Inputs must be both torch tensors or both numpy arrays."
        )

def validate_shapes(y_true, y_pred) -> None:
    if y_true.ndimension() == 0 and y_pred.ndimension() == 0:
        return
    if y_true.shape != y_pred.shape:
        raise ValueError(f"Shapes of y_true and y_pred must match.")
    if y_true.shape[0] == 0 or y_pred.shape[0] == 0:
        raise ValueError("Arrays must not be empty.")

def squeeze_inputs(y_true, y_pred) -> 'torch.Tensor':
    y_true = y_true.squeeze()
    y_pred = y_pred.squeeze()

    # Ensure the tensors are not squeezed to 0-d in cases (1,1) and (1)
    if y_true.ndimension() == 0:
        y_true = y_true.unsqueeze(0)
        y_pred = y_pred.unsqueeze(0)

    return y_true, y_pred

def compute_mae(
    y_true: Union['torch.Tensor', npt.NDArray],
    y_pred: Union['torch.Tensor', npt.NDArray],
) -> Union[float, 'torch.Tensor', npt.NDArray]:
    validate_types(y_true, y_pred)
    y_true_t, y_pred_t = to_tensor(y_true), to_tensor(y_pred)
    validate_shapes(y_true_t, y_pred_t)
    y_true_t, y_pred_t = squeeze_inputs(y_true_t, y_pred_t)

    if y_true_t.ndimension() == 1:
        return F.mean_absolute_error(y_pred_t, y_true_t).item()
    else:
        maes = [
            F.mean_absolute_error(y_pred_sample, y_true_sample)
            for y_pred_sample, y_true_sample in zip(y_pred_t, y_true_t)
        ]
        return (
            np.array(maes)
            if isinstance(y_true, np.ndarray)
            else torch.tensor(maes)
    )

def compute_mse(
    y_true: Union['torch.Tensor', npt.NDArray],
    y_pred: Union['torch.Tensor', npt.NDArray],
) -> Union[float, 'torch.Tensor', npt.NDArray]:
    validate_types(y_true, y_pred)
    y_true_t, y_pred_t = to_tensor(y_true), to_tensor(y_pred)
    validate_shapes(y_true_t, y_pred_t)
    y_true_t, y_pred_t = squeeze_inputs(y_true_t, y_pred_t)

    if y_true_t.ndimension() == 1:
        return F.mean_squared_error(y_pred_t, y_true_t).item()
    else:
        mses = [
            F.mean_squared_error(y_pred_sample, y_true_sample)
            for y_pred_sample, y_true_sample in zip(y_pred_t, y_true_t)
        ]
        return (
            np.array(mses)
            if isinstance(y_true, np.ndarray)
            else torch.tensor(mses)
        )


def compute_rmse(
    y_true: Union['torch.Tensor', npt.NDArray],
    y_pred: Union['torch.Tensor', npt.NDArray],
) -> Union[float, 'torch.Tensor', npt.NDArray]:
    validate_types(y_true, y_pred)
    y_true_t, y_pred_t = to_tensor(y_true), to_tensor(y_pred)
    validate_shapes(y_true_t, y_pred_t)
    y_true_t, y_pred_t = squeeze_inputs(y_true_t, y_pred_t)
    mse = compute_mse(y_true, y_pred)
    return mse**0.5


def compute_nrmse(
    y_true: Union['torch.Tensor', npt.NDArray],
    y_pred: Union['torch.Tensor', npt.NDArray],
) -> Union[float, 'torch.Tensor', npt.NDArray]:
    validate_types(y_true, y_pred)
    y_true_t, y_pred_t = to_tensor(y_true), to_tensor(y_pred)
    validate_shapes(y_true_t, y_pred_t)
    y_true_t, y_pred_t = squeeze_inputs(y_true_t, y_pred_t)

    rmses = compute_rmse(y_true_t, y_pred_t)

    if y_true_t.ndimension() == 1:
        y_min, y_max = torch.min(y_true_t), torch.max(y_true_t)
        range_y = y_max - y_min
        return (rmses / range_y).item()
    else:
        y_mins = [torch.min(y_true_sample) for y_true_sample in y_true_t]
        y_maxs = [torch.max(y_true_sample) for y_true_sample in y_true_t]
        ranges_y = [(y_max - y_min) for y_min, y_max in zip(y_mins, y_maxs)]
        nrmses = [rmse / range_y for rmse, range_y in zip(rmses, ranges_y)]
        return (
            np.array(nrmses)
            if isinstance(y_true, np.ndarray)
            else torch.tensor(nrmses)
        )


def compute_r2_score(
    y_true: Union['torch.Tensor', npt.NDArray],
    y_pred: Union['torch.Tensor', npt.NDArray],
) -> Union[float, 'torch.Tensor', npt.NDArray]:
    validate_types(y_true, y_pred)
    y_true_t, y_pred_t = to_tensor(y_true), to_tensor(y_pred)
    validate_shapes(y_true_t, y_pred_t)
    y_true_t, y_pred_t = squeeze_inputs(y_true_t, y_pred_t)

    if y_true_t.ndimension() == 1:
        if y_true_t.numel() == 1:
            warnings.warn("R2 score cannot be computed with only one sample.")
            return float("nan")
        return F.r2_score(y_pred_t, y_true_t).item()
    else:
        r2_scores = []
        for y_pred_sample, y_true_sample in zip(y_pred_t, y_true_t):
            if y_true_sample.numel() == 1:
                warnings.warn(
                    "R2 score cannot be computed with only one sample in this batch."
                )
                r2_scores.append(
                    float("nan")
                )  # Append NaN for invalid calculations
            else:
                r2_scores.append(F.r2_score(y_pred_sample, y_true_sample))
        return (
            np.array(r2_scores)
            if isinstance(y_true, np.ndarray)
            else torch.tensor(r2_scores)
    )


def compute_spearman_correlation(
    y_true: Union['torch.Tensor', npt.NDArray],
    y_pred: Union['torch.Tensor', npt.NDArray],
) -> Union[float, 'torch.Tensor', npt.NDArray]:
    validate_types(y_true, y_pred)
    y_true_t, y_pred_t = to_tensor(y_true), to_tensor(y_pred)
    validate_shapes(y_true_t, y_pred_t)
    y_true_t, y_pred_t = squeeze_inputs(y_true_t, y_pred_t)

    if y_true_t.ndimension() == 1:
        return F.spearman_corrcoef(y_pred_t, y_true_t).item()
    else:
        spearman_corrs = [
            F.spearman_corrcoef(y_pred_sample, y_true_sample)
            for y_pred_sample, y_true_sample in zip(y_pred_t, y_true_t)
        ]
        return (
            np.array(spearman_corrs)
            if isinstance(y_true, np.ndarray)
            else torch.tensor(spearman_corrs)
        )


def compute_mape(
    y_true: Union['torch.Tensor', npt.NDArray],
    y_pred: Union['torch.Tensor', npt.NDArray],
) -> Union[float, 'torch.Tensor', npt.NDArray]:
    validate_types(y_true, y_pred)
    y_true_t, y_pred_t = to_tensor(y_true), to_tensor(y_pred)
    validate_shapes(y_true_t, y_pred_t)
    y_true_t, y_pred_t = squeeze_inputs(y_true_t, y_pred_t)

    if y_true_t.ndimension() == 1:
        return (
            F.mean_absolute_percentage_error(y_pred_t, y_true_t).item() * 100
        )
    else:
        mapes = [
            F.mean_absolute_percentage_error(y_pred_sample, y_true_sample)
            * 100
            for y_pred_sample, y_true_sample in zip(y_pred_t, y_true_t)
        ]
        return (
            np.array(mapes)
            if isinstance(y_true, np.ndarray)
            else torch.tensor(mapes)
        )


def compute_report(
    y_true: Union['torch.Tensor', npt.NDArray],
    y_pred: Union['torch.Tensor', npt.NDArray],
) -> Dict[str, Union[float, 'torch.Tensor', npt.NDArray]]:
    return {
        "MAE": compute_mae(y_true, y_pred),
        "MSE": compute_mse(y_true, y_pred),
        "RMSE": compute_rmse(y_true, y_pred),
        "MAPE": compute_mape(y_true, y_pred),
        "NRMSE": compute_nrmse(y_true, y_pred),
        "R2 Score": compute_r2_score(y_true, y_pred),
        "Spearman Correlation": compute_spearman_correlation(y_true, y_pred),
    }


METRICS = {
    "mae": compute_mae,
    "mse": compute_mse,
    "rmse": compute_rmse,
    "nrmse": compute_nrmse,
    "r2": compute_r2_score,
    "spearman_correlation": compute_spearman_correlation,
    "mape": compute_mape,
}


def get_metric_callable(name: str) -> Callable:
    name = name.lower()
    if name not in METRICS:
        raise ValueError(f"Metric {name} is not supported")
    return METRICS[name]
