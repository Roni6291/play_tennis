from pathlib import Path

import click

from .enums import Humidity, Outlook, Temperature, Wind
from .inference import run_inference_on_file, run_inference_on_live


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
    predictions = run_inference_on_file(
        model_path=model_path,
        data_path=data_path,
    )
    click.echo(predictions)


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
    predictions = run_inference_on_live(
        model_path=model_path,
        outlook=outlook,
        temperature=temperature,
        humidity=humidity,
        wind=wind,
    )
    click.echo(predictions)


@click.group(name='infer')
def run_inference():
    """Run Inference."""
    ...


run_inference.add_command(run_inference_bulk)
run_inference.add_command(run_inference_live)
