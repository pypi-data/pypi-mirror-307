from unittest.mock import MagicMock, patch

import pytest

from pyoneai_ops.mlops.core.utils import (
    validate_correct_extension,
    validate_date_inputs,
    validate_parameters_for_synthetic_data,
    validate_path_exist,
)


class TestValidating:

    def test_evaluate_predefined_model_on_synthetic_data_invalid_ann_path_type(
        self,
    ):
        with pytest.raises(TypeError):
            validate_parameters_for_synthetic_data(
                ml_import_path=123,
                weights="some_path",
            )

    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_invalid_weight_type(
        self, mock_exists
    ):
        with pytest.raises(TypeError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path",
                weights=12345,
            )

    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_invalid_entity_type(
        self, mock_exists
    ):
        with pytest.raises(TypeError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path",
                weights="some_path",
                entity=111,
            )

    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_invalid_metric_type(
        self, mock_exists
    ):
        with pytest.raises(TypeError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path",
                weights="some_path",
                metric_name=111,
            )

    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_invalid_data_profile_type(
        self, mock_exists
    ):
        with pytest.raises(TypeError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path",
                weights="some_path",
                data_profile=111,
            )

    @pytest.mark.skip
    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_invalid_data_profile_str(
        self, mock_exists
    ):
        with pytest.raises(ValueError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path",
                weights="some_path",
                data_profile="invalid_generator",
            )

    @pytest.mark.skip
    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_invalid_data_profile_callable(
        self, mock_exists
    ):
        def invalid_generator():
            yield

        with pytest.raises(ValueError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path",
                weights="some_path",
                data_profile=invalid_generator,
            )

    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_invalid_data_profile_kwargs_type(
        self, mock_exists
    ):
        with pytest.raises(TypeError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path",
                weights="some_path",
                data_profile_kwargs=111,
            )

    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_invalid_start_type(
        self, mock_exists
    ):
        with pytest.raises(TypeError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path", weights="some_path", start_date=1
            )

    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_invalid_end_type(
        self, mock_exists
    ):
        with pytest.raises(TypeError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path", weights="some_path", end=1
            )

    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_invalid_resolution_type(
        self, mock_exists
    ):
        with pytest.raises(TypeError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path", weights="some_path", resolution=23
            )

    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_invalid_score_type(
        self, mock_exists
    ):
        with pytest.raises(TypeError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path", weights="some_path", mae_score=2
            )

    @pytest.mark.skip
    @patch("os.path.exists", return_value=True)
    def test_process_on_synthetic_data_invalid_entity(self, mock_exists):
        with pytest.raises(ValueError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path",
                weights="some_path",
                entity="invalid_entity",
            )

    @pytest.mark.skip
    @patch("os.path.exists", return_value=True)
    def test_process_on_synthetic_data_invalid_metric_name(self, mock_exists):
        with pytest.raises(ValueError):
            validate_parameters_for_synthetic_data(
                ml_import_path="some_path",
                weights="some_path",
                metric_name="invalid_metric",
            )

    @patch("os.path.exists", return_value=True)
    def test_evaluate_date_inputs_invalid_start_date(self, mock_exists):
        with pytest.raises(ValueError, match="Invalid start date format"):
            validate_date_inputs(
                start_date="invalid_date",
                end_date="invalid_date",
                resolution="10s",
            )

    @patch("os.path.exists", return_value=True)
    def test_evaluate_date_inputs_invalid_end_date(self, mock_exists):
        with pytest.raises(ValueError, match="Invalid end date format"):
            validate_date_inputs(
                start_date="-3d", end_date="invalid_date", resolution="10s"
            )

    @patch("os.path.exists", return_value=True)
    def test_evaluate_date_inputs_invalid_resolution(self, mock_exists):
        with pytest.raises(ValueError, match="Invalid resolution format"):
            validate_date_inputs(
                start_date="-3d",
                end_date="-1d",
                resolution="invalid_resolution",
            )

    @patch("os.path.exists", return_value=False)
    def test_validate_invalid_ann_path_exist_raises_error(self, mock_exists):
        with pytest.raises(
            FileNotFoundError,
            match="The path 'ann_non_existent_path' does not exist.",
        ):
            validate_path_exist("ann_non_existent_path")

    @patch("os.path.exists", return_value=False)
    def test_validate_invalid_weight_path_exist_raises_error(
        self, mock_exists
    ):
        with pytest.raises(
            FileNotFoundError,
            match="The path 'weight_non_existent_path' does not exist.",
        ):
            validate_path_exist("weight_non_existent_path")

    @pytest.mark.skip
    def test_evaluate_invalid_ann_path_extension_raises_error(self):
        with pytest.raises(
            ValueError,
            match="The file 'some_path.txt' does not have the correct extension '.csv'.",
        ):
            # validate_correct_extension("ann_model.?", ".?")
            pass

    @pytest.mark.skip
    def test_evaluate_invalid_weight_path_extension_raises_error(self):
        with pytest.raises(
            ValueError,
            match="The file 'some_path.txt' does not have the correct extension '.csv'.",
        ):
            # validate_correct_extension("weight.?", ".?")
            pass

    @pytest.mark.skip
    @patch("os.path.exists", return_value=True)
    def test_validate_valid_ann_path_exist(self, mock_exists):
        try:
            validate_path_exist("ann_existent_path")
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")

    @pytest.mark.skip
    @patch("os.path.exists", return_value=True)
    def test_validate_valid_weight_path_exist_raises_error(self, mock_exists):
        try:
            validate_path_exist("weight_existent_path")
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")

    @pytest.mark.skip
    def test_evaluate_valid_ann_path_extension(self):
        with pytest.raises(
            ValueError,
            match="The file 'some_path.txt' does not have the correct extension '.csv'.",
        ):
            try:
                # validate_correct_extension("ann_model.?", ".?")
                pass
            except Exception as e:
                pytest.fail(f"Unexpected exception raised: {e}")

    @pytest.mark.skip
    def test_evaluate_valid_weight_path_extension(self):
        with pytest.raises(
            ValueError,
            match="The file 'some_path.txt' does not have the correct extension '.csv'.",
        ):
            try:
                # validate_correct_extension("weight.?", ".?")
                pass
            except Exception as e:
                pytest.fail(f"Unexpected exception raised: {e}")

    @pytest.mark.skip
    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_valid_entity(
        self, mock_exists
    ):
        try:
            validate_parameters_for_synthetic_data(
                ml_import_path="some_valid_path",
                weights="some_valid_path",
                entity="virtualmachine",
            )
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")

    @pytest.mark.skip
    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_valid_metric_name(
        self, mock_exists
    ):
        try:
            validate_parameters_for_synthetic_data(
                ml_import_path="some_valid_path",
                weights="some_valid_path",
                metric_name="cpu_usage",
            )
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")

    @pytest.mark.skip
    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_valid_data_profile_str(
        self, mock_exists
    ):
        try:
            validate_parameters_for_synthetic_data(
                ml_import_path="some_valid_path",
                weights="some_valid_path",
                data_profile="random_workload",
            )
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")

    @pytest.mark.skip
    @patch("os.path.exists", return_value=True)
    def test_evaluate_predefined_model_on_synthetic_data_valid_data_profile_callable(
        self, mock_exists
    ):
        from pyoneai_ops.mlops.generators.synthetic import random_workload

        try:
            validate_parameters_for_synthetic_data(
                ml_import_path="some_valid_path",
                weights="some_valid_path",
                data_profile=random_workload,
            )
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")

    @patch("os.path.exists", return_value=True)
    def test_validate_correct_ann_path(self, mock_exists):
        try:
            validate_path_exist("some_valid_path")
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")

    @patch("os.path.exists", return_value=True)
    def test_validate_correct_weight_path(self, mock_exists):
        try:
            validate_path_exist("some_valid_path")
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")

    def test_evaluate_date_inputs_valid_dates(self):
        try:
            validate_date_inputs(
                start_date="-3d",
                end_date="-1d",
                resolution="10s",
            )
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")
