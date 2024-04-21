from itertools import chain
from pathlib import Path

import click

from .enums import Humidity, Outlook, Temperature, Wind
from .feat_engg import feat_transform_infer
from .inference import infer, infer_bulk
from .utils import one_hot_encode_enums


@click.command(name='bulk')
@click.option(
    '-m',
    '--model_path',
    type=click.Path(
        exists=True,
        dir_okay=False,
        path_type=Path,
    ),
    help='path to model',
)
@click.option(
    '-d',
    '--data_path',
    type=click.Path(
        exists=True,
        dir_okay=False,
        path_type=Path,
    ),
    help='path to data',
)
def run_inference_bulk(
    model_path: Path,
    data_path: Path,
) -> None:
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
    click.echo(predictions.tolist())


@click.command(name='live')
@click.option(
    '-m',
    '--model_path',
    type=click.Path(
        exists=True,
        dir_okay=False,
        path_type=Path,
    ),
    help='path to model',
)
@click.option(
    '-o',
    '--outlook',
    type=click.Choice(
        choices=[e.value for e in Outlook],
        case_sensitive=False,
    ),
    help='Either of Overcast Rain Sunny',
)
@click.option(
    '-t',
    '--temperature',
    type=click.Choice(
        choices=[e.value for e in Temperature],
        case_sensitive=False,
    ),
    help='Either of Cool Hot Mild',
)
@click.option(
    '-h',
    '--humidity',
    type=click.Choice(
        choices=[e.value for e in Humidity],
        case_sensitive=False,
    ),
    help='Either of High Normal',
)
@click.option(
    '-w',
    '--wind',
    type=click.Choice(
        choices=[e.value for e in Wind],
        case_sensitive=False,
    ),
    help='Either of Strong Weak',
)
def run_inference_live(
    model_path: Path,
    outlook: str,
    temperature: str,
    humidity: str,
    wind: str,
) -> None:
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
    click.echo(predictions.tolist()[0])


@click.group(name='infer')
def run_inference():
    """Run Inference."""
    ...


run_inference.add_command(run_inference_bulk)
run_inference.add_command(run_inference_live)
