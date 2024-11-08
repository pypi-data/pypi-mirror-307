__all__ = ("LightningDriver",)
import logging
import os
from functools import cached_property
from typing import Self, Type

import lightning as L
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, IterableDataset

from pyoneai_ops.mlops.config import get_config
from pyoneai_ops.mlops.dataset import TimeSeriesDataset
from pyoneai_ops.mlops.drivers.base import BaseDriver

log = logging.getLogger("oneaiops.mlops.drivers.lightning")


class _PyTorchTimeSeriesWrapper(IterableDataset):
    def __init__(self, dataset: TimeSeriesDataset):
        self.dataset = dataset

    def __iter__(self):
        return (
            (mh.to_array(), mp.to_array()) for mh, mp in iter(self.dataset)
        )


class _ModelLightningWrapper(L.LightningModule):

    def __init__(
        self,
        ann_class: Type[nn.Module],
        model_path: str,
        hparams: dict,
        n: int = 1,
    ):
        super().__init__()
        self.save_hyperparameters(hparams)
        self.model = ann_class(**hparams)
        self.model_path = model_path
        self.n = n
        self.trues = []
        self.preds = []

    @cached_property
    def _lr(self) -> float:
        return get_config().models[self.model_path].training["lr"]

    @cached_property
    def _weight_decay(self) -> float:
        return get_config().models[self.model_path].training["weight_decay"]

    def forward(self, inputs):
        return self.model(inputs)

    def training_step(self, batch, batch_idx):
        inputs, target = batch
        output = self(inputs.to(torch.float32))
        loss = torch.nn.functional.mse_loss(
            output.to(torch.float32).squeeze(),
            target.to(torch.float32).view(-1),
        )
        self.log("train_loss", loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(
            self.model.parameters(),
            lr=self._lr,
            weight_decay=self._weight_decay,
        )

    def on_save_checkpoint(self, checkpoint):
        # NOTE: we need to remove "model" prefix from state key's
        # to avoid issues with loading model from checkpoint saved for this
        # class
        checkpoint["state_dict"] = {
            k.removeprefix("model."): v
            for k, v in checkpoint["state_dict"].items()
        }


class LightningDriver(BaseDriver):

    @cached_property
    def _batch_size(self) -> int:
        return get_config().models[self.model_path].training["batch_size"]

    @cached_property
    def _shuffle(self) -> bool:
        return get_config().models[self.model_path].training["shuffle"]

    @cached_property
    def _num_workers(self) -> int:
        return get_config().models[self.model_path].training["num_workers"]

    def configure_loader(self, dataset) -> torch.utils.data.DataLoader:
        return DataLoader(
            _PyTorchTimeSeriesWrapper(dataset),
            batch_size=self._batch_size,
            drop_last=True,
            num_workers=self._num_workers,
        )

    def fit(
        self, dataset: TimeSeriesDataset, weights: os.PathLike | str
    ) -> Self:
        """Run training based on PyTorch Lightning framework."""
        checkpoint_dir, checkpoint_file = os.path.split(weights)
        checkpoint_callback = L.pytorch.callbacks.ModelCheckpoint(
            dirpath=checkpoint_dir,
            filename=checkpoint_file,
            mode="min",
            monitor="train_loss",
            save_top_k=1,
            every_n_epochs=1,
            enable_version_counter=False,
        )
        checkpoint_callback.FILE_EXTENSION = ""

        trainer = L.Trainer(
            accelerator="auto",
            max_epochs=self._epochs,
            callbacks=[checkpoint_callback],
        )
        trainer.fit(
            model=_ModelLightningWrapper(
                self.ml_class, self.model_path, self.hparams
            ),
            train_dataloaders=self.configure_loader(dataset),
        )
        if trainer.global_step == 0:
            raise ValueError(
                "No training steps were performed. Check if the "
                "batch size is too large."
            )

    def test(
        self,
        dataset: TimeSeriesDataset,
        metrics: list[str],
        weights: os.PathLike | str | None = None,
    ) -> dict[str, float]:
        self.validate_metrics(metrics)

        # NOTE: we support custom weights loading.
        ann_model = self.ml_class.load(weights)

        preds = []
        trues = []
        for sample_id, (x, y) in enumerate(dataset):
            trues.append(y.to_array())
            output = ann_model.predict(x, n=self.n)
            preds.append(output.to_array())

        if not preds or not trues:
            raise ValueError("No predictions or true values were collected.")
        trues = np.concatenate(trues)
        preds = np.concatenate(preds)
        return {
            metric_name: compute_metric(trues, preds)
            for metric_name, compute_metric in zip(
                metrics, self.collect_metrics_callables(metrics)
            )
        }
