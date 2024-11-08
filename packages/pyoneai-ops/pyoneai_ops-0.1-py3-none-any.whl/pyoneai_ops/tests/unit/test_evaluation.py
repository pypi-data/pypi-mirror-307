from unittest.mock import MagicMock, patch

import pytest

from pyoneai_ops.mlops.core.evaluation import evaluate_on_synthetic_data
from pyoneai_ops.mlops.dataset import (
    OneTimeSeriesDataset,
    SyntheticTimeSeriesDataset,
)


class TestEvaluationSynthetic:

    @pytest.fixture
    def save_path(self):
        yield "checkpoint/checkpoint.ckpt"

    @pytest.fixture(autouse=True)
    def setup_config(self, mocker, save_path):
        from pyoneai_ops.mlops.config import Config

        registry = {
            "virtualmachine": {
                "cpu_usage": {
                    "prediction": {
                        "class": "pyoneai.mlmodels.TransformerModel",
                        "kwargs": {
                            "input_size": 1,
                            "output_size": 1,
                            "in_sequence_length": 24,
                            "nhead": 16,
                            "num_encoder_layers": 5,
                            "num_decoder_layers": 1,
                            "dropout": 0.1,
                            "hidden_dim": 64,
                            "activation": "relu",
                        },
                        "path": save_path,
                    }
                }
            }
        }
        self.session = MagicMock()
        self.session._config.registry = registry

        self.config = Config(
            **{
                "sequence_length": 24,
                "batch_size": 5,
                "epochs": 2,
                "lr": 0.05,
                "weight_decay": 0.01,
            }
        )
        for path in [
            "mlops.dataset.get_config",
            "mlops.drivers.lightning.get_config",
            "mlops.drivers.base.get_config",
        ]:

            mocker.patch(
                path,
                return_value=self.config,
            )

    @pytest.fixture(autouse=True)
    def setup_synthetic_time_series_dataset(self):
        oneinisght_obj = MagicMock()
        self.vm_synthetic_dataset = SyntheticTimeSeriesDataset(
            oneinisght_obj,
            slice("-1d10m", "+1d10m", "1h"),
            "random_workload",
        )
        yield

    @pytest.fixture
    def valid_period(self):
        return slice("-1d10m", "+1d10m", "1h")

    @pytest.fixture
    def valid_data_profile_kwargs(self):
        # return {"some_key": "some_value"}
        return None

    @pytest.fixture
    def invalid_data_profile_kwargs(self):
        return {"bad_key": "bad_value"}

    @pytest.mark.skip
    def test_evaluate_predefined_model_on_synthetic_data_with_all_parameters(
        self, valid_period, valid_data_profile_kwargs
    ):
        evaluate_on_synthetic_data(
            session=self.session,
            entity="virtualmachine",
            metric_name="cpu_usage",
            data_profile="random_workload",
            period=valid_period,  # BE SURE THAT DELETEING ONEAIOPS WILL WORK.
            weights="home/marchostau/Desktop/OpenNebula/temporaryModel/checkpoint.ckpt",  # MOCK IT (DON'T SPECIFY CUSTOM PATHS)
            data_profile_kwargs=valid_data_profile_kwargs,
            mae_score=True,
            mse_score=True,
            rmse_score=True,
            nrmse_score=True,
            r2_score=True,
            spearman_correlation=True,
            mape_score=True,
        )

    @pytest.mark.skip
    def test_evaluate_predefined_model_on_synthetic_data_without_weights(
        self, session, valid_period, valid_data_profile_kwargs
    ):
        evaluate_on_synthetic_data(
            session=session,
            entity="virtualmachine",
            metric_name="cpu_usage",
            data_profile="random_workload",
            period=valid_period,
            weights=None,
            data_profile_kwargs=valid_data_profile_kwargs,
            mae_score=True,
            mse_score=True,
            rmse_score=True,
            nrmse_score=True,
            r2_score=True,
            spearman_correlation=True,
            mape_score=True,
        )

    @pytest.mark.skip
    def test_evaluate_predefined_model_on_synthetic_data_with_invalid_weights():
        pass

    @pytest.mark.skip
    def test_evaluate_predefined_model_on_synthetic_data_without_data_profile(
        self, session, valid_period, valid_data_profile_kwargs
    ):
        with pytest.raises(ValueError):  # Replace ValueError for the expected
            evaluate_on_synthetic_data(
                session=session,
                entity="virtualmachine",
                metric_name="cpu_usage",
                data_profile=None,
                period=valid_period,
                weights="path/to/weights.ckpt",
                data_profile_kwargs=valid_data_profile_kwargs,
                mae_score=True,
                mse_score=True,
                rmse_score=True,
                nrmse_score=True,
                r2_score=True,
                spearman_correlation=True,
                mape_score=True,
            )

    @pytest.mark.skip
    def test_evaluate_predefined_model_on_synthetic_data_with_invalid_data_profile_kwargs(
        self, session, valid_period, invalid_data_profile_kwargs
    ):
        with pytest.raises(ValueError):  # Replace ValueError for the expected
            evaluate_on_synthetic_data(
                session=session,
                entity="virtualmachine",
                metric_name="cpu_usage",
                data_profile="random_workload",
                period=valid_period,
                weights="path/to/weights.ckpt",
                data_profile_kwargs=invalid_data_profile_kwargs,
                mae_score=True,
                mse_score=True,
                rmse_score=True,
                nrmse_score=True,
                r2_score=True,
                spearman_correlation=True,
                mape_score=True,
            )

    @pytest.mark.skip
    def test_evaluate_predefined_model_on_synthetic_data_with_all_booleans_false(
        self, session, valid_period, valid_data_profile_kwargs
    ):
        evaluate_on_synthetic_data(
            session=session,
            entity="virtualmachine",
            metric_name="cpu_usage",
            data_profile="random_workload",
            period=valid_period,
            weights="path/to/weights.ckpt",
            data_profile_kwargs=valid_data_profile_kwargs,
            mae_score=False,
            mse_score=False,
            rmse_score=False,
            nrmse_score=False,
            r2_score=False,
            spearman_correlation=False,
            mape_score=False,
        )

    @pytest.mark.skip
    def test_evaluate_predefined_model_on_synthetic_data_with_invalid_period():
        pass

    @pytest.mark.skip
    def test_evaluate_predefined_model_on_synthetic_data_with_invalid_weight_in_registry():
        pass

    @pytest.mark.skip
    def test_evaluate_predefined_model_on_synthetic_data_with_invalid_ann_path_in_registry():
        pass

    @pytest.mark.skip
    def test_evaluate_predefined_model_on_synthetic_data_with_invalid_session():
        pass

    @pytest.mark.skip
    def test_evaluate_predefined_model_on_synthetic_data_with_invalid_model_args():
        pass
