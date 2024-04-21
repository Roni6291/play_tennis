from pathlib import Path

import pandas as pd


def feat_transform_infer(data_path: Path) -> pd.DataFrame:
    """Feature transformation on inference data.

    Args:
        data_path (Path): path to data (csv)

    Returns:
        pd.DataFrame: Feature engineered data
    """
    data = pd.read_csv(data_path.as_posix())
    return pd.get_dummies(data.drop(columns=['Play_Badminton']))
