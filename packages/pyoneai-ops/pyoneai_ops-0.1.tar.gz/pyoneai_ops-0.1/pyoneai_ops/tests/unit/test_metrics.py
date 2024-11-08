import numpy as np
import pytest
import torch

from pyoneai_ops.mlops.metrics import (
    compute_mae,
    compute_mape,
    compute_mse,
    compute_nrmse,
    compute_r2_score,
    compute_report,
    compute_rmse,
    compute_spearman_correlation,
    to_tensor,
    validate_shapes,
    validate_types,
)


class TestMetrics:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.y_true = np.array(
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        )
        self.y_pred = np.array(
            [1.1, 2.1, 2.9, 4.2, 5.4, 6.4, 7.4, 8.0, 9.7, 10.5]
        )
        self.y_true_tensor = torch.tensor(self.y_true)
        self.y_pred_tensor = torch.tensor(self.y_pred)

        self.y_true_tensor_samples = torch.tensor(
            [
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
            ]
        )
        self.y_pred_tensor_samples = torch.tensor(
            [
                [1.1, 2.1, 2.9, 4.2, 5.4, 6.4, 7.4, 8.0, 9.7, 10.5],
                [1.1, 2.1, 2.9, 4.2, 5.4, 6.4, 7.4, 8.0, 9.7, 10.5],
                [1.1, 2.1, 2.9, 4.2, 5.4, 6.4, 7.4, 8.0, 9.7, 10.5],
                [1.1, 2.1, 2.9, 4.2, 5.4, 6.4, 7.4, 8.0, 9.7, 10.5],
            ]
        )

        self.y_true_numpy_samples = np.array(
            [
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
            ]
        )
        self.y_pred_numpy_samples = np.array(
            [
                [1.1, 2.1, 2.9, 4.2, 5.4, 6.4, 7.4, 8.0, 9.7, 10.5],
                [1.1, 2.1, 2.9, 4.2, 5.4, 6.4, 7.4, 8.0, 9.7, 10.5],
            ]
        )

    def test_compute_mae(self):
        mae = compute_mae(self.y_true, self.y_pred)
        assert np.isclose(mae, 0.29)

    def test_compute_mse(self):
        mse = compute_mse(self.y_true, self.y_pred)
        assert np.isclose(mse, 0.12900)

    def test_compute_rmse(self):
        rmse = compute_rmse(self.y_true, self.y_pred)
        assert np.isclose(rmse, np.sqrt(0.12900))

    def test_compute_r2_score(self):
        r2 = compute_r2_score(self.y_true, self.y_pred)
        assert np.isclose(r2, 0.984, atol=1e-3)

    def test_compute_spearman_correlation(self):
        spearman_corr = compute_spearman_correlation(self.y_true, self.y_pred)
        assert np.isclose(spearman_corr, 1)

    def test_compute_mape(self):
        mape = compute_mape(self.y_true, self.y_pred)
        assert np.isclose(mape, 5.6492, atol=1e-6)

    def test_compute_nrmse(self):
        nrmse = compute_nrmse(self.y_true, self.y_pred)
        assert np.isclose(nrmse, np.sqrt(0.12900) / (10.0 - 1.0), atol=1e-6)

    def test_returning_keys_compute_report(self):
        report = compute_report(self.y_true, self.y_pred)
        assert isinstance(report, dict)
        assert set(report.keys()) == {
            "MAE",
            "MSE",
            "RMSE",
            "MAPE",
            "NRMSE",
            "R2 Score",
            "Spearman Correlation",
        }

    @pytest.mark.parametrize(
        "y_pred, y_true",
        [
            (np.array([1.1, 1.9, 3.2]), np.array([1.0, 2.0])),
            (np.array([[1.1, 1.9, 3.2]]), np.array([1.0, 2.0])),
            (torch.tensor([1.1, 1.9, 3.2]), torch.tensor([1.0, 2.0])),
        ],
    )
    def test_validate_shape_fail_on_shape_mismatch(self, y_true, y_pred):
        y_true, y_pred = to_tensor(y_true), to_tensor(y_pred)
        with pytest.raises(
            ValueError, match="Shapes of y_true and y_pred must match"
        ):
            validate_shapes(y_true, y_pred)

    @pytest.mark.parametrize(
        "y_pred, y_true",
        [(np.array([]), np.array([])), (torch.tensor([]), torch.tensor([]))],
    )
    def test_validate_shape_fail_on_empty_array(self, y_true, y_pred):
        y_true, y_pred = to_tensor(y_true), to_tensor(y_pred)
        with pytest.raises(ValueError, match="Arrays must not be empty."):
            validate_shapes(y_true, y_pred)

    @pytest.mark.parametrize(
        "y_pred, y_true",
        [
            (np.array([1.1, 1.9, 3.2]), torch.tensor([1.0, 2.0, 3.0])),
            (torch.tensor([1.1, 1.9, 3.2]), np.array([1.0, 2.0, 3.0])),
        ],
    )
    def test_validate_types_fail_on_types_mismatch(self, y_true, y_pred):
        with pytest.raises(TypeError):
            validate_types(y_true, y_pred)

    @pytest.mark.parametrize(
        "y_pred, y_true",
        [
            ([1.1, 1.9, 3.2], [1.0, 2.0, 3.0]),
            ((1.1, 1.9, 3.2), (1.0, 2.0, 3.0)),
        ],
    )
    def test_validate_types_fail_on_wrong_type(self, y_true, y_pred):
        with pytest.raises(TypeError):
            validate_types(y_true, y_pred)

    @pytest.mark.parametrize(
        "metric_fn, expected_result",
        [
            (compute_mae, 0.1),
            (compute_mse, 0.01),
            (compute_rmse, np.sqrt(0.01)),
            (compute_mape, 10),
            (compute_nrmse, float("inf")),
            (compute_spearman_correlation, 0.0),
        ],
    )
    def test_single_element_input_arrays_results(
        self, metric_fn, expected_result
    ):
        y_true = np.array([1.0])
        y_pred = np.array([1.1])

        result = metric_fn(y_true, y_pred)
        assert isinstance(result, float)
        assert np.isclose(result, expected_result)

    def test_single_element_input_arrays_result_for_r2(self):
        y_true = torch.tensor([1.0])
        y_pred = torch.tensor([1.1])

        with pytest.warns(
            match="R2 score cannot be computed with only one sample."
        ):
            result = compute_r2_score(y_true, y_pred)
            assert float("nan")

    @pytest.mark.parametrize(
        "metric_fn",
        [
            compute_mae,
            compute_mse,
            compute_rmse,
            compute_r2_score,
            compute_mape,
            compute_nrmse,
            compute_spearman_correlation,
        ],
    )
    def test_float_returning_type(self, metric_fn):
        y_true = np.array([1.0, 2.0])
        y_pred = np.array([1.1, 2.4])
        result = metric_fn(y_true, y_pred)
        assert isinstance(result, float)

        y_true = np.array([[1.0, 2.0]])
        y_pred = np.array([[1.1, 2.4]])
        result = metric_fn(y_true, y_pred)
        assert isinstance(result, float)

    @pytest.mark.parametrize(
        "metric_fn, expected_result",
        [
            (compute_mae, 0.29),
            (compute_mse, 0.12900),
            (compute_rmse, 0.3591),
            (compute_r2_score, 0.9843),
            (compute_mape, 5.6492),
            (compute_nrmse, 0.0399),
            (compute_spearman_correlation, 1.0),
        ],
    )
    def test_tensor_input_with_samples_returning_output(
        self, metric_fn, expected_result
    ):
        SAMPLES = 4
        result = metric_fn(
            self.y_true_tensor_samples, self.y_pred_tensor_samples
        )
        assert torch.allclose(
            result, torch.tensor([expected_result] * SAMPLES), atol=1e-4
        )

    @pytest.mark.parametrize(
        "metric_fn",
        [
            (compute_mae),
            (compute_mse),
            (compute_rmse),
            (compute_r2_score),
            (compute_mape),
            (compute_nrmse),
            (compute_spearman_correlation),
        ],
    )
    def test_tensor_input_with_samples_returning_shape(self, metric_fn):
        SAMPLES = 4
        result = metric_fn(
            self.y_true_tensor_samples, self.y_pred_tensor_samples
        )
        assert result.shape[0] == SAMPLES

    @pytest.mark.parametrize(
        "metric_fn",
        [
            (compute_mae),
            (compute_mse),
            (compute_rmse),
            (compute_r2_score),
            (compute_mape),
            (compute_nrmse),
            (compute_spearman_correlation),
        ],
    )
    def test_tensor_input_with_samples_returning_type(self, metric_fn):
        result = metric_fn(
            self.y_true_tensor_samples, self.y_pred_tensor_samples
        )
        assert isinstance(result, torch.Tensor)

    @pytest.mark.parametrize(
        "metric_fn, expected_result",
        [
            (compute_mae, 0.29),
            (compute_mse, 0.12900),
            (compute_rmse, np.sqrt(0.12900)),
            (compute_r2_score, 0.9843),
            (compute_mape, 5.6492),
            (compute_nrmse, np.sqrt(0.12900) / (10.0 - 1.0)),
            (compute_spearman_correlation, 1.0),
        ],
    )
    def test_numpy_input_with_samples_returning_output(
        self, metric_fn, expected_result
    ):
        SAMPLES = 2
        result = metric_fn(
            self.y_true_numpy_samples, self.y_pred_numpy_samples
        )
        assert np.allclose(
            result, np.array([expected_result] * SAMPLES), atol=1e-3
        )

    @pytest.mark.parametrize(
        "metric_fn",
        [
            (compute_mae),
            (compute_mse),
            (compute_rmse),
            (compute_r2_score),
            (compute_mape),
            (compute_nrmse),
            (compute_spearman_correlation),
        ],
    )
    def test_numpy_input_with_samples_returning_shape(self, metric_fn):
        SAMPLES = 2
        result = metric_fn(
            self.y_true_numpy_samples, self.y_pred_numpy_samples
        )
        assert result.shape[0] == SAMPLES

    @pytest.mark.parametrize(
        "metric_fn",
        [
            (compute_mae),
            (compute_mse),
            (compute_rmse),
            (compute_r2_score),
            (compute_mape),
            (compute_nrmse),
            (compute_spearman_correlation),
        ],
    )
    def test_numpy_input_with_samples_returning_type(self, metric_fn):
        result = metric_fn(
            self.y_true_numpy_samples, self.y_pred_numpy_samples
        )
        assert isinstance(result, np.ndarray)

    @pytest.mark.parametrize(
        "metric_fn, expected_result",
        [
            (compute_mae, 0.0),
            (compute_mse, 0.0),
            (compute_rmse, 0.0),
            (compute_mape, 0.0),
            (compute_nrmse, float("nan")),
            (compute_spearman_correlation, 0.0),
        ],
    )
    def test_scalar_input(self, metric_fn, expected_result):
        y_true = np.array(3.0)
        y_pred = np.array(3.0)
        y_true = to_tensor(y_true)
        y_pred = to_tensor(y_pred)

        result = metric_fn(y_true, y_pred)

        if np.isnan(expected_result):
            assert np.isnan(result)
        else:
            assert np.isclose(result, expected_result)
