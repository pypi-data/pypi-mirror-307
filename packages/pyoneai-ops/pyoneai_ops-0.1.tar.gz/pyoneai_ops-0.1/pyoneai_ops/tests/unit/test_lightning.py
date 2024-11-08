import os
import shutil
from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest
import torch

from pyoneai_ops.mlops.dataset import SyntheticTimeSeriesDataset
from pyoneai_ops.mlops.generators.synthetic import random_workload


@pytest.mark.filterwarnings("ignore")
class TestLightningTrainer:

    @pytest.fixture
    def mlmodels_path(self):
        yield "./mlmodels"

    @pytest.fixture
    def save_path(self):
        yield "checkpoint/checkpoint.ckpt"

    @pytest.fixture(autouse=True)
    def clear(self, save_path, mlmodels_path):
        yield
        if os.path.exists(save_path):
            shutil.rmtree(os.path.dirname(save_path), ignore_errors=True)
        if os.path.exists(mlmodels_path):
            shutil.rmtree(mlmodels_path, ignore_errors=True)

    @pytest.fixture(autouse=True)
    def common_setup(self, mocker, save_path, mlmodels_path):
        from pyoneai_ops.mlops.config import Config

        self.session = MagicMock()
        self.session.config.model_path = mlmodels_path

        self.config = Config(
            **{
                "sequence_length": 24,
                "models": {
                    "pyoneai.mlmodels.TransformerModel": {
                        "training": {
                            "lr": 0.05,
                            "weight_decay": 0.01,
                            "batch_size": 5,
                            "epochs": 2,
                            "num_workers": 0,
                        },
                        "hparams": {
                            "input_size": 1,
                            "output_size": 1,
                            "in_sequence_length": 24,
                            "num_encoder_layers": 1,
                            "num_decoder_layers": 1,
                            "dropout": 0.0,
                            "hidden_dim": 64,
                            "nhead": 16,
                            "activation": "relu",
                        },
                    }
                },
            }
        )
        for path in [
            "pyoneai_ops.mlops.dataset.get_config",
            "pyoneai_ops.mlops.drivers.lightning.get_config",
            "pyoneai_ops.mlops.drivers.base.get_config",
        ]:

            mocker.patch(
                path,
                return_value=self.config,
            )

    @pytest.fixture(autouse=True)
    def onetime_setup(self, mocker):
        # TODO: don't mock the entire class, just the logic that needs to be mocked
        mock_onetime = mocker.patch(
            "pyoneai_ops.mlops.dataset.OneTimeSeriesDataset"
        )
        mock_onetime.session = self.session
        mock_onetime.return_value.loader = torch.utils.data.DataLoader(
            torch.utils.data.TensorDataset(
                torch.arange(100 * 24, dtype=torch.float32).view(100, 24, 1),
                torch.arange(100, dtype=torch.float32).view(100, 1),
            ),
            batch_size=2,
        )

        self.one_dataset = mock_onetime.return_value

    @pytest.fixture(autouse=True)
    def synthetic_setup(self, mocker):
        self.synthetic_dataset = SyntheticTimeSeriesDataset(
            MagicMock(), slice("-1d", "-1h", "10m"), random_workload
        )

    def test_error_on_missing_entity(self):
        from pyoneai_ops.mlops.drivers.lightning import LightningDriver

        with pytest.raises(KeyError):
            LightningDriver(
                self.session,
                "host",
                "cpu_usage",
            )

    @pytest.mark.slow
    def test_save_checkpoint(self, save_path, mlmodels_path):
        from pyoneai_ops.mlops.drivers.lightning import LightningDriver

        LightningDriver(
            self.session,
            "virtualmachine",
            "cpu_usage",
            model_path="pyoneai.mlmodels.TransformerModel",
        ).fit(self.synthetic_dataset, save_path)
        assert os.path.exists(save_path)
