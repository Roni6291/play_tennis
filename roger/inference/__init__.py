from itertools import chain
from pathlib import Path

from ..enums import Humidity, Outlook, Temperature, Wind  # noqa: TID252
from ..feat_engg import feat_transform_infer  # noqa: TID252
from ..utils import one_hot_encode_enums  # noqa: TID252
from .predictions import infer, infer_bulk


def run_inference_on_file(
    model_path: Path,
    data_path: Path,
) -> list[bool]:
    """Inference workflow on multiple data points.

    Args:
        model_path (Path): path to model
        data_path (Path): path to data

    Returns:
        list[bool]: predictions
    """
    data = feat_transform_infer(data_path)
    predictions = infer_bulk(
        model_path,
        data,
    )
    return predictions.tolist()


def run_inference_on_live(
    model_path: Path,
    outlook: str,
    temperature: str,
    humidity: str,
    wind: str,
) -> bool:
    """Inference workflow on single data point.

    Args:
        model_path (Path): path to model
        outlook (str): Outlook type
        temperature (str): Temp type
        humidity (str): Humidity type
        wind (str): Wind type

    Returns:
        bool: prediction
    """
    outlook_encoded = one_hot_encode_enums(Outlook, outlook.lower())
    temp_encoded = one_hot_encode_enums(Temperature, temperature.lower())
    humidity_encoded = one_hot_encode_enums(Humidity, humidity.lower())
    wind_encoded = one_hot_encode_enums(Wind, wind.lower())

    feats = list(
        chain(
            outlook_encoded,
            temp_encoded,
            humidity_encoded,
            wind_encoded,
        )
    )
    feat_cols = [
        'Outlook_Overcast',
        'Outlook_Rain',
        'Outlook_Sunny',
        'Temperature_Cool',
        'Temperature_Hot',
        'Temperature_Mild',
        'Humidity_High',
        'Humidity_Normal',
        'Wind_Strong',
        'Wind_Weak',
    ]
    predictions = infer(model_path, feat_cols=feat_cols, feats=feats)
    return predictions.tolist()[0]


__all__ = [
    'infer',
    'infer_bulk',
    'run_inference_on_file',
    'run_inference_on_live',
]
