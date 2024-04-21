from pathlib import Path

import joblib
import numpy as np
import numpy.typing as npt
import pandas as pd


def infer_bulk(model_path: Path, data: pd.DataFrame) -> npt.NDArray[np.bool_]:
    """Run inference on multiple data points.

    Args:
        model_path (Path): path to model
        data (pd.DataFrame): path to file where inference data is stored

    Returns:
        npt.NDArray[np.bool_]: predictions
    """
    # loading model using joblib as it was pickled via this package
    model = joblib.load(model_path)
    return model.predict(data)


def infer(
    model_path: Path,
    feat_cols: list[str],
    feats: list[int],
) -> npt.NDArray[np.bool_]:
    """Run inference on single data point in live.

    Args:
        model_path (Path): path to model
        feat_cols (list[str]): all feature column names
        feats (list[int]): all features

    Returns:
        npt.NDArray[np.bool_]: predictions
    """
    # loading model using joblib as it was pickled via this package
    model = joblib.load(model_path)
    data = pd.DataFrame({feat_col: [feat] for feat_col, feat in zip(feat_cols, feats)})
    return model.predict(data)
