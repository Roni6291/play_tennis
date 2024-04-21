from pathlib import Path

from fastapi import FastAPI
import uvicorn

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
            f'temperature is{weather.temperature.value} & '
            f'humidity is {weather.humidity.value} & '
            f'wind is {weather.wind.value}, '
            f'It is advised {play_map.get(playability_)}'
        ),
    )


def start():
    """Launched with `poetry run start` at root level."""
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)
