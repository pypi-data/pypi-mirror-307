import os
import pickle

import numpy as np

from pyoneai_ops.mlops.dataset import TimeSeriesDataset
from pyoneai_ops.mlops.drivers.base import BaseDriver


class PersistenceModelDriver(BaseDriver):

    def fit(self, dataset: TimeSeriesDataset, weights: os.PathLike | str):
        """Run training with PersistenceModel"""
        persistence_model = self.ml_class(**self.hparams).fit(dataset)
        self._save_checkpoint(persistence_model, weights)
        return self

    def _save_checkpoint(self, fitted_model, weights) -> None:
        with open(weights, "wb") as f:
            pickle.dump(fitted_model, f)

    def test(
        self,
        dataset: TimeSeriesDataset,
        metrics: list[str],
        weights: os.PathLike | str | None = None,
    ):
        self.validate_metrics(metrics)

        persistence_model = self.ml_class(**self.hparams)

        preds = []
        trues = []
        for sample_id, (x, y) in enumerate(dataset):
            trues.append(y.to_array())
            results_metric = persistence_model.predict(x, self.n)
            preds.append(results_metric.to_array())

        if not preds or not trues:
            raise ValueError("No predictions or true values were collected.")
        trues = np.concatenate(trues).squeeze()
        preds = np.concatenate(preds).squeeze()
        return {
            metric_name: compute_metric(trues, preds)
            for metric_name, compute_metric in zip(
                metrics, self.collect_metrics_callables(metrics)
            )
        }
