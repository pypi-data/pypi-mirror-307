import os.path as osp

from prefect.variables import Variable

from pyoneai_ops.mlops.const import Variables


def _apply_default_weights():
    lstm_weights_path = osp.join(
        "/", "etc", "one", "oneaiops", "models", "lstm", "checkpoint.ckpt"
    )
    if not osp.exists(lstm_weights_path):
        raise ValueError(
            f"Default LSTM weights not found at {lstm_weights_path}"
        )
    Variable.set(
        Variables.DEFAULT_LSTM_WEIGHTS, value=lstm_weights_path, overwrite=True
    )

    transformer_weights_path = osp.join(
        "/",
        "etc",
        "one",
        "oneaiops",
        "models",
        "transformer",
        "checkpoint.ckpt",
    )
    if not osp.exists(transformer_weights_path):
        raise ValueError(
            f"Default Transformer weights not found at {transformer_weights_path}"
        )
    Variable.set(
        Variables.DEFAULT_TRANSFORMER_WEIGHTS,
        value=transformer_weights_path,
        overwrite=True,
    )


def apply_variables():
    _apply_default_weights()
