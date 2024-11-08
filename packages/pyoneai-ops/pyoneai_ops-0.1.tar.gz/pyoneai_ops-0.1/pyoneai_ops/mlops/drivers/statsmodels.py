import os
import pickle
from logging import warning
from typing import Self

import numpy as np

from pyoneai_ops.mlops.dataset import TimeSeriesDataset
from pyoneai_ops.mlops.drivers.base import BaseDriver


class StatsmodelsDriver(BaseDriver):

    def fit(
        self, dataset: TimeSeriesDataset, weights: os.PathLike | str
    ) -> Self:
        """Run training based on statsmodels."""
        stats_model = self.ml_class(**self.hparams).fit(dataset)
        self._save_checkpoint(stats_model, weights)
        return self

    def _save_checkpoint(self, fitted_model, weights) -> None:
        with open(weights, "wb") as f:
            pickle.dump(fitted_model, f)

    def test(
        self,
        dataset: TimeSeriesDataset,
        metrics: list[str],
        weights: os.PathLike | str | None = None,
    ) -> dict[str, float]:
        if weights:
            warning(
                "Weights are not used for statsmodels models. "
                "The path will be ignored."
            )
        self.validate_metrics(metrics)

        stats_model = self.ml_class(**self.hparams)

        preds = []
        trues = []
        for sample_id, (x, y) in enumerate(dataset):
            trues.append(y.to_array())
            results_metric = stats_model.predict(x, self.n)
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
