from collections.abc import Iterable
from pathlib import Path

import click

from .feat_engg import feat_transform_infer
from .inference import infer, infer_bulk


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
    '-d',
    '--data',
    nargs=10,
    type=click.IntRange(min=0, max=1),
    help="""Pass as `
        Outlook_Overcast Outlook_Rain Outlook_Sunny
        Temperature_Cool Temperature_Hot Temperature_Mild
        Humidity_High Humidity_Normal Wind_Strong Wind_Weak
        `
        """,
)
def run_inference_live(
    model_path: Path,
    data: Iterable[int],
) -> bool:
    """Inference workflow on single data point.

    Args:
        model_path (Path): path to model
        data (Iterable[int]): path to data

    Returns:
        bool: prediction
    """
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
    predictions = infer(model_path, feat_cols=feat_cols, feats=list(data))
    return predictions.tolist()[0]


@click.group(name='infer')
def run_inference():
    """Run Inference."""
    ...


run_inference.add_command(run_inference_bulk)
run_inference.add_command(run_inference_live)
