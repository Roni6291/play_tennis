import multiprocessing
from pathlib import Path

from fastapi import FastAPI
import uvicorn

from roger.asgi import StandaloneApplication
from roger.dataclasses import Playability, Version, Weather
from roger.inference import run_inference_on_live

app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.post('/infer/live/{version}')
def get_live_prediction(version: Version, weather: Weather) -> Playability:
    model_path = Path(f'./models/{version}/tennis.pkl')
    playability_ = run_inference_on_live(
        model_path=model_path,
        outlook=weather.outlook,
        temperature=weather.temperature,
        humidity=weather.humidity,
        wind=weather.wind,
    )
    play_map: dict[bool, str] = {
        True: 'FOR PLAYING',
        False: 'NOT TO PLAY',
    }
    return Playability(
        outlook=weather.outlook,
        temperature=weather.temperature,
        humidity=weather.humidity,
        wind=weather.wind,
        can_play=playability_,
        description=(
            'When '
            f' outlook is {weather.outlook.value} & '
            f'temperature is {weather.temperature.value} & '
            f'humidity is {weather.humidity.value} & '
            f'wind is {weather.wind.value}, '
            f'It is advised {play_map.get(playability_)}'
        ),
    )


def asgi_run():
    """Launched with `poetry run asgi` at root level."""
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)


# XXX: fails with ModuleNotFoundError: 'fcntl' not in Windows  # noqa: TD001
def gunicorn_run():
    """Launched with `poetry run wsgi` at root level."""
    options = {
        'bind': '0.0.0.0:8000',
        'workers': multiprocessing.cpu_count(),
        'worker_class': 'uvicorn.workers.UvicornWorker',
    }
    StandaloneApplication('myproject.main:app', options).run()
