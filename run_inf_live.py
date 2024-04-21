from itertools import chain
from pathlib import Path

from roger.enums import Humidity, Outlook, Temperature, Wind
from roger.inference import infer
from roger.utils import one_hot_encode_enums


def run_inference_live(
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
    outlook_encoded = one_hot_encode_enums(Outlook, outlook)
    temp_encoded = one_hot_encode_enums(Temperature, temperature)
    humidity_encoded = one_hot_encode_enums(Humidity, humidity)
    wind_encoded = one_hot_encode_enums(Wind, wind)

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


if __name__ == '__main__':
    pred = run_inference_live(
        model_path=Path('./models/0.1.0/tennis.pkl'),
        outlook='Rain',
        temperature='Cool',
        humidity='Normal',
        wind='Weak',
    )
    print(pred)
